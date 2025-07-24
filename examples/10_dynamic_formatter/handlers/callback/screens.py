from bojango.action import ActionManager
from bojango.core.routing import callback
from bojango.action.screen import ActionScreen
from bojango.utils.format import BaseFormatter, MarkdownV2Formatter


@callback('s_start')
async def s_start(update, context):
	yield ActionScreen(text='Test message with *default formatter*, it\'s openai in bojangoconfig')
	await ActionManager.redirect('s_second', update, context)



class AnotherFormatter(MarkdownV2Formatter):
	def format(self, text: str) -> str:
		return f'>{super().format(text)}||'



@callback('s_second')
async def s_second(update, context):
	yield ActionScreen(text='Test message with another formatter', formatter=AnotherFormatter())