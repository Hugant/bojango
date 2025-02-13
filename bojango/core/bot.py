import asyncio
import importlib
import logging
from dataclasses import dataclass, field
from typing import Optional, List, Self

from telegram import Message
from telegram.ext import ApplicationBuilder, Application

from bojango.action.manager import ActionManager
from bojango.core.routing import Router
from bojango.utils.localization import BaseLocalizer


@dataclass
class BojangoBotConfig:
  """Конфигурация бота."""
  api_token: str
  handlers_modules: List[str]
  localizer: Optional[BaseLocalizer] = None
  telegram_bot_base_url: Optional[str] = None


class BojangoBot:
  """Класс основного бота Bojango."""

  _instance: Self | None = None

  def __init__(self, config: BojangoBotConfig):
    """
    Инициализация бота с заданной конфигурацией.

    :param config: Конфигурация бота.
    """
    if BojangoBot._instance is not None:
      raise RuntimeError('BojangoBot has been initialized. Use get_instance().')

    self.config = config
    self._validate_config()

    self.logger = logging.getLogger(self.__class__.__name__)
    self.logger.info('Initializing BojangoBot...')

    # Настройка Telegram Application
    self.__app = ApplicationBuilder().token(config.api_token)
    if config.telegram_bot_base_url:
      self.__app.base_url(config.telegram_bot_base_url)
    self.__app.local_mode(True)
    self.__app: Application = self.__app.build()

    # Инициализация ActionManager и Router
    self.action_manager = ActionManager()
    self.router = Router(self.action_manager)

    # Загрузка модулей обработчиков
    self._load_handlers()
    self.__app.bot_data['action_manager'] = self.action_manager
    self.router.attach_to_application(self.__app)

    BojangoBot._instance = self

  @classmethod
  def get_instance(cls) -> Self:
    """
		Возвращает текущий экземпляр BojangoBot.

		:return: Экземпляр бота.
		:raises RuntimeError: Если бот еще не был инициализирован.
		"""
    if cls._instance is None:
      raise RuntimeError('BojangoBot has not initialized. Сначала создайте его экземпляр.')
    return cls._instance

  def _validate_config(self):
    """Валидация конфигурации бота."""
    if not self.config.api_token:
      raise ValueError('API token must be set in the configuration.')
    # if not self.config.localizer:
    #   raise ValueError('LocalizationManager must be set in the configuration.')
    if not self.config.handlers_modules:
      raise ValueError('At least one handlers module must be specified in the configuration.')

  def _load_handlers(self):
    """Загружает обработчики из указанных модулей."""
    self.logger.info('Loading handler modules...')
    for module_name in self.config.handlers_modules:
      try:
        importlib.import_module(module_name)
        self.logger.info(f'Successfully loaded module: {module_name}')
      except ImportError as e:
        self.logger.error(f'Failed to load module "{module_name}": {e}', exc_info=True)
        raise

  async def start(self):
    """Асинхронный запуск бота."""
    self.logger.info('Starting bot...')
    try:
      await self.__app.initialize()
      await self.__app.start()
      self.logger.info('Bot started successfully.')
      await self.__app.updater.start_polling()
      self.logger.info('Bot is polling for updates...')
      await asyncio.Event().wait()
    except Exception as e:
      self.logger.error(f'Critical error during bot start: {e}', exc_info=True)
      await self.stop()

  async def stop(self):
    """Остановка бота."""
    self.logger.info('Stopping bot...')
    try:
      await self.__app.updater.stop()
      await self.__app.stop()
      await self.__app.shutdown()
      self.logger.info('Bot stopped successfully.')
    except Exception as e:
      self.logger.error(f'Error during bot stop: {e}', exc_info=True)

  def run(self):
    """
    Синхронный запуск бота через asyncio.run.

    Этот метод блокирует выполнение программы до завершения работы бота.
    """
    self.logger.info('Running bot synchronously...')
    asyncio.run(self.start())

  async def send_message(self, chat_id: int, text: str, parse_mode: str = 'Markdown', reply_markup=None) -> Message:
    """
    Отправляет сообщение пользователю.

    :param chat_id: ID чата пользователя.
    :param text: Текст сообщения.
    :param parse_mode: Режим разметки (по умолчанию Markdown).
    :param reply_markup: Клавиатура или инлайн-кнопки.
    :return: Объект отправленного сообщения.
    """
    self.logger.debug('Sending message to chat %s', chat_id)
    return await self.__app.bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode,
                                             reply_markup=reply_markup)

  async def edit_message(self, chat_id: int, message_id: int, new_text: str, parse_mode: str = 'Markdown',
                         reply_markup=None):
    """
    Редактирует существующее сообщение.

    :param chat_id: ID чата пользователя.
    :param message_id: ID редактируемого сообщения.
    :param new_text: Новый текст сообщения.
    :param parse_mode: Режим разметки (по умолчанию Markdown).
    :param reply_markup: Клавиатура или инлайн-кнопки.
    """
    self.logger.debug('Editing message %s in chat %s', message_id, chat_id)
    await self.__app.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=new_text, parse_mode=parse_mode,
                                           reply_markup=reply_markup)

