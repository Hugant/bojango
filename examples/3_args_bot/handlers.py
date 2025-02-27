from bojango.action.manager import ActionManager
from bojango.core.routing import command, callback, message
from bojango.action.screen import ActionScreen, ActionButton, ScreenType


# Обработчик команды /start
@command('start')
async def start_command(update, context):
	await ActionManager.redirect('start_screen', update, context)


# Callback 'Приветственного экрана'
@callback('start_screen')
async def start_screen_callback(update, context):
	yield ActionScreen(
		text='Добро пожаловать! Выберите действие:',
		buttons=[
			[ActionButton(text='Далее', action_name='next_step', step_name='Далее')],
			[ActionButton(text='О нас', action_name='next_step', step_name='О нас')]
		]
	)


@callback('next_step')
async def next_step_callback(update, context, step_name='Безшаговый'):
	yield ActionScreen(
		text=f'Вы выбрали шаг {step_name}',
		buttons=[
			[ActionButton(text='Далее', action_name='2step', name='Валера', age=13)]
		]
	)


@callback('2step')
async def step2_callback(update, context, name, age):
	yield ActionScreen(
		text=f'Вы выбрали шаг {name} {age}',
		buttons=[
			[ActionButton(text='Назад', action_name='next_step')],
			[ActionButton(text='На главную', action_name='start_screen')]
		]
	)


	# TODO: Выводить ошибку что callback большой
	# TODO: Решить проблему с вызовом одинаковых экранов в одной группе кнопок