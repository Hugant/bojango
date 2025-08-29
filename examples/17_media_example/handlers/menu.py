from bojango.action import ActionScreen, ActionButton, ActionManager
from bojango.core.routing import callback, image, file


@callback('s_start')
async def s_start(update, context):
	yield ActionScreen('Выберите какой контент хотите получить', buttons=[
		[ActionButton('Текст', action_name='s_text')],
		[ActionButton('Изображение', action_name='s_image_menu')],
		[ActionButton('Файл', action_name='s_file_menu')],
		[ActionButton('Видео', action_name='s_video_menu')],
		[ActionButton('Кружок', action_name='s_video_note_menu')],
		[ActionButton('Голосовое', action_name='s_voice_menu')],
		[ActionButton('Аудио', action_name='s_audio_menu')],
	])


@image()
async def image(update, context):
	await ActionManager.redirect('s_image', update, context, file_id=update.message.photo[-1].file_id)


@file()
async def file(update, context):
	await ActionManager.redirect('s_file', update, context, file_id=update.message.document.file_id)