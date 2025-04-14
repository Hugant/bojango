from bojango.action.manager import ActionManager
from bojango.core.routing import command, callback, message, audio, video_note
from bojango.action.screen import ActionScreen, ActionButton, ScreenType
from bojango.utils.format import TelegramTextFormatter


# Обработчик команды /start
@command('start')
async def start_command(update, context):
	await ActionManager.redirect('s_screen', update, context)


@callback('s_screen')
async def s_audio(update, context):
	tf = TelegramTextFormatter()

