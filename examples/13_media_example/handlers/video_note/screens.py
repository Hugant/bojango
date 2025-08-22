from bojango.action import ActionScreen, ActionButton
from bojango.core.routing import callback


@callback('s_video_note_menu')
async def s_video_note_menu(update, context):
	yield ActionScreen('Меню выбора кружков', buttons=[
		[ActionButton('Без текста', action_name='s_video_note')],
		[ActionButton('Назад', action_name='s_start')],
	])


@callback('s_video_note')
async def s_video_note(update, context):
	yield ActionScreen(video_note='media/videos/hb_sinops.mp4')
	yield ActionScreen('Отправка текста после кружка', buttons=[
		[ActionButton('Назад', action_name='s_video_note_menu')],
	])
