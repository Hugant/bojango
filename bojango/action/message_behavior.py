from abc import abstractmethod, ABC
from typing import Type, Callable

from telegram import Update, InlineKeyboardMarkup
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from bojango.action.content_strategy import BaseContentStrategy, ImageContentStrategy, FileContentStrategy, \
  TextContentStrategy
from bojango.action.screen import ScreenType, ActionScreen


class BaseScreenBehavior(ABC):
  BEHAVIORS: dict[ScreenType, Type['BaseScreenBehavior']] = {}

  @staticmethod
  def resolve_behavior(screen_type: ScreenType) -> 'BaseScreenBehavior':
    behavior_cls = BaseScreenBehavior.BEHAVIORS.get(screen_type)

    if behavior_cls is None:
      raise ValueError(f'Behavior type {screen_type} not supported')

    return behavior_cls()

  @abstractmethod
  async def render(
    self,
    screen: ActionScreen,
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    strategy: BaseContentStrategy
  ) -> None:
    raise NotImplementedError


def register_behavior(screen_type: ScreenType) -> Callable[[Type[BaseScreenBehavior]], Type[BaseScreenBehavior]]:
  """
  Декоратор для регистрации поведения экрана.

  :param screen_type: Тип экрана (ScreenType), для которого регистрируется поведение.
  """
  def decorator(cls: Type[BaseScreenBehavior]) -> Type[BaseScreenBehavior]:
    BaseScreenBehavior.BEHAVIORS[screen_type] = cls
    return cls

  return decorator


@register_behavior(ScreenType.NEW)
class NewScreenBehavior(BaseScreenBehavior):
  """
  Поведение для отправки нового сообщения (ScreenType.NEW).
  """

  async def render(
    self,
    screen: ActionScreen,
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    strategy: BaseContentStrategy
  ) -> None:
    data = await strategy.prepare(screen, update, context)

    if isinstance(strategy, ImageContentStrategy):
      await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)
      await context.bot.send_photo(**data)
    elif isinstance(strategy, FileContentStrategy):
      await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_DOCUMENT)
      await context.bot.send_document(**data)
    elif isinstance(strategy, TextContentStrategy):
      await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
      await context.bot.send_message(**data)
    else:
      raise ValueError(f'Unknown content strategy: {type(strategy).__name__}')


@register_behavior(ScreenType.REPLY)
class ReplyScreenBehavior(BaseScreenBehavior):
  """
  Поведение для отправки сообщения ответом (ScreenType.REPLY).
  """

  async def render(
    self,
    screen: ActionScreen,
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    strategy: BaseContentStrategy
  ) -> None:
    data = await strategy.prepare(screen, update, context)
    data['reply_to_message_id'] = screen.message_id

    if not screen.message_id:
      raise ValueError('Unable to reply to message: no message_id provided.')

    if isinstance(strategy, ImageContentStrategy):
      await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)
      await context.bot.send_photo(**data)
    elif isinstance(strategy, FileContentStrategy):
      await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_DOCUMENT)
      await context.bot.send_document(**data)
    elif isinstance(strategy, TextContentStrategy):
      await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
      await context.bot.send_message(**data)
    else:
      raise ValueError(f'Unknown content strategy: {type(strategy).__name__}')


@register_behavior(ScreenType.REPLACE)
class ReplaceScreenBehavior(BaseScreenBehavior):
  """
  Поведение для замены сообщения (ScreenType.REPLACE).
  """

  async def render(
    self,
    screen: ActionScreen,
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    strategy: BaseContentStrategy
  ) -> None:
    data = await strategy.prepare(screen, update, context)

    if update.callback_query:
      chat_id = update.effective_chat.id
      message = update.callback_query.message
      message_id = message.message_id

      is_photo = bool(message.photo)
      is_document = bool(message.document)

      if is_photo and not isinstance(strategy, ImageContentStrategy):
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
        await context.bot.send_message(**data)
        return

      if is_document and not isinstance(strategy, FileContentStrategy):
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
        await context.bot.send_message(**data)
        return

      if isinstance(strategy, ImageContentStrategy):
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)
        await context.bot.send_photo(**data)
      elif isinstance(strategy, FileContentStrategy):
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_DOCUMENT)
        await context.bot.send_document(**data)
      else:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
        await context.bot.edit_message_text(**data, message_id=message_id)
    else:
      await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
      await context.bot.send_message(**data)


@register_behavior(ScreenType.REMOVE_KEYBOARD)
class RemoveKeyboardScreenBehavior(BaseScreenBehavior):
  """
  Поведение для удаления клавиатуры в сообщении (ScreenType.REMOVE_KEYBOARD).
  """

  async def render(
    self,
    screen: ActionScreen,
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    strategy: BaseContentStrategy
  ) -> None:
    if update.callback_query:
      await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
      await context.bot.edit_message_reply_markup(
        chat_id=update.effective_chat.id,
        message_id=update.callback_query.message.message_id,
        reply_markup=InlineKeyboardMarkup([]),
      )
    else:
      raise ValueError(
        'Unable to remove keyboard: no callback_query found. '
        'Keyboard removal is only possible in response to a callback interaction.'
      )
