from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from bojango.action.screen import ActionScreen


class BaseContentStrategy(ABC):
  """
  Абстрактный класс стратегии генерации содержимого сообщения.
  Каждая стратегия отвечает за подготовку параметров,
  которые затем будут переданы в метод Telegram API (send_message, send_photo и т.д.).
  """

  PARSE_MODE = 'markdown'

  @staticmethod
  def resolve_strategy(screen: ActionScreen) -> 'BaseContentStrategy':
    if screen.image:
      return ImageContentStrategy()
    elif screen.file:
      return FileContentStrategy()
    elif screen.text:
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
      'text': screen.resolve_text(screen.text),
      'reply_markup': screen.generate_keyboard(context),
      'parse_mode': BaseContentStrategy.PARSE_MODE,
    }


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
      'parse_mode': self.PARSE_MODE,
    }

    if screen.text:
      data['caption'] = screen.resolve_text(screen.text)

    return data


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
      'parse_mode': self.PARSE_MODE,
    }

    if screen.text:
      data['caption'] = screen.resolve_text(screen.text)

    return data