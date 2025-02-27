from bojango.core.bot import BojangoBotConfig, BojangoBot

config = BojangoBotConfig(
	api_token='990608607:AAESo023jTDMKDkBHbxpU0DuiXDAsYVx1oE',
	handlers_modules=[
		'handlers'
	]
)

bot = BojangoBot(config)

if __name__ == '__main__':
	bot.run()