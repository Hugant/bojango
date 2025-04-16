from .base import BaseFormatter, ParseMode
import re


class NoFormatter(BaseFormatter):
  """
    Передает текст как есть
  """
  _parse_mode = ParseMode.MARKDOWN

  def format(self, text: str) -> str:
    return text


class MarkdownFormatter(BaseFormatter):
  """
  Экранирует символы для Markdown V1: _, *, [, ].
  """
  _parse_mode = ParseMode.MARKDOWN

  ESCAPE_CHARS = r'_*\[]'

  def format(self, text: str) -> str:
    return re.sub(f'([{re.escape(self.ESCAPE_CHARS)}])', r'\\\1', text)


class MarkdownV2Formatter(BaseFormatter):
  """
  Экранирует все специальные символы для Markdown V2.
  """
  _parse_mode = ParseMode.MARKDOWNV2

  ESCAPE_CHARS = r'_*\[\]()~`>#+-=|{}.!'

  def format(self, text: str) -> str:
    return re.sub(f'([{re.escape(self.ESCAPE_CHARS)}])', r'\\\1', text)