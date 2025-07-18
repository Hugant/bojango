from bojango.core.routing import callback
from bojango.action.screen import ActionScreen


@callback('s_start')
async def s_start(update, context):
    yield ActionScreen(text='👋 Добро пожаловать')


@callback('s_image')
async def s_image(update, context):
    yield ActionScreen(text='Есть картинка')