from bojango.action.dispatcher import ActionManager
from bojango.core.routing import command, callback, message, audio
from bojango.action.screen import ActionScreen, ActionButton, ScreenType


# Обработчик команды /start
@command('start')
async def start_command(update, context):
	await ActionManager.redirect('s_screen', update, context)


@audio()
async def a_audio(update, context):
	await ActionManager.redirect('s_audio', update, context)


@callback('s_screen')
async def s_audio(update, context):
	yield ActionScreen('Отправь аудио-сообщение')


@callback('s_audio')
async def s_audio(update, context):
	yield ActionScreen('Ты отправил аудио-сообщение')
