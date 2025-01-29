from typing import Callable, Self

from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

from bojango.action.manager import ActionManager
from bojango.action.screen import ActionScreen
from bojango.core.utils import decode_callback_data


class Router:
	"""Класс маршрутизации для обработки команд и callback запросов."""

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

	def attach_to_application(self, application: Application) -> None:
		"""Привязывает маршруты к Telegram Application.

    :param application: Экземпляр Telegram Application.
    """
		for command, handler in self._commands.items():
			application.add_handler(CommandHandler(command, handler))
		for query, handler in self._callbacks.items():
			application.add_handler(CallbackQueryHandler(handler, pattern=f'^{query}'))

		for pattern, handler in self._message_handlers:
			application.add_handler(MessageHandler(filters.ALL, handler))

	def get_routes(self) -> dict[str, Callable]:
		"""Возвращает все зарегистрированные маршруты.

    :return: Словарь маршрутов.
    """
		return {**self._commands, **self._callbacks}


def _wrap_handler(handler: Callable, expects_args: bool = False) -> Callable:
	"""Обёртка для обработки async_generator и передачи аргументов."""

	async def wrapped_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, args: dict | None = None) -> None:
		"""
		Обработчик, принимающий аргументы.

		:param update: Объект обновления Telegram.
		:param context: Контекст.
		:param args: Дополнительные аргументы.
		"""
		args = args or {}

		query = update.callback_query
		if query and query.data:
			action_name, decoded_args = decode_callback_data(query.data)
			args.update(decoded_args or {})

		# Вызываем обработчик
		if expects_args:
			result = handler(update, context, args)
		else:
			result = handler(update, context)

		# Если это async_generator
		if hasattr(result, '__aiter__'):
			async for screen in result:
				if isinstance(screen, ActionScreen):
					await screen.render(update, context)
				else:
					raise ValueError('Обработчик должен возвращать ActionScreen.')
		else:
			await result  # Если это обычная корутина

	return wrapped_handler


def command(name: str) -> Callable:
	"""Декоратор для регистрации команды.

  :param name: Название команды.
  :return: Обёрнутый обработчик.
  """

	def decorator(handler: Callable) -> Callable:
		router = Router()
		router.register_command(name, _wrap_handler(handler, expects_args=False))
		return handler

	return decorator


def callback(query: str) -> Callable:
	"""Декоратор для регистрации callback.

  :param query: Шаблон callback.
  :return: Обёрнутый обработчик.
  """

	def decorator(handler: Callable) -> Callable:
		router = Router()
		router.register_callback(query, _wrap_handler(handler, expects_args=True))
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
