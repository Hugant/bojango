from telegram import Update

from bojango.action import ActionScreen, ActionManager
from bojango.core.routing import message, command, callback, audio, voice, image, video_note, file, video


@command('start')
async def start(update, context):
	yield ActionScreen('Отправьте мне какой-нибудь медиа файл, аудио, кружок или текст')


@message()
async def message(update, context):
	await ActionManager.redirect('message_screen', update, context)

@callback('message_screen')
async def message_screen(update, context):
	yield ActionScreen(f'Вы отправили сообщение с содержанием: {update.message.text}')


@audio()
async def audio(update, context):
	await ActionManager.redirect('audio_screen', update, context)

@callback('audio_screen')
async def audio_screen(update: Update, context):
	yield ActionScreen(f'Вы отправили сообщение с аудио')


@voice()
async def voice(update, context):
	await ActionManager.redirect('voice_screen', update, context)

@callback('voice_screen')
async def voice_screen(update: Update, context):
	yield ActionScreen(f'Вы отправили голосовое сообщение')
	
	
@image()
async def image(update, context):
	await ActionManager.redirect('image_screen', update, context)

@callback('image_screen')
async def image_screen(update: Update, context):
	yield ActionScreen(f'Вы отправили изображение')


@video_note()
async def video_note(update, context):
	await ActionManager.redirect('video_note_screen', update, context)

@callback('video_note_screen')
async def video_note_screen(update: Update, context):
	yield ActionScreen(f'Вы отправили кружок')
	

@video()
async def video(update, context):
	await ActionManager.redirect('video_screen', update, context)

@callback('video_screen')
async def video_screen(update: Update, context):
	yield ActionScreen(f'Вы отправили видео')


@file()
async def file(update, context):
	await ActionManager.redirect('file_screen', update, context)

@callback('file_screen')
async def file_screen(update: Update, context):
	yield ActionScreen(f'Вы отправили файл')
	
	

