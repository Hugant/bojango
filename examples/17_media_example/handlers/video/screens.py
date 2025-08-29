from bojango.action import ActionScreen, ActionButton
from bojango.core.routing import callback


@callback('s_video_menu')
async def s_video_menu(update, context):
	yield ActionScreen('Меню выбора видео', buttons=[
		[ActionButton('С текстом', action_name='s_video_caption')],
		[ActionButton('Без текста', action_name='s_video')],
		[ActionButton('Назад', action_name='s_start')],
	])


@callback('s_video')
async def s_video(update, context):
	yield ActionScreen(video='media/videos/hb_sinops.mp4', buttons=[
		[ActionButton('Заменить', action_name='s_video_replace')],
		[ActionButton('Назад', action_name='s_video_menu')],
	])

@callback('s_video_replace')
async def s_video_replace(update, context):
	yield ActionScreen(video='media/videos/hb_ticker.mp4', buttons=[
		[ActionButton('Заменить', action_name='s_video')],
		[ActionButton('Назад', action_name='s_video_menu')],
	])


@callback('s_video_caption')
async def s_video_caption(update, context):
	yield ActionScreen('Первое видео', video='media/videos/hb_sinops.mp4', buttons=[
		[ActionButton('Заменить', action_name='s_video_caption_replace')],
		[ActionButton('Назад', action_name='s_video_menu')],
	])

@callback('s_video_caption_replace')
async def s_video_caption_replace(update, context):
	yield ActionScreen('Второе видео', video='media/videos/hb_ticker.mp4', buttons=[
		[ActionButton('Заменить', action_name='s_video_caption')],
		[ActionButton('Назад', action_name='s_video_menu')],
	])