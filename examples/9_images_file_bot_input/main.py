import os
import sys
import asyncio
import logging.config

from bojango.utils.format import OpenaiFormatter
from bojango.core.bot import BojangoBot, BojangoBotConfig
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '%(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'detailed',
            'level': 'INFO',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level':  'DEBUG',
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


config = BojangoBotConfig(
    api_token=os.getenv('YOUR_TELEGRAM_API_TOKEN'),
    formatter=OpenaiFormatter,
    handlers_modules=[
        'handlers.commands',
        'handlers.messages',
        'handlers.callback.screens',
        'handlers.callback.logical'
    ]
)


async def main():
    logger.info("Инициализация бота")
    bot = BojangoBot(config)
    logger.info("Инициализация бота успешно завершена")
    try:
        logger.info('Запуск бота...')
        await bot.start()
        logger.info('Ожидаем сообщение от пользователя...')
    finally:
        await bot.stop()
        logger.info("Бот остановлен")


if __name__ == "__main__":
    asyncio.run(main())
    