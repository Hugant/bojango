from bojango.action import ActionScreen, ActionButton
from bojango.core.routing import callback


@callback('s_image_menu')
async def s_image_menu(update, context):
	yield ActionScreen('Меню выбора изображения', buttons=[
		[ActionButton('С текстом', action_name='s_image_caption')],
		[ActionButton('Без текста', action_name='s_image')],
		[ActionButton('Назад', action_name='s_start')],
	])


@callback('s_image')
async def s_image(update, context):
	yield ActionScreen(image='media/images/hb_chat.png', buttons=[
		[ActionButton('Заменить', action_name='s_image_replace')],
		[ActionButton('Назад', action_name='s_image_menu')],
	])

@callback('s_image_replace')
async def s_image_replace(update, context):
	yield ActionScreen(image='media/images/hb_ticker.png', buttons=[
		[ActionButton('Заменить', action_name='s_image')],
		[ActionButton('Назад', action_name='s_image_menu')],
	])


@callback('s_image_caption')
async def s_image_caption(update, context):
	yield ActionScreen('Первое изображение', image='media/images/hb_chat.png', buttons=[
		[ActionButton('Заменить', action_name='s_image_caption_replace')],
		[ActionButton('Назад', action_name='s_image_menu')],
	])

@callback('s_image_caption_replace')
async def s_image_caption_replace(update, context):
	yield ActionScreen('Второе изображение', image='media/images/hb_ticker.png', buttons=[
		[ActionButton('Заменить', action_name='s_image_caption')],
		[ActionButton('Назад', action_name='s_image_menu')],
	])