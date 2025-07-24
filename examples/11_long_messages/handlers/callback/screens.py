import asyncio

from bojango.action import ActionManager
from bojango.core.routing import callback
from bojango.action.screen import ActionScreen
from bojango.utils.format import BaseFormatter, MarkdownV2Formatter


@callback('s_start')
async def s_start(update, context):
	await asyncio.sleep(10)
	yield ActionScreen(text='Start message')
	await ActionManager.redirect('s_second', update, context)


@callback('s_second')
async def s_second(update, context):
	await ActionManager.redirect('s_third', update, context)


@callback('s_third')
async def s_third(update, context):
	await ActionManager.redirect('s_fourth', update, context)


@callback('s_fourth')
async def s_fourth(update, context):
	yield ActionScreen(text='Okay, im ready')