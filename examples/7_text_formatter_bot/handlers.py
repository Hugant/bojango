from bojango.action.dispatcher import ActionManager
from bojango.core.routing import command, callback, message, audio, video_note
from bojango.action.screen import ActionScreen, ActionButton, ScreenType
from bojango.utils.formatter import TelegramTextFormatter


@command('start')
async def start_command(update, context):
	await ActionManager.redirect('s_screen', update, context)


@callback('s_screen')
async def s_audio(update, context):
	# tf = TelegramTextFormatter()
	#
	# tf.add_pre_replace(r'\*\*', '&&b')
	# tf.add_pre_replace(r'\*', r'&&s')
	# tf.add_pre_replace(r'_', r'&&u')
	# tf.add_pre_replace(r'`', r'&&q')
	# tf.add_pre_replace(r'```', r'&&mq')
	#
	#
	# tf.add_literal('&&b', '&&b')
	# tf.add_literal('&&u', '&&u')
	# tf.add_literal('&&q', '&&q')
	# tf.add_literal('&&mq', '&&mq')
	#
	# # Игнорируем Markdown-заголовки
	# tf.add_ignore('#####')
	# tf.add_ignore('####')
	# tf.add_ignore('###')
	# tf.add_ignore('##')
	# tf.add_ignore('#')
	#
	# # Игнорируем кастомные паттерны, например, маркеры вида 【...】
	# tf.add_ignore_pattern(r'【.*?】')
	#
	# # Постзамены (если хотим вернуть двойную звёздочку к одиночной)
	# tf.add_post_replace(r'&&b', r'*')
	# tf.add_post_replace(r'&&s', r'\*')
	# tf.add_post_replace(r'&&u', r'_')
	# tf.add_post_replace(r'&&q', r'`')
	# tf.add_post_replace(r'&&mq', r'```')

	# yield ActionScreen('Тест 1: *bo\*ld*')
	# yield ActionScreen('Тест 1: **bold A* text**')
	# yield ActionScreen('Тест 1: **bold A* text**')
	# yield ActionScreen('Тест 1: **bold A* text**')
	yield ActionScreen('Тест 1: **bold A* text**')
	yield ActionScreen('Тест 2: _italic *text_?')
	yield ActionScreen('Тест 3: __underline__')
	yield ActionScreen('Тест 4: ~~strikethrough~~')
	yield ActionScreen('Тест 5: ||spoiler||')
	yield ActionScreen('Тест 6: *bold _italic bold ~italic bold strikethrough ||italic bold strikethrough spoiler||~ __underline italic bold___ bold*')
	yield ActionScreen('Тест 7: [inline URL](http://www.example.com/)')
	yield ActionScreen('Тест 8: [inline mention of a user](tg://user?id=hugant)')
	yield ActionScreen('Тест 9: ![👍](tg://emoji?id=5368324170671202286)')
	yield ActionScreen('Тест 10: `inline fixed-width code`')
	yield ActionScreen('Тест 11: ```pre-formatted fixed-width code block```')
	yield ActionScreen('Тест 12: ```python pre-formatted fixed-width code block written in the Python programming language```')
	# yield ActionScreen('Тест 13: >Block quotation started')
	# yield ActionScreen('Тест 13: >Block quotation continued')
	# yield ActionScreen('Тест 14: **>The expandable block quotation started right after the previous block quotation')
	# yield ActionScreen('Тест 15: >The last line of the expandable block quotation with the expandability mark||')
	yield ActionScreen('Тест 1: Алгоритм A* - один из самых *интересных* алгори**тмов')
	yield ActionScreen('Тест 2: Это **важный** момент')  # GPT-стил
	yield ActionScreen('Тест 3: **Мощное** решение с **разметкой**')  # двойные звезд
	yield ActionScreen('Тест 4: Просто *жирный* текст без A*')
	yield ActionScreen('Тест 5: A* и *форматирование*')  # комб
	yield ActionScreen('Тест 6: **A* и *B***')  # опасный сло
	yield ActionScreen('Тест 7: [Ссылка](https://example.com) и **текст**')
	yield ActionScreen('Тест 8: Это `код` и **важно**')
	yield ActionScreen('Тест 9: `Код без разметки *внутри*`!')
	yield ActionScreen('Тест 10: A*B*C (без форматирования)')
	yield ActionScreen('Тест 11: Код: ```python\nprint("Hello")\n def foo(a: str): return [int(a) * 3 + 4]{3}```')
	yield ActionScreen('Тест 12: Заголовок ### не должен отображаться')
	yield ActionScreen('Тест 13: **Несбалансированный жирный')
	yield ActionScreen('Тест 14: Подчёркнутый _элемент_')
	yield ActionScreen('Тест 15: **Жирный** и _подчёркнутый_ рядом')
	yield ActionScreen('Тест 16: Экранированные символы A\\* и \\*неформат*')
	yield ActionScreen('Тест 17: Алгоритм D* — и *тут* тоже')
	yield ActionScreen('Тест 18: Комбинация `код *внутри* текста` и **выделение**')
	yield ActionScreen('Тест 19: **Жирный, но с A* внутри**')
	yield ActionScreen('Тест 20: Просто текст без разметки')
	yield ActionScreen('Тест 21: 2 + 2 = 4')


