from bojango.action import ActionScreen, ActionButton
from bojango.core.routing import callback


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
