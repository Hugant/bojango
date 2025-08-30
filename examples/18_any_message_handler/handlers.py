from bojango.action.dispatcher import ActionManager
from bojango.core.routing import command, callback, message, audio, video_note, any_message
from bojango.action.screen import ActionScreen, ActionButton, ScreenType
from bojango.utils.formatter import TelegramTextFormatter


@command('start')
async def start_command(update, context):
	await ActionManager.redirect('s_screen', update, context)


@callback('s_screen')
async def s_screen(update, context):
	yield ActionScreen('Отправь любое сообщение, можно вместе с вложением')


@any_message()
async def any_message(update, context):
	msg = update.effective_message
	print(1)
	await ActionManager.redirect('s_answer', update, context, chat_id=msg.chat_id, message_id=msg.message_id)


@callback('s_answer')
async def s_answer(update, context, chat_id = None, message_id = None):
	await context.bot.copy_message(
		chat_id=chat_id,
		from_chat_id=chat_id,
		message_id=message_id
	)