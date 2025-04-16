import re

from bojango.utils.format import BaseFormatter, MarkdownV2Formatter
from bojango.utils.format.base import ParseMode


class OpenaiFormatter(BaseFormatter):
	"""
		Передает текст как есть
	"""
	_parse_mode = ParseMode.MARKDOWNV2

	RESERVED_CHARS = r'_*\[\]()~`>#+=|{}.!-'

	def format(self, text: str) -> str:
		# Экранируем все специальные символы MarkdownV2
		def escape_md_v2(s: str) -> str:
			return re.sub(r'([_*\[\]()~`>#+\-=|{}.!\\])', r'\\\1', s)

		# 1. Сохраняем кодовые блоки ```
		code_blocks = {}

		def replace_code_block(match):
			key = f"@@CODEBLOCK_{len(code_blocks)}@@"
			code_blocks[key] = f"```{match.group(1)}```"
			return key

		text = re.sub(r"```(.*?)```", replace_code_block, text, flags=re.DOTALL)

		# 2. Сохраняем инлайн-код `...`
		inline_codes = {}

		def replace_inline_code(match):
			key = f"@@INLINE_{len(inline_codes)}@@"
			inline_codes[key] = f"`{match.group(1)}`"
			return key

		text = re.sub(r"`([^`\n]+)`", replace_inline_code, text)

		# 3. Сохраняем ссылки
		links = {}

		def replace_links(match):
			key = f"@@LINK_{len(links)}@@"
			label = escape_md_v2(match.group(1))
			url = match.group(2)
			links[key] = f"[{label}]({url})"
			return key

		text = re.sub(r'\[([^\]]+)]\(([^)]+)\)', replace_links, text)

		# 4. Жирный текст: **text**
		text = re.sub(r'\*\*([^\*]+)\*\*', lambda m: f"*{escape_md_v2(m.group(1))}*", text)

		# 5. Курсив: *text*
		# text = re.sub(r'\*([^\*]+)\*', lambda m: f"_{escape_md_v2(m.group(1))}_", text)

		# 6. Подчёркивание: __text__
		text = re.sub(r'__([^_]+)__', lambda m: f"_{escape_md_v2(m.group(1))}_", text)

		# 7. Перечёркнутый текст: ~~text~~
		text = re.sub(r'~~([^~]+)~~', lambda m: f"~{escape_md_v2(m.group(1))}~", text)

		# 8. Спойлер: ||text||
		text = re.sub(r'\|\|([^|]+)\|\|', lambda m: f"||{escape_md_v2(m.group(1))}||", text)

		# Экранируем оставшийся текст (который вне форматирования)
		# text = escape_md_v2(text)

		# Восстанавливаем вставки
		for key, val in {**code_blocks, **inline_codes, **links}.items():
			text = text.replace(escape_md_v2(key), val)

		print(text)
		return text
