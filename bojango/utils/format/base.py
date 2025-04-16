from abc import abstractmethod, ABC
from enum import Enum


class ParseMode(Enum):
	MARKDOWN = 'Markdown'
	MARKDOWNV2 = 'MarkdownV2'
	HTML = 'html'



class BaseFormatter(ABC):
	_parse_mode: ParseMode = ParseMode.MARKDOWN

	@property
	def parse_mode(self):
		return self._parse_mode.value

	@abstractmethod
	def format(self, text: str) -> str:
		raise NotImplementedError
