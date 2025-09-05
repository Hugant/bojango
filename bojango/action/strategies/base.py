from abc import abstractmethod, ABC
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

from telegram import Update, Bot
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from bojango.action.screen import ActionScreen
from bojango.utils.format import BaseFormatter, NoFormatter


class MessageKind(str, Enum):
  TEXT = 'text'
  PHOTO = 'photo'
  DOCUMENT = 'document'
  VIDEO = 'video'
  VIDEO_NOTE = 'video_note'
  VOICE = 'voice'
  AUDIO = 'audio'


@dataclass(slots=True)
class Transport(ABC):
  bot: Bot
  kind: MessageKind
  chat_action: ChatAction
  api_method_send: str
  api_method_edit: Optional[str] = None
  can_edit: bool = False

  @staticmethod
  def detect_message_kind(message) -> MessageKind:
    if message.photo:    return MessageKind.PHOTO
    if message.document: return MessageKind.DOCUMENT

    return MessageKind.TEXT

  async def _call(self, method_name: str, **kwargs: Any) -> Any:
    method = getattr(self.bot, method_name, None)
    if not callable(method):
      raise AttributeError(f'Bot has no callable method {method_name!r}')
    return await method(**kwargs)

  async def _with_action(self, chat_id: int, coro) -> Any:
    try:
      await self.bot.send_chat_action(chat_id=chat_id, action=self.chat_action)
    except Exception:
      pass
    return await coro

  async def send(self, **data: Any) -> None:
    chat_id = data.setdefault('chat_id', data.get('chat_id'))
    if chat_id is None:
      raise ValueError('chat_id has not provided')

    await self._with_action(chat_id, self._call(self.api_method_send, **data))

  async def edit(self, *, data: dict[str, Any], message_id: int, chat_id: Optional[int], legitimate: Optional[bool]) -> bool:
    if self.can_edit and legitimate:
      if not self.api_method_edit:
        raise ValueError('api_method_edit has not provided')
      try:
        kwargs = dict(data)
        kwargs['message_id'] = message_id
        if chat_id is not None:
          kwargs['chat_id'] = chat_id
        await self._with_action(chat_id or data['chat_id'], self._call(self.api_method_edit, **kwargs))
      except Exception:
        try:
          await self._call('delete_message', chat_id=chat_id, message_id=message_id)
        except Exception:
          pass
        await self._with_action(chat_id, self._call(self.api_method_send, **data))
    else:
      try:
        await self._call('delete_message', chat_id=chat_id, message_id=message_id)
      except Exception:
        pass
      await self._with_action(chat_id, self._call(self.api_method_send, **data))

  async def delete(self, *, chat_id: int, message_id: int) -> None:
    await self._call('delete_message', chat_id=chat_id, message_id=message_id)

  async def remove_keyboard(self, *, chat_id: int, message_id: int) -> None:
    """
    Снимает клавиатуру у существующего сообщения.
    Для текста — edit_message_reply_markup; для медиа — тоже edit_message_reply_markup.
    """
    try:
      await self._call('edit_message_reply_markup', chat_id=chat_id, message_id=message_id, reply_markup=None)
    except Exception:
      # допустимо молча проигнорировать — Telegram может не позволить
      pass


class BaseContentStrategy(ABC):
  """
  Абстрактный класс стратегии генерации содержимого сообщения.
  Каждая стратегия отвечает за подготовку параметров,
  которые затем будут переданы в метод Telegram API (send_message, send_photo и т.д.).
  """
  _formatter: BaseFormatter = NoFormatter()

  @classmethod
  def set_formatter(cls, formatter: BaseFormatter):
    cls._formatter = formatter

  @classmethod
  def get_formatter(cls, formatter: BaseFormatter):
    cls._formatter = formatter

  @classmethod
  def get_parse_mode(cls) -> str:
    return cls._formatter.parse_mode

  def format_text(self, text: str) -> str:
    return self._formatter.format(text)

  @staticmethod
  def resolve_strategy(screen: ActionScreen) -> 'BaseContentStrategy':
    from bojango.action.strategies import (
      ImageContentStrategy, FileContentStrategy, TextContentStrategy, VideoContentStrategy, VideoNoteContentStrategy,
      VoiceContentStrategy, AudioContentStrategy)

    if screen.formatter:
      BaseContentStrategy.set_formatter(screen.formatter) # TODO: check problems

    if screen.image:
      return ImageContentStrategy()
    elif screen.file:
      return FileContentStrategy()
    elif screen.video:
      return VideoContentStrategy()
    elif screen.video_note:
      return VideoNoteContentStrategy()
    elif screen.voice:
      return VoiceContentStrategy()
    elif screen.audio:
      return AudioContentStrategy()
    elif screen.text or (screen.text is not None and screen.text == ''):
      return TextContentStrategy()
    else:
      raise ValueError(f'No content strategy for this situation')

  @abstractmethod
  async def prepare(
    self,
    screen: ActionScreen,
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
  ) -> dict[str, Any]:
    """
    Подготавливает данные для отправки сообщения.

    :param screen: Объект ActionScreen с параметрами.
    :param update: Telegram Update.
    :param context: Контекст Telegram.
    :return: Словарь с параметрами для отправки (text, photo, file, reply_markup и т.д.)
    """
    pass

  @abstractmethod
  def get_transport(self, context: ContextTypes.DEFAULT_TYPE) -> Transport:
    """

		"""
    pass