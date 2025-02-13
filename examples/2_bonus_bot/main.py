from bojango.core.bot import BojangoBotConfig, BojangoBot

config = BojangoBotConfig(
	api_token='YOUR_TELEGRAM_API_TOKEN',
	handlers_modules=[
		'handlers'
	]
)

bot = BojangoBot(config)

if __name__ == '__main__':
	bot.run()