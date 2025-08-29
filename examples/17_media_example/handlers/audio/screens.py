from bojango.action import ActionScreen, ActionButton
from bojango.core.routing import callback


@callback('s_audio_menu')
async def s_audio_menu(update, context):
	yield ActionScreen('Меню выбора файла', buttons=[
		[ActionButton('С текстом', action_name='s_audio_caption')],
		[ActionButton('Без текста', action_name='s_audio')],
		[ActionButton('Назад', action_name='s_start')],
	])


@callback('s_audio')
async def s_audio(update, context):
	yield ActionScreen(audio='media/voices/voice1.ogg', buttons=[
		[ActionButton('Заменить', action_name='s_audio_replace')],
		[ActionButton('Назад', action_name='s_audio_menu')],
	])

@callback('s_audio_replace')
async def s_audio_replace(update, context):
	yield ActionScreen(audio='media/voices/voice2.ogg', buttons=[
		[ActionButton('Заменить', action_name='s_audio')],
		[ActionButton('Назад', action_name='s_audio_menu')],
	])


@callback('s_audio_caption')
async def s_audio_caption(update, context):
	yield ActionScreen('Первое аудио', audio='media/voices/voice1.ogg', buttons=[
		[ActionButton('Заменить', action_name='s_audio_caption_replace')],
		[ActionButton('Назад', action_name='s_audio_menu')],
	])

@callback('s_audio_caption_replace')
async def s_audio_caption_replace(update, context):
	yield ActionScreen('Второе аудио', audio='media/voices/voice2.ogg', buttons=[
		[ActionButton('Заменить', action_name='s_audio_caption')],
		[ActionButton('Назад', action_name='s_audio_menu')],
	])