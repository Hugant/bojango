from bojango.action.manager import ActionManager
from bojango.action.screen import ActionScreen, ActionButton
from bojango.core.routing import command, callback


# Обработчик команды /start
@command("start")
async def start_command(update, context):
	await ActionManager.redirect('s_start', update, context)


# Стартовый экран
@callback("s_start")
async def s_start(update, context):
	yield ActionScreen(
		text="Добро пожаловать! Выберите действие:",
		buttons=[
			[ActionButton(text="Перейти к акции", action_name="s_promo")],
			[ActionButton(text="О нас", action_name="s_about")]
		]
	)


# Экран о нас
@callback("s_about")
async def s_about(update, context):
	yield ActionScreen(
		text="Мы очень крутая компания",
		buttons=[
			[ActionButton(text="Назад", action_name="s_start")]
		]
	)


# Экран с акцией
@callback("s_promo")
async def s_promo(update, context):
	yield ActionScreen(
		text="🔥 Специальная акция! Нажмите, чтобы проверить подписку.",
		buttons=[
			[ActionButton(text="Проверить подписку", action_name="l_is_channel_subscriber")],
			[ActionButton(text="Назад", action_name="s_start")]
		]
	)


# Проверка подписки и редирект
@callback("l_is_channel_subscriber")
async def check_subscription(update, context):
		user_is_subscribed = True  # Здесь должна быть логика проверки подписки

		if user_is_subscribed:
				await ActionManager.redirect("promo_success", update, context)
		else:
				await ActionManager.redirect("promo_fail", update, context)


# Успешное получение акции
@callback("promo_success")
async def promo_success(update, context):
		yield ActionScreen(
				text="🎉 Поздравляем! Вы подписаны и получаете бонус.",
				buttons=[[ActionButton(text="На главную", action_name="s_start")]]
		)


# Ошибка подписки
@callback("promo_fail")
async def promo_fail(update, context):
		yield ActionScreen(
				text="❌ Вы не подписаны. Подпишитесь на канал и попробуйте снова.",
				buttons=[[ActionButton(text="Назад", action_name="s_promo")]]
		)
