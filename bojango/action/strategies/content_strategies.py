from telegram import Update
from telegram.ext import ContextTypes

from bojango.action.screen import ActionScreen
from bojango.action.strategies.base import BaseContentStrategy


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
