import asyncio
import os

from dotenv import load_dotenv
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from bojango.action import ActionManager
from bojango.core.bot import BojangoBot
from bojango.core.routing import callback
from bojango.action.screen import ActionScreen

load_dotenv()

@callback('s_start')
async def s_start(update, context):
	bot = BojangoBot.get_instance()
	await bot.send_message(int(os.getenv('TEST_CHAT_ID')), 'Сообщение с кнопкой от ptb', reply_markup=InlineKeyboardMarkup(
		[
			[InlineKeyboardButton(text='Следующий шаг', callback_data='s_second')]
		]
	))


@callback('s_second')
async def s_second(update, context):
	await ActionManager.redirect('s_third', update, context)


@callback('s_third')
async def s_third(update, context):
	await ActionManager.redirect('s_fourth', update, context)


@callback('s_fourth')
async def s_fourth(update, context):
	yield ActionScreen(text='Okay, im ready')


