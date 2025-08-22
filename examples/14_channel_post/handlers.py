from bojango.core.routing import message


@message()
async def message(update, context):
	print(update)