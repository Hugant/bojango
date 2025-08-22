from bojango.core.routing import command
from bojango.action import ActionManager


@command('start')
async def start(update, context):
	await ActionManager.redirect('s_start', update, context)


@command('send_text')
async def send_text(update, context):
	await ActionManager.redirect('s_text', update, context)


@command('send_image')
async def send_image(update, context):
	await ActionManager.redirect('s_image', update, context)


@command('send_file')
async def send_file(update, context):
	await ActionManager.redirect('s_file', update, context)


@command('send_video')
async def send_video(update, context):
	await ActionManager.redirect('s_video', update, context)


@command('send_video_note')
async def send_video_note(update, context):
	await ActionManager.redirect('s_video_note', update, context)


@command('send_voice')
async def send_voice(update, context):
	await ActionManager.redirect('s_voice', update, context)


@command('send_audio')
async def send_audio(update, context):
	await ActionManager.redirect('s_audio', update, context)