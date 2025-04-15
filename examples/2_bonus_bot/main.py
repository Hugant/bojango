import os

from dotenv import load_dotenv

from bojango.core.bot import BojangoBotConfig, BojangoBot

load_dotenv()

config = BojangoBotConfig(
	api_token=os.getenv('YOUR_TELEGRAM_API_TOKEN'),
	handlers_modules=[
		'handlers'
	]
)

bot = BojangoBot(config)

if __name__ == '__main__':
	bot.run()