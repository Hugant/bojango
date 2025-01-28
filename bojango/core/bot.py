import asyncio
import importlib
import logging
from dataclasses import dataclass, field
from typing import Optional, List

from telegram.ext import ApplicationBuilder, Application

from bojango.action.manager import ActionManager
from bojango.core.routing import Router
from bojango.utils.localization import BaseLocalizer


@dataclass
class BojangoBotConfig:
  """Конфигурация бота."""
  api_token: str
  localizer: BaseLocalizer
  handlers_modules: List[str]
  telegram_bot_base_url: Optional[str] = None


class BojangoBot:
  """Класс основного бота Bojango."""

  def __init__(self, config: BojangoBotConfig):
    """
    Инициализация бота с заданной конфигурацией.

    :param config: Конфигурация бота.
    """
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

  def _validate_config(self):
    """Валидация конфигурации бота."""
    if not self.config.api_token:
      raise ValueError('API token must be set in the configuration.')
    if not self.config.localizer:
      raise ValueError('LocalizationManager must be set in the configuration.')
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
