import os
from datetime import datetime, timezone, timedelta
from bojango.action import ActionScreen, ActionManager, ActionButton
from bojango.core.routing import command, join_request, callback


@command('start')
async def start(update, context):
	await ActionManager.redirect('s_start', update, context)


@join_request()
async def join_request(update, context):
	req = update.chat_join_request
	await context.bot.approve_chat_join_request(chat_id=req.chat.id, user_id=req.from_user.id)


@callback('s_start')
async def s_start(update, context):
	expire = datetime.now(timezone.utc) + timedelta(hours=2)

	channel_link = await context.bot.create_chat_invite_link(
		chat_id=os.getenv('CHANNEL_ID'),
		creates_join_request=True,
		expire_date=int(expire.timestamp()),
		name='auto-approve',
	)

	chat_link = await context.bot.create_chat_invite_link(
		chat_id=os.getenv('CHAT_ID'),
		creates_join_request=True,
		expire_date=int(expire.timestamp()),
		name='auto-approve',
	)

	yield ActionScreen('Попробуйте войти в канал и чат для проверки автоджоина', buttons=[
		[ActionButton('Ссылка на канал', url=channel_link.invite_link)],
		[ActionButton('Ссылка на чат', url=chat_link.invite_link)],
	])
