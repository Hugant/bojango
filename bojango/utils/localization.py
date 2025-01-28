from typing import Any, Self
import gettext
from abc import ABC, abstractmethod
import logging

# Logger initialization
logger = logging.getLogger(__name__)


class BaseLocalizer(ABC):
  """Абстрактный класс для локализаторов."""

  @abstractmethod
  def translate(self, key: str, **kwargs) -> str:
    """
    Метод перевода текста. Должен быть реализован в наследниках.

    :param key: Ключ для перевода (msgid или строка).
    :param kwargs: Дополнительные параметры для перевода.
    :return: Переведённый текст.
    """
    pass


class LocalizationFileNotFoundError(Exception):
  """Исключение, возникающее при отсутствии файла перевода."""

  def __init__(self, language: str):
    super().__init__(f'Translation file for language "{language}" not found.')


class TranslationKeyNotFoundError(Exception):
  """Исключение, возникающее при отсутствии ключа перевода."""

  def __init__(self, key: str):
    super().__init__(f'Translation key "{key}" not found.')


class LocalizationManager(BaseLocalizer):
  """Локализация через gettext."""

  _instance: Self | None = None

  def __new__(cls, locales_dir: str, default_language: str = 'ru') -> Self:
    if cls._instance is None:
      cls._instance = super().__new__(cls)
      cls._instance.__initialized = False
    return cls._instance

  def __init__(self, locales_dir: str, default_language: str = 'ru'):
    if self.__initialized:
      return
    self.locales_dir = locales_dir
    self.default_language = default_language
    self.translations = {}
    self.__initialized = True
    logger.info('LocalizationManager initialized with default language: %s', default_language)

  @classmethod
  def get_instance(cls) -> Self:
    """Возвращает единственный экземпляр LocalizationManager."""
    if cls._instance is None:
      raise ValueError('LocalizationManager не инициализирован. Создайте его экземпляр перед использованием.')
    return cls._instance

  def set_language(self, language: str) -> None:
    """
    Устанавливает текущий язык.

    :param language: Код языка (например, 'ru', 'en').
    """
    self.default_language = language
    logger.info('Language set to: %s', language)

  def get_translation(self, language: str | None = None) -> gettext.GNUTranslations:
    """
    Возвращает объект перевода для указанного языка.

    :param language: Код языка. Если не указан, используется язык по умолчанию.
    :return: Объект перевода.
    :raises LocalizationFileNotFoundError: Если файл перевода отсутствует.
    """
    language = language or self.default_language

    if language not in self.translations:
      try:
        self.translations[language] = gettext.translation(
          'messages',
          localedir=self.locales_dir,
          languages=[language],
        )
        logger.info('Translation for language "%s" loaded successfully.', language)
      except FileNotFoundError:
        logger.error('Translation file for language "%s" not found.', language)
        raise LocalizationFileNotFoundError(language)

    return self.translations[language]

  def translate(self, key: str, **kwargs) -> str:
    """
    Переводит текст на текущий установленный язык.

    :param key: Ключ перевода.
    :param kwargs: Дополнительные параметры перевода.
    :return: Переведённый текст.
    :raises TranslationKeyNotFoundError: Если ключ перевода отсутствует.
    """
    translation = self.get_translation()
    try:
      translated_text = translation.gettext(key)
      if translated_text == key:  # Если gettext вернул сам ключ (ключ не найден)
        raise KeyError
      logger.debug('Translating key "%s": %s', key, translated_text)
      return translated_text
    except KeyError:
      logger.error('Translation key "%s" not found. Returning the key as fallback.', key)
      raise TranslationKeyNotFoundError(key)


class LateValue:
  """Класс для отложенного вычисления значения."""

  def __init__(self, key: str, **kwargs: Any) -> None:
    """
    :param key: Ключ для перевода.
    :param kwargs: Дополнительные параметры для перевода.
    """
    self.key = key
    self.kwargs = kwargs

  @property
  def value(self) -> str:
    """Выполняет перевод с использованием глобального локализатора."""
    localizer = LocalizationManager.get_instance()
    translated_text = localizer.translate(self.key)

    if '__value' not in self.kwargs:
      return translated_text % self.kwargs
    else:
      return translated_text % self.kwargs['__value']

  def __mod__(self, other: Any) -> 'LateValue':
    """
    Поддержка оператора `%` для подстановки.

    :param other: Данные для форматирования строки.
    :return: Новый LateValue с обновлёнными параметрами.
    """
    if isinstance(other, dict):
      formatted_kwargs = {**self.kwargs, **other}
      return LateValue(self.key, **formatted_kwargs)
    else:
      formatted_kwargs = {**self.kwargs, '__value': other}
      return LateValue(self.key, **formatted_kwargs)

  def __str__(self) -> str:
    """Автоматически возвращает результат перевода."""
    return self.value




