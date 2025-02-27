from bojango.action.manager import ActionManager
from bojango.core.routing import command, callback, message
from bojango.action.screen import ActionScreen, ActionButton, ScreenType


# Обработчик команды /start
@command('start')
async def start_command(update, context):
	await ActionManager.redirect('start_screen', update, context)


# Callback 'Приветственного экрана'
@callback('start_screen')
async def start_screen_callback(update, context, args):
	yield ActionScreen(
		text='Добро пожаловать! Выберите действие:',
		buttons=[
			[ActionButton(text='Далее', action_name='next_step')],
			[ActionButton(text='О нас', action_name='about')]
		]
	)


# Callback для кнопки 'Далее'
@callback('next_step')
async def next_step_callback(update, context, args):
	yield ActionScreen(
		text='Вы перешли на следующий шаг!',
		buttons=[[ActionButton(text='Назад', action_name='start_screen')]]
	)


# Callback для кнопки 'О нас'
@callback('about')
async def about_callback(update, context, args):
	yield ActionScreen(
		text='Этот бот создан на Bojango!',
		buttons=[[ActionButton(text='Назад', action_name='start_screen')]]
	)


# Обработчик текстовых сообщений (фильтрация номеров телефона)
@message(pattern=r'^\d{10}$')
async def phone_number_handler(update, context):
	await ActionManager.redirect('about', update, context)
	# yield ActionScreen(
	# 	text='Вы отправили номер телефона!',
	# 	buttons=[[ActionButton(text='Ок', action_name='start')]]
	# )