from typing import Callable, Self

from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

from bojango.action.manager import ActionManager
from bojango.action.screen import ActionScreen
from bojango.core.utils import decode_callback_data, pop_user_data_kwargs


class Router:
	"""Класс маршрутизации для обработки команд и callback запросов."""

	# Ограничения телеграмма в длину callback_data 64 символа, также берем qid, при формировании кнопок ?qid=25042272,
	# в итоге максимальная длина callback действия 51, и 1 на запас
	MAX_QUERY_LENGTH: int = 50
	_instance: Self | None = None

	def __new__(cls, action_manager: ActionManager | None = None) -> Self:
		if cls._instance is None:
			if action_manager is None:
				raise ValueError('ActionManager должен быть передан при первом создании Router.')
			cls._instance = super().__new__(cls)
			cls._instance._action_manager = action_manager
			cls._instance._commands = {}
			cls._instance._callbacks = {}
			cls._instance._message_handlers = []
			cls._instance._audio_handler = None
			cls._instance._video_note_handler = None
		return cls._instance

	def register_command(self, command: str, handler: Callable) -> None:
		"""Регистрирует команду для обработки.

    :param command: Название команды.
    :param handler: Обработчик команды.
    """
		self._commands[command] = handler
		self._action_manager.register_action(command, handler)

	def register_callback(self, query: str, handler: Callable) -> None:
		"""Регистрирует callback для обработки.

    :param query: Шаблон callback.
    :param handler: Обработчик callback.
    """
		self._callbacks[query] = handler
		self._action_manager.register_action(query, handler)

	def register_message(self, handler: Callable, pattern: str = '.*') -> None:
		"""Регистрирует обработчик сообщений."""
		self._message_handlers.append((pattern, handler))

	def register_audio_handler(self, handler: Callable) -> None:
		"""
		Регистрирует обработчик аудио сообщений.

		:param handler: Функция-обработчик аудио.
		"""
		self._audio_handler = handler

	def register_video_note_handler(self, handler: Callable) -> None:
		"""
		Регистрирует обработчик аудио сообщений.

		:param handler: Функция-обработчик аудио.
		"""
		self._video_note_handler = handler

	def attach_to_application(self, application: Application) -> None:
		"""Привязывает маршруты к Telegram Application.

    :param application: Экземпляр Telegram Application.
    """
		for command, handler in self._commands.items():
			application.add_handler(CommandHandler(command, handler))
		for query, handler in self._callbacks.items():
			application.add_handler(CallbackQueryHandler(handler, pattern=f'{query}'))

		for pattern, handler in self._message_handlers:
			application.add_handler(MessageHandler(filters.TEXT & filters.Regex(pattern), handler))

		if self._audio_handler:
			application.add_handler(MessageHandler(filters.VOICE, self._audio_handler))

		if self._video_note_handler:
			application.add_handler(MessageHandler(filters.VIDEO_NOTE, self._video_note_handler))

	def get_routes(self) -> dict[str, Callable]:
		"""Возвращает все зарегистрированные маршруты.

    :return: Словарь маршрутов.
    """
		return {**self._commands, **self._callbacks}


def _wrap_handler(handler: Callable) -> Callable:
	"""Обёртка для обработки async_generator и передачи аргументов."""

	async def wrapped_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, **kwargs) -> None:
		"""
		Обработчик, принимающий аргументы.

		:param update: Объект обновления Telegram.
		:param context: Контекст.
		:param args: Дополнительные аргументы.
		"""
		kwargs = {**kwargs, **pop_user_data_kwargs(update.callback_query, context.user_data)}
		# try
		result = handler(update, context, **kwargs)

		if hasattr(result, '__aiter__'):
			async for screen in result:
				if isinstance(screen, ActionScreen):
					await screen.render(update, context)
				else:
					raise ValueError('Обработчик должен возвращать ActionScreen.')
		else:
			await result

	return wrapped_handler


def command(name: str) -> Callable:
	"""Декоратор для регистрации команды.

  :param name: Название команды.
  :return: Обёрнутый обработчик.
  """

	def decorator(handler: Callable) -> Callable:
		router = Router()
		router.register_command(name, _wrap_handler(handler))
		return handler

	return decorator


def callback(query: str) -> Callable:
	"""Декоратор для регистрации callback.

  :param query: Шаблон callback.
  :return: Обёрнутый обработчик.
  """

	if len(query) > Router.MAX_QUERY_LENGTH:
		raise ValueError(f'Callback name "{query}" is too long ({len(query)} chars). '
										 f'Max length: {Router.MAX_QUERY_LENGTH}.')

	def decorator(handler: Callable) -> Callable:
		router = Router()
		router.register_callback(query, _wrap_handler(handler))
		return handler

	return decorator


def message(pattern: str = ".*") -> Callable:
	"""
	Декоратор для регистрации хендлера текстовых сообщений.

	:param pattern: Регулярное выражение для фильтрации сообщений.
	"""

	def decorator(handler: Callable) -> Callable:
		router = Router()
		router.register_message(handler, pattern)
		return handler

	return decorator


def audio() -> Callable:
	"""
	Декоратор для регистрации обработчика аудио сообщений.
	"""

	def decorator(handler: Callable) -> Callable:
		router = Router()
		router.register_audio_handler(handler)
		return handler

	return decorator


def video_note() -> Callable:
	"""
	Декоратор для регистрации обработчика аудио сообщений.
	"""

	def decorator(handler: Callable) -> Callable:
		router = Router()
		router.register_video_note_handler(handler)
		return handler

	return decorator



# TODO: Переписать методику работы с языками
# ⚙️ Что можно улучшить или упростить
# 1. Проблема глобального состояния → set_language() меняет default_language глобально
# Это может создать гонки состояний, особенно если параллельно обрабатываются несколько пользователей.
#
# ✅ Решение:
# Убираем set_language() из боевого кода. Вместо этого всегда передаём lang в get_translation() и translate().
#
# ➡️ Например:
#
# python
# Copy
# Edit
# def translate(self, key: str, lang: str | None = None, **kwargs) -> str:
#   translation = self.get_translation(lang)
#   ...
# И далее:
#
# python
# Copy
# Edit
# localizer.translate('some_key', lang=user.lang)
# 2. Singleton с явной инициализацией — может быть проблемным
# Ты проверяешь наличие _instance, но если где-то забыть __init__, код сломается.
#
# ✅ Решение:
# Создай отдельный метод для инициализации:
#
# python
# Copy
# Edit
# @classmethod
# def initialize(cls, locales_dir: str, default_language: str = 'ru') -> None:
#   if cls._instance is None:
#     cls._instance = cls(locales_dir, default_language)
# Затем вызываешь один раз при старте бота:
#
# python
# Copy
# Edit
# LocalizationManager.initialize(locales_dir='locales', default_language='ru')
# 3. Идея: Сделать LocalizerService без Singleton
# Если хочешь избежать глобального состояния, можешь создать обёртку, где каждый пользователь получает независимый объект.
#
# 4. Идея: Fallback по умолчанию, если перевода нет
# Сейчас ты выбрасываешь TranslationKeyNotFoundError, но может быть полезно — возвращать сам key и логировать.
#
# Альтернатива:
# Добавь параметр strict=True и в translate:
#
# python
# Copy
# Edit
# if translated_text == key:
#   if strict:
#     raise TranslationKeyNotFoundError(key)
#   logger.warning(f'Missing translation: {key}')
#   return key
# 💾 Улучшенный translate() с параметром lang и fallback:
# python
# Copy
# Edit
# def translate(self, key: str, lang: str | None = None, strict: bool = False, **kwargs) -> str:
#   translation = self.get_translation(lang)
#   try:
#     translated_text = translation.gettext(key)
#     if translated_text == key and strict:
#       raise KeyError
#     logger.debug('Translating key "%s": %s', key, translated_text)
#     return translated_text % kwargs if kwargs else translated_text
#   except KeyError:
#     logger.warning('Translation key "%s" not found.', key)
#     return key
# 🧩 Вариант вызова:
# Вместо глобального set_language():
#
# python
# Copy
# Edit
# localizer = LocalizationManager.get_instance()
# text = localizer.translate('welcome_text', lang=user.lang)
# 🧩 LateValue — идеально, оставить как есть ✅
# Резюме:
# Пункт	Оценка / Совет
# Singleton	Ок, но лучше через initialize()
# set_language()	Потенциальная угроза — убрать из использования
# translate()	Добавить lang, убрать глобальный state
# LateValue	Отлично реализовано
# Logging	Всё на уровне, можно расширить в strict=False
# Готов к следующему блоку — можем посмотреть, как ты интегрируешь LocalizationManager в шаблонизацию или в тексты сообщений.

# TODO:
# 2. DRY: Обёртка для сокращения одинаковых функций
# Можно сделать универсальный декоратор-обёртку, чтобы не писать одно и то же:
#
# python
# Copy
# Edit
# def redirect_command(target: str):
# 	def wrapper(func):
# 		@command(func.__name__[2:])  # имя команды = имя функции без 'c_'
# 		async def inner(update, context):
# 			await ActionManager.redirect(target, update, context)
# 		return inner
# 	return wrapper
# Пример использования:
#
# python
# Copy
# Edit
# @redirect_command('l_start')
# async def c_start(update, context): pass
#
# @redirect_command('s_lang')
# async def c_lang(update, context): pass

# ➡️ Это уменьшит дублирование, но добавит немного абстракции — только если хочешь чистоту.

