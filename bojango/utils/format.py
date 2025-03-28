import re
import logging
from typing import List, Tuple


class TelegramTextFormatter:
	def __init__(self):
		self._literals: List[Tuple[str, str]] = []
		self._ignores: List[str] = []
		self._ignore_patterns: List[str] = []
		self._pre_replace: List[Tuple[str, str]] = []
		self._post_replace: List[Tuple[str, str]] = []
		self.logger = logging.getLogger('TelegramTextFormatter')

	def add_literal(self, open_literal: str, close_literal: str) -> None:
		"""Добавляет пару литералов."""
		self._literals.append((open_literal, close_literal))
		self.logger.debug('Added literal: (%s, %s)', open_literal, close_literal)

	def add_ignore(self, ignore: str) -> None:
		"""Добавляет строку для игнорирования."""
		self._ignores.append(ignore)
		self.logger.debug('Added ignore string: %s', ignore)

	def add_ignore_pattern(self, pattern: str) -> None:
		"""Добавляет регулярное выражение для игнорирования."""
		self._ignore_patterns.append(pattern)
		self.logger.debug('Added ignore pattern: %s', pattern)

	def add_pre_replace(self, old: str, new: str) -> None:
		"""Добавляет замену перед форматированием."""
		self._pre_replace.append((old, new))
		self.logger.debug('Added pre-replace: %s -> %s', old, new)

	def add_post_replace(self, old: str, new: str) -> None:
		"""Добавляет замену после форматирования."""
		self._post_replace.append((old, new))
		self.logger.debug('Added post-replace: %s -> %s', old, new)

	def _apply_replacements(self, text: str, replacements: List[Tuple[str, str]]) -> str:
		"""Применяет замены к тексту."""
		for old, new in replacements:
			text = re.sub(old, new, text)
		return text

	def _balance_literals(self, text: str) -> str:
		"""Проверяет сбалансированность литералов и добавляет недостающие."""
		for open_literal, close_literal in self._literals:
			amount_open = text.count(open_literal)
			amount_close = text.count(close_literal)
			if open_literal == close_literal:
				if amount_open % 2 != 0:
					text += close_literal
					self.logger.warning('Unbalanced literal: %s -> Adding closing literal %s', open_literal, close_literal)
			elif amount_open != amount_close:
				text += close_literal
				self.logger.warning('Unbalanced literal: %s -> Adding closing literal %s', open_literal, close_literal)

		return text

	def format(self, text: str) -> str:
		"""
		Форматирует текст, применяя все правила:
		1. Предварительные замены.
		2. Балансировка литералов.
		3. Игнорирование строк.
		4. Пост-замены.
		"""
		self.logger.debug('Formatting text: %s', text)
		text = self._apply_replacements(text, self._pre_replace)
		text = self._balance_literals(text)

		for ignore in self._ignores:
			text = text.replace(ignore, '')

		for pattern in self._ignore_patterns:
			text = re.sub(pattern, '', text)

		text = self._apply_replacements(text, self._post_replace)
		self.logger.debug('Formatted text: %s', text)
		return text.strip()
