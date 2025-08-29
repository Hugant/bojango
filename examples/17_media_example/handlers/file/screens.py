from pathlib import Path

from bojango.action import ActionScreen, ActionButton
from bojango.core.routing import callback


@callback('s_file_menu')
async def s_file_menu(update, context):
	yield ActionScreen('Меню выбора файла', buttons=[
		[ActionButton('С текстом', action_name='s_file_caption')],
		[ActionButton('Без текста', action_name='s_file')],
		[ActionButton('Назад', action_name='s_start')],
	])


@callback('s_file')
async def s_file(update, context, file_id: str = None):
	if file_id:
		yield ActionScreen(file=file_id, buttons=[
			[ActionButton('Заменить', action_name='s_file_replace')],
			[ActionButton('Назад', action_name='s_file_menu')],
		])
	else:
		yield ActionScreen(file='media/files/hb_chat.txt', buttons=[
			[ActionButton('Заменить', action_name='s_file_replace')],
			[ActionButton('Назад', action_name='s_file_menu')],
		])

@callback('s_file_replace')
async def s_file_replace(update, context):
	yield ActionScreen(file='media/files/hb_ticker.txt', buttons=[
		[ActionButton('Заменить', action_name='s_file')],
		[ActionButton('Назад', action_name='s_file_menu')],
	])


@callback('s_file_caption')
async def s_file_caption(update, context):
	yield ActionScreen('Первый файл', file='media/files/hb_chat.txt', buttons=[
		[ActionButton('Заменить', action_name='s_file_caption_replace')],
		[ActionButton('Назад', action_name='s_file_menu')],
	])

@callback('s_file_caption_replace')
async def s_file_caption_replace(update, context):
	yield ActionScreen('Второй файл', file='media/files/hb_ticker.txt', buttons=[
		[ActionButton('Заменить', action_name='s_file_caption')],
		[ActionButton('Назад', action_name='s_file_menu')],
	])