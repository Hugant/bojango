from abc import abstractmethod, ABC
from typing import Any

from telegram import Update
from telegram.ext import ContextTypes

from bojango.action.screen import ActionScreen
from bojango.utils.format import BaseFormatter, NoFormatter


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
  def get_parse_mode(cls) -> str:
    return cls._formatter.parse_mode

  def format_text(self, text: str) -> str:
    return self._formatter.format(text)

  @staticmethod
  def resolve_strategy(screen: ActionScreen) -> 'BaseContentStrategy':
    from bojango.action.strategies import ImageContentStrategy, FileContentStrategy, TextContentStrategy

    if screen.image:
      return ImageContentStrategy()
    elif screen.file:
      return FileContentStrategy()
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