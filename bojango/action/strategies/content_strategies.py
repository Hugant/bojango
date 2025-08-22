from typing import Any

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from bojango.action.screen import ActionScreen
from bojango.action.strategies.base import BaseContentStrategy, Transport, MessageKind


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
    if isinstance(screen.image, str):
      photo = open(screen.image, 'rb')
    else:
      photo = screen.image

    data = {
      'chat_id': update.effective_chat.id,
      'photo': photo,
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
    if isinstance(screen.file, str):
      document = open(screen.file, 'rb')
    else:
      document = screen.file

    data = {
      'chat_id': update.effective_chat.id,
      'document': document,
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
    if isinstance(screen.video, str):
      video = open(screen.video, 'rb')
    else:
      video = screen.video

    data = {
      'chat_id': update.effective_chat.id,
      'video': video,
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
    if isinstance(screen.video_note, str):
      video_note = open(screen.video_note, 'rb')
    else:
      video_note = screen.video_note

    data = {
      'chat_id': update.effective_chat.id,
      'video_note': video_note,
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
    if isinstance(screen.voice, str):
      voice = open(screen.voice, 'rb')
    else:
      voice = screen.video

    data = {
      'chat_id': update.effective_chat.id,
      'voice': voice,
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
    if isinstance(screen.audio, str):
      audio = open(screen.audio, 'rb')
    else:
      audio = screen.video

    data = {
      'chat_id': update.effective_chat.id,
      'audio': audio,
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