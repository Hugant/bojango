from bojango.action.dispatcher import ActionManager
from bojango.core.routing import command, callback, message, audio
from bojango.action.screen import ActionScreen, ActionButton, ScreenType


# Обработчик команды /start
@command('start')
async def start_command(update, context):
	await ActionManager.redirect('s_screen', update, context)


@callback('s_screen')
async def s_audio(update, context):
	yield ActionScreen('Отправь сообщение')


@message(pattern='.*')
async def m_all(update, context):
	await ActionManager.redirect('s_answer', update, context)


@callback('s_answer')
async def s_audio(update, context):
	yield ActionScreen('А это ответ на твое сообщение', screen_type=ScreenType.REPLY, message_id=update.message.message_id)
