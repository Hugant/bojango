import re

from bojango.utils.format import BaseFormatter, MarkdownV2Formatter
from bojango.utils.format.base import ParseMode


class OpenaiFormatter(BaseFormatter):
	"""
		Передает текст как есть
	"""
	_parse_mode = ParseMode.MARKDOWNV2

	RESERVED_CHARS = r'_\[\]()+=|{}.!-~'
	# RESERVED_CHARS = r'_*\[\]()~`>#+=|{}.!-'

	def format(self, text: str) -> str:
		def link_replacer(match):
			key = f"@@LINK{len(links)}@@"
			links[key] = match.group(0)
			return key


		text = re.sub(r'(?<!\*)\*(?!\*)', '@@STAR@@', text)
		text = re.sub(r'\*\*(.+?)\*\*', r'@@BOLD@@\1@@BOLD@@', text)
		text = re.sub(r'(?<!\*)\*(?!\*)', '@@STAR@@', text)

		links = {}
		text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link_replacer, text)

		text = re.sub(f'([{re.escape(OpenaiFormatter.RESERVED_CHARS)}])', r'\\\1', text)

		for key, original in links.items():
			text = text.replace(key, original)

		text = text.replace('#', '')
		text = text.replace('@@STAR@@', '\*')
		text = text.replace('@@BOLD@@', '*')

		return text
