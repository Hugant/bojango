import urllib.parse
from typing import Any, Dict, Tuple
import logging


logger = logging.getLogger(__name__)

def encode_callback_data(action_name: str, args: Dict[str, Any] | None = None) -> str:
  """
  Кодирует имя действия и аргументы в callback_data.

  :param action_name: Имя действия, которое будет использоваться в callback_data.
  :param args: Словарь аргументов, которые нужно закодировать.
  :return: Строка с закодированными данными.
  """
  logger.debug(f'Encoding callback data for action "{action_name}" with args: {args}')
  if args:
    encoded_args = urllib.parse.urlencode(args)
    callback_data = f'{action_name}?{encoded_args}'
  else:
    callback_data = action_name
  logger.debug(f'Encoded callback data: {callback_data}')
  return callback_data


def decode_callback_data(callback_data: str) -> Tuple[str, Dict[str, Any] | None]:
  """
  Декодирует callback_data в имя действия и аргументы.

  :param callback_data: Строка callback_data, содержащая имя действия и аргументы.
  :return: Кортеж из имени действия и словаря аргументов.
  """
  logger.debug(f'Decoding callback data: {callback_data}')
  if '?' in callback_data:
    action_name, query_string = callback_data.split('?', 1)
    args = dict(urllib.parse.parse_qsl(query_string))
    logger.debug(f'Decoded action name: "{action_name}", args: {args}')
    return action_name, args

  logger.debug(f'Decoded action name: "{callback_data}", no args found.')
  return callback_data, None
