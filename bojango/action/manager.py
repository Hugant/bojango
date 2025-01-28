from typing import Callable, AsyncIterable, Dict, Any
from telegram import Update
from telegram.ext import ContextTypes
import logging

from bojango.action.screen import ActionScreen
from bojango.core.utils import decode_callback_data


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)


class ActionAlreadyExistsError(Exception):
  """Исключение, вызываемое при повторной регистрации действия."""
  def __init__(self, action_name: str, message='Action already exists'):
    message = f'{message}: "{action_name}"'
    super().__init__(message)
    self.action_name = action_name


class UnknownActionError(Exception):
  """Исключение, вызываемое при попытке вызвать неизвестное действие."""
  def __init__(self, action_name: str, message='Unknown action'):
    message = f'{message}: "{action_name}"'
    super().__init__(message)
    self.action_name = action_name


class Action:
  """Класс, представляющий отдельное действие."""
  def __init__(self, name: str, callback: Callable):
    """
    :param name: Имя действия.
    :param callback: Callback-функция, которая возвращает AsyncIterable[ActionScreen].
    """
    self.name = name
    self.callback = callback
    logger.debug(f'Action initialized: {name}')

  async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE, args: Dict[str, Any] | None = None) -> AsyncIterable[ActionScreen]:
    """
    Выполняет действие и возвращает экраны.

    :param update: Объект обновления от Telegram.
    :param context: Контекст Telegram.
    :param args: Дополнительные аргументы.
    :yield: ActionScreen объекты для рендера.
    """
    logger.debug(f'Executing action: {self.name} with args: {args}')
    async for screen in self.callback(update, context, args):
      yield screen


class ActionManager:
  """Менеджер для регистрации и выполнения действий (Singleton)."""
  _instance = None

  def __new__(cls):
    if cls._instance is None:
      cls._instance = super().__new__(cls)
      cls._instance._actions = {}
      logger.debug('ActionManager initialized as a singleton.')
    return cls._instance

  def register_action(self, name: str, callback: Callable) -> None:
    """
    Регистрирует новое действие.

    :param name: Имя действия.
    :param callback: Callback-функция для выполнения действия.
    :raises ActionAlreadyExistsError: Если действие с таким именем уже существует.
    """
    if name in self._actions:
      logger.error(f'Attempted to register an action that already exists: {name}')
      raise ActionAlreadyExistsError(name)
    self._actions[name] = Action(name, callback)
    logger.info(f'Action registered: {name}')

  def get_action(self, name: str) -> Action:
    """
    Получает действие по имени.

    :param name: Имя действия.
    :return: Объект действия.
    :raises UnknownActionError: Если действие не найдено.
    """
    if name not in self._actions:
      logger.error(f'Unknown action requested: {name}')
      raise UnknownActionError(name)
    logger.debug(f'Action retrieved: {name}')
    return self._actions[name]

  async def execute_action(self, name: str, update: Update, context: ContextTypes.DEFAULT_TYPE, args: Dict[str, Any] | None = None) -> None:
    """
    Выполняет действие по имени.

    :param name: Имя действия.
    :param update: Объект обновления Telegram.
    :param context: Контекст Telegram.
    :param args: Дополнительные параметры.
    :raises ValueError: Если действие возвращает не ActionScreen.
    """
    logger.info(f'Executing action: {name} with args: {args}')
    action = self.get_action(name)
    try:
      async for screen in action.execute(update, context, args):
        if isinstance(screen, ActionScreen):
          logger.debug(f'Rendering screen from action: {name}')
          await screen.render(update, context)
        else:
          logger.error(f'Invalid screen returned by action: {name}')
          raise ValueError(f'Default action must return ActionScreen, got {type(screen)}.')
    except Exception as e:
      logger.exception(f'Error while executing action {name}: {e}')
      raise

  @staticmethod
  async def handle(name: str, update: Update, context: ContextTypes.DEFAULT_TYPE, **data) -> None:
    """
    Обрабатывает callback и выполняет действие.

    :param name: Имя действия.
    :param update: Объект обновления Telegram.
    :param context: Контекст Telegram.
    :param data: Дополнительные данные.
    """
    logger.debug(f'Handling action: {name} with data: {data}')
    try:
      query = update.callback_query
      if query and query.data:
        name, args = decode_callback_data(query.data)
        if data:
          args = {**args, **data} if args else data
      else:
        args = data

      await ActionManager().execute_action(name, update, context, args=args)
    except Exception as e:
      logger.exception(f'Error handling action "{name}": {e}')
