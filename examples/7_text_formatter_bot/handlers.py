from bojango.action.manager import ActionManager
from bojango.core.routing import command, callback, message, audio, video_note
from bojango.action.screen import ActionScreen, ActionButton, ScreenType
from bojango.utils.format import TelegramTextFormatter


# Обработчик команды /start
@command('start')
async def start_command(update, context):
	await ActionManager.redirect('s_screen', update, context)


@callback('s_screen')
async def s_audio(update, context):
	tf = TelegramTextFormatter()

	# tf.add_pre_replace(r'([_*`\[\]()~>#+=|{}.!-])', r'\\\1')
	# tf.add_pre_replace(r'(*)', r'\\\1')
	# tf.add_pre_replace(r'(?<=\w)\*(?=\W)', r'\\*')

	# Добавляем пары литералов, чтобы балансировать Markdown
	# tf.add_pre_replace(r'(?<!\\)(?<=\w)\*(?=\W)', r'\\*')

	# tf.add_pre_replace(r'(?<!\\)(?<=\w)(?<!\*)\*(?!\*)(?=\W)', r'\\*')

	# tf.add_pre_replace(r'(**)', r'\*')
	# tf.add_pre_replace(r'(*', r'\\*')
	tf.add_pre_replace(r'\*\*', '<&b>')
	tf.add_pre_replace(r'\*', r'<&s>')


	tf.add_literal('<&b>', '<&b>')

	# tf.add_literal('*', '*')
	tf.add_literal(r'_', r'_')
	tf.add_literal(r'`', r'`')
	# tf.add_literal(r'[]', r'[]')
	tf.add_literal(r'```', r'```')


	# Игнорируем Markdown-заголовки
	tf.add_ignore('#####')
	tf.add_ignore('####')
	tf.add_ignore('###')
	tf.add_ignore('##')
	tf.add_ignore('#')

	# Игнорируем кастомные паттерны, например, маркеры вида 【...】
	tf.add_ignore_pattern(r'【.*?】')

	# Постзамены (если хотим вернуть двойную звёздочку к одиночной)
	tf.add_post_replace(r'<&b>', r'*')
	tf.add_post_replace(r'<&s>', r'\*')

	# tf.add_pre_replace('*', '\\*')

	# tf.add_pre_replace(r'([^\*])(\*{1})(\*{2}|)([^\*])', r'\1\\*\3\4')

	# tf.add_literal('\\*', '\\*')
	# tf.add_literal('*', '*')
	# tf.add_literal('```', '```')
	# tf.add_literal('`', '`')
	# tf.add_literal('[', ']')
	#
	# tf.add_ignore('#####')
	# tf.add_ignore('####')
	# tf.add_ignore('###')
	# tf.add_ignore('##')
	#
	# tf.add_ignore_pattern(r'【.*?】')
	#
	# tf.add_post_replace(r'\*\*', '*')

	yield ActionScreen(tf.format('Тест 1: Алгоритм A* - один из самых *интересных* алгори**тмов'))
	yield ActionScreen(tf.format('Тест 2: Это **важный** момент'))  # GPT-стиль
	yield ActionScreen(tf.format('Тест 3: **Мощное** решение с **разметкой**'))  # двойные звезды
	yield ActionScreen(tf.format('Тест 4: Просто *жирный* текст без A*'))
	yield ActionScreen(tf.format('Тест 5: A* и *форматирование*'))  # комбо
	yield ActionScreen(tf.format('Тест 6: **A* и *B***'))  # опасный слом
	yield ActionScreen(tf.format('Тест 7: [Ссылка](https://example.com) и **текст**'))
	yield ActionScreen(tf.format('Тест 8: Это `код` и **важно**'))
	yield ActionScreen(tf.format('Тест 9: `Код без разметки *внутри*`'))
	yield ActionScreen(tf.format('Тест 10: A*B*C без форматирования'))
	yield ActionScreen(tf.format('Тест 11: Код: ```python\nprint("Hello")\n```'))
	yield ActionScreen(tf.format('Тест 12: Заголовок ### не должен отображаться'))
	yield ActionScreen(tf.format('Тест 13: **Несбалансированный жирный'))
	yield ActionScreen(tf.format('Тест 14: Подчёркнутый _элемент_'))
	yield ActionScreen(tf.format('Тест 15: **Жирный** и _подчёркнутый_ рядом'))
	yield ActionScreen(tf.format('Тест 16: Экранированные символы A\\* и \\*неформат*'))
	yield ActionScreen(tf.format('Тест 17: Алгоритм D* — и *тут* тоже'))
	yield ActionScreen(tf.format('Тест 18: Комбинация `код *внутри* текста` и **выделение**'))
	yield ActionScreen(tf.format('Тест 19: **Жирный**, но с A* внутри'))
	yield ActionScreen(tf.format('Тест 20: Просто текст без разметки'))

	# yield ActionScreen(tf.format('Алгоритм A* - один из самых *интересных* алгоритмов'))
	# yield ActionScreen(tf.format('Алгоритм A* - один из самых *интересных* алгоритмов'))
	# yield ActionScreen(tf.format('Экран 1: Одна звездочка *, не должна сломать'))
	# yield ActionScreen(tf.format('Экран 2: Две звездочки, *просто жирный текст*'))
	# yield ActionScreen(tf.format('Экран 3: ## Типо заголовок, ### И еще один, #### И еще один, ##### и еще.'))
	# yield ActionScreen(tf.format('Экран 4: Одна звездочка *, *не должна сломать*'))
	# yield ActionScreen(tf.format('Экран 5: *Одна звездочка *, не должна сломать*'))
	# yield ActionScreen(tf.format('Экран 6: ```python print("hello world")```'))
	# yield ActionScreen(tf.format('Экран 7: Текст без символов markdown'))
	# yield ActionScreen(tf.format('Экран 8: _Курсив в Markdown_, проверка подчёркивания'))
	# yield ActionScreen(tf.format('Экран 9: Комбинация *жирный _и курсив_*'))
	# yield ActionScreen(tf.format('Экран 10: Экранированные символы \\*не жирный\\*'))
	# yield ActionScreen(tf.format('Экран 11: Лишняя *звёздочка без пары'))
	# yield ActionScreen(tf.format('Экран 12: `Код внутри одной строки`'))
	# yield ActionScreen(tf.format('Экран 13: [Ссылка](https://example.com) и текст рядом'))
	# yield ActionScreen(tf.format('Экран 14: Открытый блок кода ```print(1)'))
	# yield ActionScreen(tf.format('Экран 15: Неправильный markdown с **двумя звёздочками и без конца'))
	# yield ActionScreen(tf.format('Экран 16: Несколько __подчёркнутых__ элементов и **жирных** рядом'))
	# yield ActionScreen(tf.format('Экран 17: Много разных символов * # ` [ ] ( ) ! ~ > <'))
	# yield ActionScreen(tf.format('Экран 18: Сообщение с эмодзи 😊 и markdown *текст*'))
	# yield ActionScreen(tf.format('Экран 19: Заголовок с решётками #### Заголовок 4 уровня'))
	# yield ActionScreen(tf.format('Экран 20: Текст с 【кастомным маркером】и *markdown* символами'))

