import logging
from enum import Enum
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bojango.core.utils import encode_callback_data
from bojango.utils.localization import LateValue


logger = logging.getLogger(__name__)


class ScreenType(Enum):
  """Типы экранов."""
  NEW = 'new'  # Создать новое сообщение
  REPLACE = 'replace'  # Заменить текст и клавиатуру существующего сообщения
  REMOVE_KEYBOARD = 'remove_keyboard'  # Удалить клавиатуру из сообщения
  REPLY = 'reply'  # Ответить на сообщение


class ActionButton:
  """Класс для управления кнопками экрана."""
  def __init__(self, text: str | LateValue, action_name: str | None = None, url: str | None = None, **kwargs):
    """
    :param text: Текст кнопки или LateValue для локализации.
    :param action_name: Название действия, которое вызовет кнопка.
    :param args: Дополнительные аргументы для действия.
    """
    self.text = text
    self.url = url
    self.action_name = action_name
    self.kwargs = kwargs
    self.query_id = str(abs(hash(id(self))) % 10**8)

    if self.action_name is None and self.url is None:
      raise ValueError('You must specify either action_name or url')


class ActionScreen:
  """Класс для управления экранами действий."""
  def __init__(
    self,
    text: str | LateValue | None = None,
    image: str | bytes | None = None,
    file: str | bytes | None = None,
    buttons: list[list[ActionButton]] | None = None,
    screen_type: ScreenType = ScreenType.REPLACE,
    message_id: int | None = None
  ) -> None:
    """
    :param text: Текст сообщения или LateValue для локализации.
    :param buttons: Клавиатура в виде списка списков ActionButton.
    :param screen_type: Тип экрана (ScreenType).
    :param message_id: ID сообщения для редактирования, если применимо.
    """

    if text is None and file is None and image is None:
      raise ValueError('You must specify either text, image or file')

    if image and file:
      raise ValueError('Cannot attach both image and file to a single message.')

    self.text = text
    self.image = image
    self.file = file
    self.buttons = buttons or []
    self.screen_type = screen_type
    self.message_id = message_id

  async def render(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Отображает экран в зависимости от его типа.

    :param update: Объект Update Telegram.
    :param context: Объект Context Telegram.
    """

    from bojango.action.content_strategy import BaseContentStrategy
    from bojango.action.message_behavior import BaseScreenBehavior

    behavior = BaseScreenBehavior.resolve_behavior(self.screen_type)
    strategy = BaseContentStrategy.resolve_strategy(self)

    logger.info(f'Rendering screen: {self.screen_type}, Chat ID: {update.effective_chat.id}')

    try:
      await behavior.render(screen=self, update=update, context=context, strategy=strategy)

      if update.callback_query:
        await update.callback_query.answer()
    except Exception as e:
      logger.error(f'Screen render error: {e}')
      raise

  def resolve_text(self, text: str | LateValue) -> str:
    """
    Возвращает строку из текста или LateValue.

    :param text: Текстовая строка или объект LateValue.
    :return: Разрешённая строка.
    """
    resolved_text = text.value if isinstance(text, LateValue) else text
    logger.debug(f'Text resolved: {resolved_text}')
    return resolved_text

  def generate_keyboard(self, context: ContextTypes.DEFAULT_TYPE) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру из кнопок.

    :return: Объект InlineKeyboardMarkup с клавиатурой.
    """
    keyboard = []
    for row in self.buttons:
      buttons_row = []

      for button in row:
        if button.url:
          buttons_row.append(
            InlineKeyboardButton(
              text=self.resolve_text(button.text),
              url=button.url,
            )
          )
        else:
          context.user_data[button.query_id] = button.kwargs or {}
          buttons_row.append(
            InlineKeyboardButton(
              text=self.resolve_text(button.text),
              callback_data=encode_callback_data(button.action_name, {'qid': button.query_id}),
            )
          )

      keyboard.append(buttons_row)
    logger.debug('Keyboard generated successfully.')
    return InlineKeyboardMarkup(keyboard)

  async def send_to_chat(self, chat_id: int, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Отправляет экран в указанный чат.

    :param chat_id: ID чата, куда нужно отправить экран.
    :param context: Контекст Telegram для выполнения отправки.
    """
    keyboard = self.generate_keyboard(context)
    text = self.resolve_text(self.text)

    try:
      if self.screen_type == ScreenType.NEW:
        await context.bot.send_message(
          chat_id=chat_id,
          text=text,
          reply_markup=keyboard,
          parse_mode='markdown'
        )
      else:
        raise ValueError('Only NEW screen type is supported for send_to_chat.')
    except Exception as e:
      logger.error('Failed to send ActionScreen to chat_id %s: %s', chat_id, e)
      raise