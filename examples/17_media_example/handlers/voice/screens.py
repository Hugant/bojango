from bojango.action import ActionScreen, ActionButton
from bojango.core.routing import callback


@callback('s_voice_menu')
async def s_voice_menu(update, context):
	yield ActionScreen('Меню выбора голосового', buttons=[
		[ActionButton('С текстом', action_name='s_voice_caption')],
		[ActionButton('Без текста', action_name='s_voice')],
		[ActionButton('Назад', action_name='s_start')],
	])


@callback('s_voice')
async def s_voice(update, context):
	yield ActionScreen(voice='media/voices/voice1.ogg', buttons=[
		[ActionButton('Заменить', action_name='s_voice_replace')],
		[ActionButton('Назад', action_name='s_voice_menu')],
	])

@callback('s_voice_replace')
async def s_voice_replace(update, context):
	yield ActionScreen(voice='media/voices/voice2.ogg', buttons=[
		[ActionButton('Заменить', action_name='s_voice')],
		[ActionButton('Назад', action_name='s_voice_menu')],
	])


@callback('s_voice_caption')
async def s_voice_caption(update, context):
	yield ActionScreen('Первое голосовое', voice='media/voices/voice1.ogg', buttons=[
		[ActionButton('Заменить', action_name='s_voice_caption_replace')],
		[ActionButton('Назад', action_name='s_voice_menu')],
	])

@callback('s_voice_caption_replace')
async def s_voice_caption_replace(update, context):
	yield ActionScreen('Второе голосовое', voice='media/voices/voice2.ogg', buttons=[
		[ActionButton('Заменить', action_name='s_voice_caption')],
		[ActionButton('Назад', action_name='s_voice_menu')],
	])