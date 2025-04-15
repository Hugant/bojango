from bojango.action.manager import ActionManager
from bojango.core.routing import command, callback, message, audio, video_note
from bojango.action.screen import ActionScreen, ActionButton, ScreenType
from bojango.utils.format import TelegramTextFormatter


@command('start')
async def start_command(update, context):
	await ActionManager.redirect('s_menu', update, context)


@callback('s_menu')
async def s_menu(update, context):
	yield ActionScreen(
		text='Привет, это небольшой гайд по работе с изображениями и файлами в bojango. Что хочешь посмотреть?',
		buttons=[
			[ActionButton('Изображение', action_name='s_image_menu')],
			[ActionButton('Файл', action_name='s_file_menu')],
		]
	)


@callback('s_image_menu')
async def s_image_menu(update, context):
	yield ActionScreen(text='Выберите тип сообщения', buttons=[
		[ActionButton('Просто изображение', action_name='s_image')],
		[ActionButton('Изображение с текстом', action_name='s_image_with_text')],
		[ActionButton('Изображение ответом на сообщение', action_name='s_image_with_reply')],
		[ActionButton('Главное меню', action_name='s_menu')],
	])


@callback('s_image')
async def s_image(update, context):
	yield ActionScreen(
		image='images/hb_chat.png',
		buttons=[
			[ActionButton('Назад', action_name='s_image_menu')],
		]
	)


@callback('s_image_with_text')
async def s_image_with_text(update, context):
	yield ActionScreen(
		text='Изображение с текстом',
		image='images/hb_ticker.png',
		buttons=[
			[ActionButton('Назад', action_name='s_image_menu')],
		]
	)


@callback('s_image_with_reply')
async def s_image_with_reply(update, context):
	yield ActionScreen(text='Отправьте сообщение "Изображение"')


@message(pattern=r'\bИзображение\b')
async def m_image(update, context):
	await ActionManager.redirect('s_image_with_reply_answer', update, context)


@callback('s_image_with_reply_answer')
async def s_image_with_reply_answer(update, context):
	yield ActionScreen(
		image='images/hb_sinops.png',
		screen_type=ScreenType.REPLY,
		message_id=update.message.message_id,
		buttons=[
			[ActionButton('Меню изображений', action_name='s_image_menu')],
			[ActionButton('Главное меню', action_name='s_menu')],
		]
	)


@callback('s_file_menu')
async def s_file_menu(update, context):
	yield ActionScreen(
		text='Выберите тип сообщения',
		buttons=[
			[ActionButton('Просто файл', action_name='s_file')],
			[ActionButton('Файл с текстом', action_name='s_file_with_text')],
			[ActionButton('Изображение ответом на сообщение', action_name='s_image_with_reply')],
		]
	)


@callback('s_file')
async def s_file(update, context):
	yield ActionScreen(
		file='files/hb_chat.txt',
		buttons=[
			[ActionButton('Назад', action_name='s_file_menu')],
		]
	)


@callback('s_file_with_text')
async def s_file_with_text(update, context):
	yield ActionScreen(
		text='Изображение с текстом',
		file='files/hb_ticker.txt',
		buttons=[
			[ActionButton('Назад', action_name='s_file_menu')],
		]
	)


@callback('s_file_with_reply')
async def s_file_with_reply(update, context):
	yield ActionScreen(text='Отправьте сообщение "Файл"')


@message(pattern=r'\bФайл\b')
async def m_file(update, context):
	await ActionManager.redirect('s_file_with_reply_answer', update, context)


@callback('s_file_with_reply_answer')
async def s_file_with_reply_answer(update, context):
	yield ActionScreen(
		file='files/hb_sinops.txt',
		screen_type=ScreenType.REPLY,
		message_id=update.message.message_id,
		buttons=[
			[ActionButton('Меню файлов', action_name='s_file_menu')],
			[ActionButton('Главное меню', action_name='s_menu')],
		]
	)