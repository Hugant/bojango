from telegram import Update, Message
from telegram.ext import ContextTypes

from bojango.action.behaviors.base import register_behavior, BaseScreenBehavior
from bojango.action.screen import ScreenType, ActionScreen
from bojango.action.strategies.base import BaseContentStrategy, Transport


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
    transport = strategy.get_transport(context)
    await transport.send(**data)
    # if isinstance(strategy, ImageContentStrategy):
    #   await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)
    #   await context.bot.send_photo(**data)
    # elif isinstance(strategy, FileContentStrategy):
    #   await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_DOCUMENT)
    #   await context.bot.send_document(**data)
    # elif isinstance(strategy, TextContentStrategy):
    #   await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    #   await context.bot.send_message(**data)
    # else:
    #   raise ValueError(f'Unknown content strategy: {type(strategy).__name__}')


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

    transport = strategy.get_transport(context)
    await transport.send(**data)


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
    transport = strategy.get_transport(context)

    if update.callback_query:
      message = update.callback_query.message
      message_id = message.message_id
      new_kind = transport.kind
      prev_kind = Transport.detect_message_kind(message)

      legitimate = new_kind == prev_kind
      await transport.edit(data=data, message_id=message_id, chat_id=update.effective_chat.id, legitimate=legitimate)
    elif screen.message_id:
      print(update)
      print(context)
      await transport.edit(data=data, message_id=screen.message_id, chat_id=None)
    else:
      await transport.send(**data)


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
      transport = strategy.get_transport(context)
      await transport.remove_keyboard(chat_id=update.effective_chat.id,
                                      message_id=update.callback_query.message.message_id)
    else:
      raise ValueError(
        'Unable to remove keyboard: no callback_query found. '
        'Keyboard removal is only possible in response to a callback interaction.'
      )
