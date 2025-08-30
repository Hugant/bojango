import logging.config
import os

from bojango.core.bot import BojangoBotConfig, BojangoBot

from dotenv import load_dotenv

from bojango.utils.format import OpenaiFormatter

load_dotenv()

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
			'level': 'DEBUG',
		},
	},
	'loggers': {
		'': {  # Root logger
			'handlers': ['console'],
			'level': 'DEBUG',
		},
	},
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

config = BojangoBotConfig(
	api_token=os.getenv('YOUR_TELEGRAM_API_TOKEN'),
	formatter=OpenaiFormatter,
	handlers_modules=[
		'handlers'
	]
)

bot = BojangoBot(config)

if __name__ == '__main__':
	bot.run()