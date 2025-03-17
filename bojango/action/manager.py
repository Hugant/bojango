from typing import Callable, AsyncIterable, Dict, Any
from telegram import Update
from telegram.ext import ContextTypes
import logging

from bojango.action.screen import ActionScreen
from bojango.core.utils import decode_callback_data, pop_user_data_kwargs

logger = logging.getLogger(__name__)


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

  async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE, **kwargs) -> \
  AsyncIterable[ActionScreen]:
    """Выполняет действие, возвращающее экраны."""
    result = self.callback(update, context, **kwargs)

    logger.debug(f'Executing action: {self.name} with args: {kwargs}')
    try:
      if hasattr(result, '__aiter__'):
        async for screen in result:
          yield screen
      else:
        screen = await result
        yield screen
    except TypeError as e:
      raise TypeError(f'Executing action {self.name} required positional arguments: {e.args[0]}')


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

  async def execute_action(self, name: str, update: Update, context: ContextTypes.DEFAULT_TYPE, **kwargs) -> None:
    """
    Выполняет действие по имени.

    :param name: Имя действия.
    :param update: Объект обновления Telegram.
    :param context: Контекст Telegram.
    :param args: Дополнительные параметры.
    :raises ValueError: Если действие возвращает не ActionScreen.
    """
    logger.info(f'Executing action: {name} with args: {kwargs}')
    action = self.get_action(name)
    try:
      async for screen in action.execute(update, context, **kwargs):
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
  async def handle(name: str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обрабатывает callback и выполняет действие.

    :param name: Имя действия.
    :param update: Объект обновления Telegram.
    :param context: Контекст Telegram.
    :param data: Дополнительные данные.
    """
    data = {}
    logger.debug(f'Handling action: {name} with data: {data}')
    try:
      kwargs = pop_user_data_kwargs(update.callback_query, context.user_data)
      await ActionManager().execute_action(name, update, context, **kwargs)
    except Exception as e:
      logger.exception(f'Error handling action "{name}": {e}')

  @staticmethod
  async def redirect(action_name: str, update: Update, context: ContextTypes.DEFAULT_TYPE,
                     **kwargs) -> ActionScreen:
    """
    Редирект на указанное действие.

    :param action_name: Имя действия для вызова.
    :param update: Объект Update.
    :param context: Контекст Telegram.
    :param args: Аргументы для переданного действия.
    """
    logger.info('Redirecting to action: %s', action_name)
    action_manager: ActionManager = ActionManager()
    action = action_manager.get_action(action_name)
    kwargs = {**pop_user_data_kwargs(update.callback_query, context.user_data), **kwargs}
    print(kwargs)
    async for screen in action.execute(update, context, **kwargs):
      if screen:
        return screen
