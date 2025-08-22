from bojango.action import ActionScreen, ActionButton
from bojango.core.routing import callback


@callback('s_text')
async def s_text(update, context):
	yield ActionScreen('Первое текстовое сообщение', buttons=[
		[ActionButton('Заменить', action_name='s_text_replace')],
		[ActionButton('Назад', action_name='s_start')],
	])

@callback('s_text_replace')
async def s_text(update, context):
	yield ActionScreen('Второе текстовое сообщение', buttons=[
		[ActionButton('Заменить', action_name='s_text')],
		[ActionButton('Назад', action_name='s_start')],
	])