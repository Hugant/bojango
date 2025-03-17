import logging
from enum import Enum
from typing import Any
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
  EDIT = 'edit'  # Редактировать сообщение без клавиатуры
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
    text: str | LateValue,
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
    self.text = text
    self.buttons = buttons or []
    self.screen_type = screen_type
    self.message_id = message_id

  def resolve_text(self, text: str | LateValue) -> str:
    """
    Возвращает строку из текста или LateValue.

    :param text: Текстовая строка или объект LateValue.
    :return: Разрешённая строка.
    """
    resolved_text = text.value if isinstance(text, LateValue) else text
    logger.debug(f'Text resolved: {resolved_text}')
    return resolved_text

  async def render(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Отображает экран в зависимости от его типа.

    :param update: Объект Update Telegram.
    :param context: Объект Context Telegram.
    """
    keyboard = self.generate_keyboard(context)
    text = self.resolve_text(self.text)
    query = update.callback_query
    chat_id = update.effective_chat.id

    logger.info(f'Rendering screen: {self.screen_type}, Chat ID: {chat_id}')

    try:
      if self.screen_type == ScreenType.REPLY:
        await context.bot.send_message(
          chat_id=chat_id,
          text=text,
          reply_to_message_id=self.message_id
        )
      elif self.screen_type == ScreenType.NEW:
        await context.bot.send_message(
          chat_id=chat_id,
          text=text,
          reply_markup=keyboard,
          parse_mode='markdown'
        )
      elif self.screen_type == ScreenType.REPLACE and not query:
        await context.bot.send_message(
          chat_id=chat_id,
          text=text,
          reply_markup=keyboard,
          parse_mode='markdown'
        )
      elif self.screen_type == ScreenType.REPLACE and query:
        await context.bot.edit_message_text(
          chat_id=chat_id,
          message_id=query.message.message_id,
          text=text,
          reply_markup=keyboard,
          parse_mode='markdown'
        )
      elif self.screen_type == ScreenType.REMOVE_KEYBOARD and query:
        await context.bot.edit_message_reply_markup(
          chat_id=chat_id,
          message_id=query.message.message_id,
          reply_markup=InlineKeyboardMarkup([])
        )
      elif self.screen_type == ScreenType.EDIT and query:
        await context.bot.edit_message_text(
          chat_id=chat_id,
          message_id=query.message.message_id,
          text=text,
          parse_mode='markdown'
        )
      else:
        logger.error('Unsupported ScreenType or missing query.')
        raise ValueError('Unsupported ScreenType or missing query.')

      if query:
        await query.answer()
    except Exception as e:
      logger.error(f'Screen render error: {e}')
      raise

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
      elif self.screen_type == ScreenType.EDIT:
        raise ValueError('EDIT screen type is not supported in send_to_chat.')
      else:
        raise ValueError('Only NEW screen type is supported for send_to_chat.')
    except Exception as e:
      logger.error('Failed to send ActionScreen to chat_id %s: %s', chat_id, e)
      raise