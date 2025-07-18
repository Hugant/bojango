from bojango.core.routing import image
from bojango.action.dispatcher import ActionManager

@image()
async def image(update, context):
    await ActionManager.redirect('s_image', update, context)