import os
import re
from pathlib import Path
from typing import Any, Union

from telegram import Update, InputFile
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from bojango.action.screen import ActionScreen
from bojango.action.strategies.base import BaseContentStrategy, Transport, MessageKind


_FILE_ID_RE = re.compile(r'^[A-Za-z0-9_-]{20,200}$')  # «похоже на file_id»

def _looks_like_url(s: str) -> bool:
    return s.startswith(('http://', 'https://'))

def _looks_like_path(s: str) -> bool:
    # Быстро: есть разделитель пути ИЛИ расширение ИЛИ Windows-диск
    if ('/' in s) or ('\\' in s):
        return True
    if re.search(r'\.[A-Za-z0-9]{1,5}$', s):  # voice.ogg / img.png / doc.pdf
        return True
    if re.match(r'^[A-Za-z]:\\', s):  # C:\...
        return True
    return False

def _looks_like_file_id(s: str) -> bool:
    # file_id не содержит / \ . и обычно длинный base64url-подобный
    return _FILE_ID_RE.fullmatch(s) is not None

def resolve_media_arg(s: str) -> (str | bytes, str | None):
  if _looks_like_path(s) or os.path.exists(s):
    path = Path(s)
    return path.read_bytes(), path.name

  return s, None


class TextContentStrategy(BaseContentStrategy):
  """
  Стратегия для отображения только текста (с кнопками или без).
  """

  async def prepare(
    self,
    screen: ActionScreen,
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
  ) -> dict:
    return {
      'chat_id': update.effective_chat.id,
      'text': self.format_text(screen.resolve_text(screen.text)),
      'reply_markup': screen.generate_keyboard(context),
      'parse_mode': BaseContentStrategy.get_parse_mode(),
    }

  def get_transport(self, context: ContextTypes.DEFAULT_TYPE) -> Transport:
    return Transport(
      bot=context.bot,
      kind=MessageKind.TEXT,
      chat_action=ChatAction.TYPING,
      api_method_send='send_message',
      api_method_edit='edit_message_text',
      can_edit=True
    )


class ImageContentStrategy(BaseContentStrategy):
  """
  Стратегия для отправки изображения с текстом и клавиатурой.
  """

  async def prepare(
    self,
    screen: ActionScreen,
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
  ) -> dict:
    filedata, filename = resolve_media_arg(screen.image)

    data = {
      'chat_id': update.effective_chat.id,
      'photo': filedata,
      'filename': filename,
      'reply_markup': screen.generate_keyboard(context),
      'parse_mode': BaseContentStrategy.get_parse_mode(),
    }

    if screen.text:
      data['caption'] = self.format_text(screen.resolve_text(screen.text))

    return data

  def get_transport(self, context: ContextTypes.DEFAULT_TYPE) -> Transport:
    return Transport(
      bot=context.bot,
      kind=MessageKind.PHOTO,
      chat_action=ChatAction.TYPING,
      api_method_send='send_photo',
      can_edit=False,
    )


class FileContentStrategy(BaseContentStrategy):
  """
  Стратегия для отправки документа (файла) с текстом и клавиатурой.
  """

  async def prepare(
    self,
    screen: ActionScreen,
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
  ) -> dict:
    filedata, filename = resolve_media_arg(screen.file)

    data = {
      'chat_id': update.effective_chat.id,
      'document': filedata,
      'filename': filename,
      'reply_markup': screen.generate_keyboard(context),
      'parse_mode': BaseContentStrategy.get_parse_mode(),
    }

    if screen.text:
      data['caption'] = self.format_text(screen.resolve_text(screen.text))

    return data

  def get_transport(self, context: ContextTypes.DEFAULT_TYPE) -> Transport:
    return Transport(
      bot=context.bot,
      kind=MessageKind.DOCUMENT,
      chat_action=ChatAction.TYPING,
      api_method_send='send_document',
      can_edit=False,
    )


class VideoContentStrategy(BaseContentStrategy):
  """
  Стратегия для отправки видео с текстом и клавиатурой.
  """

  async def prepare(
    self,
    screen: ActionScreen,
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
  ) -> dict:
    filedata, filename = resolve_media_arg(screen.video)

    data = {
      'chat_id': update.effective_chat.id,
      'video': filedata,
      'filename': filename,
      'reply_markup': screen.generate_keyboard(context),
      'parse_mode': BaseContentStrategy.get_parse_mode(),
    }

    if screen.text:
      data['caption'] = self.format_text(screen.resolve_text(screen.text))

    return data

  def get_transport(self, context: ContextTypes.DEFAULT_TYPE) -> Transport:
    return Transport(
      bot=context.bot,
      kind=MessageKind.VIDEO,
      chat_action=ChatAction.UPLOAD_VIDEO,
      api_method_send='send_video',
      can_edit=False,
    )


class VideoNoteContentStrategy(BaseContentStrategy):
  """
  Стратегия для отправки видео с текстом и клавиатурой.
  """

  async def prepare(
    self,
    screen: ActionScreen,
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
  ) -> dict:
    filedata, filename = resolve_media_arg(screen.video_note)

    data = {
      'chat_id': update.effective_chat.id,
      'video_note': filedata,
      'filename': filename,
      'length': 360
    }

    return data

  def get_transport(self, context: ContextTypes.DEFAULT_TYPE) -> Transport:
    return Transport(
      bot=context.bot,
      kind=MessageKind.VIDEO_NOTE,
      chat_action=ChatAction.RECORD_VIDEO,
      api_method_send='send_video_note',
      can_edit=False,
    )


class VoiceContentStrategy(BaseContentStrategy):
  """
  Стратегия для отправки видео с текстом и клавиатурой.
  """

  async def prepare(
    self,
    screen: ActionScreen,
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
  ) -> dict:
    filedata, filename = resolve_media_arg(screen.voice)

    data = {
      'chat_id': update.effective_chat.id,
      'voice': filedata,
      'filename': filename,
      'reply_markup': screen.generate_keyboard(context),
      'parse_mode': BaseContentStrategy.get_parse_mode(),
    }

    if screen.text:
      data['caption'] = self.format_text(screen.resolve_text(screen.text))

    return data

  def get_transport(self, context: ContextTypes.DEFAULT_TYPE) -> Transport:
    return Transport(
      bot=context.bot,
      kind=MessageKind.VOICE,
      chat_action=ChatAction.RECORD_VOICE,
      api_method_send='send_voice',
      can_edit=False,
    )


class AudioContentStrategy(BaseContentStrategy):
  """
  Стратегия для отправки видео с текстом и клавиатурой.
  """

  async def prepare(
    self,
    screen: ActionScreen,
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
  ) -> dict:
    filedata, filename = resolve_media_arg(screen.audio)

    data = {
      'chat_id': update.effective_chat.id,
      'audio': filedata,
      'filename': filename,
      'reply_markup': screen.generate_keyboard(context),
      'parse_mode': BaseContentStrategy.get_parse_mode(),
    }

    if screen.text:
      data['caption'] = self.format_text(screen.resolve_text(screen.text))

    return data

  def get_transport(self, context: ContextTypes.DEFAULT_TYPE) -> Transport:
    return Transport(
      bot=context.bot,
      kind=MessageKind.VOICE,
      chat_action=ChatAction.UPLOAD_VIDEO,
      api_method_send='send_audio',
      can_edit=False,
    )