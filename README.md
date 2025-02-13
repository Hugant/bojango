# Bojango

Bojango — это фреймворк для упрощения разработки Telegram-ботов. Он предоставляет удобные инструменты для маршрутизации, управления экранами, локализации и работы с асинхронными функциями.

## Особенности

- **Маршрутизация**: Используйте удобные декораторы для регистрации команд и callback-обработчиков.
- **Управление экранами**: Легко создавайте и рендерьте интерфейсы с кнопками.
- **Локализация**: Поддержка мультиязычных приложений с помощью gettext.
- **Асинхронная архитектура**: Полная поддержка asyncio для высокопроизводительных приложений.
- **Гибкость**: Возможность расширения и кастомизации под ваши задачи.

## Быстрый старт

### 1. Установка и настройка

Установить Bojango можно через `pip`:

```bash
pip install bojango
```

Создайте файл `bot.py` и настройте бота:

```python
from bojango.bot import BojangoBot, BojangoBotConfig

config = BojangoBotConfig(
    api_token='YOUR_BOT_TOKEN',
    handlers_modules=['handlers']
)

bot = BojangoBot(config)
bot.run()
```

### 2. Регистрация команд

Создайте файл `handlers.py` и добавьте команду:

```python
from bojango.core.routing import command
from bojango.action.screen import ActionScreen

@command('start')
async def start_command(update, context):
    yield ActionScreen(text='Добро пожаловать! Этот бот создан с помощью bojango')
```

### 3. Запуск бота

Запустите бота:
```bash
python bot.py
```

## Базовые сущности

### `ActionManager`
`ActionManager` - отвечает за регистрацию и выполнение действий. Позволяет добавлять и получать 
действия по имени, а также выполнять их с передачей аргументов.

Пример регистрации и выполнения действия:
```python
from bojango.action.manager import ActionManager

async def my_action(update, context, args):
    await update.message.reply_text('Привет! Это кастомное действие.')

manager = ActionManager()
manager.register_action('custom_action', my_action)

# Выполнение действия
await manager.execute_action('custom_action', update, context)
```

### `ActionButton`
`ActionButton` - кнопка, связанная с определённым действием или ссылкой.

Пример создания кнопки:
```python
from bojango.action.screen import ActionButton

button = ActionButton('Подробнее', action_name='details')
```

### `ActionScreen`
`ActionScreen` - представляет собой экран с текстом и кнопками, который может отображаться пользователю.

Пример создания и отображения экрана:
```python
from bojango.action.screen import ActionScreen, ActionButton, ScreenType

screen = ActionScreen(
    text='Выберите действие:',
    buttons=[[ActionButton('Нажми меня', action_name='next_step')]],
    screen_type=ScreenType.NEW  # По умолчанию ScreenType.EDIT
)
await screen.render(update, context)
```

## Роутинг и регистрация действий

Bojango предоставляет гибкую систему маршрутизации для обработки команд, callback-запросов и текстовых 
сообщений. Все маршруты регистрируются через Router и связываются с соответствующими обработчиками.

### Регистрация команд
Команды регистрируются с помощью декоратора `@command`. При вызове соответствующей команды в Telegram-боте 
срабатывает привязанный обработчик, который может отправлять пользователю `ActionScreen`.
Функция обернутая декоратором `@command` обязательно должна принимать `update` и `context`.

Пример регистрации команды `/start`, предполагаются что уже зарегистрированы `next_step` и `about`:
```python
from bojango.core.routing import command
from bojango.action.screen import ActionScreen, ActionButton, ScreenType

@command('start')
async def start_command(update, context):
    yield ActionScreen(
        text='Добро пожаловать! Выберите действие:',
        buttons=[
            [ActionButton(text='Далее', action_name='next_step')],
            [ActionButton(text='О нас', action_name='about')]
        ],
        screen_type=ScreenType.NEW  # По умолчанию ScreenType.EDIT
    )
```

### Регистрация callback-запросов
Для обработки callback-запросов (например, нажатия кнопок) используется декоратор `@callback`. 
Callback-запросы позволяют передавать дополнительные параметры и менять отображение экрана.
Функция обернутая декоратором `@callback` обязательно должна принимать `update`, `context` и `args`.

Пример callback-обработчика:
```python
from bojango.core.routing import callback
from bojango.action.screen import ActionScreen, ActionButton

@callback('next_step')
async def next_step_callback(update, context, args):
    yield ActionScreen(
        text='Вы перешли на следующий шаг!',
        buttons=[[ActionButton(text='Назад', action_name='start')]]
    )
```

### Регистрация обработчиков сообщений
Можно регистрировать обработчики текстовых сообщений, например, для обработки пользовательского ввода.
Функция обернутая декоратором `message` обязательно должна принимать `update` и `context`.

```python
from bojango.core.routing import message
from bojango.action.screen import ActionScreen, ActionButton

@message()
async def handle_text_message(update, context):
    user_text = update.message.text
    yield ActionScreen(
        text=f'Вы написали: {user_text}',
        buttons=[[ActionButton(text='Ок', action_name='start')]]
    )
```

В Bojango можно фильтровать входящие текстовые сообщения, используя параметр pattern в декораторе @message. 
Это позволяет обрабатывать только определенные сообщения, например, команды, номера телефонов или адреса электронной почты.

```python
from bojango.core.routing import message
from bojango.action.screen import ActionScreen, ActionButton

@message(pattern=r'^\d{10}$')  # Фильтруем только 10-значные числа (например, номера телефонов без кода страны)
async def phone_number_handler(update, context):
    yield ActionScreen(
        text='Вы отправили номер телефона!',
        buttons=[[ActionButton(text='Назад', action_name='start')]]
    )
```

Фильтрация e-mail адресов
```python
from bojango.core.routing import message
from bojango.action.screen import ActionScreen, ActionButton

@message(pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
async def email_handler(update, context):
    yield ActionScreen(
        text='Вы отправили e-mail!',
        buttons=[[ActionButton(text='Ок', action_name='start')]]
    )
```

Фильтрация сообщений, содержащих слово 'привет'
```python
from bojango.core.routing import message
from bojango.action.screen import ActionScreen, ActionButton

@message(pattern=r'.*привет.*')
async def hello_handler(update, context):
    yield ActionScreen(
        text='Привет! Как я могу помочь?',
        buttons=[[ActionButton(text='Меню', action_name='start')]]
    )
```

## Редирект
В Bojango метод `ActionManager.redirect` позволяет перенаправлять пользователя на другое действие без необходимости 
повторного вызова обработчика вручную. Это полезно, когда нужно динамически менять экраны в зависимости от контекста.

```python
from bojango.core.routing import callback, message

from bojango.action.manager import ActionManager
from bojango.action.screen import ActionScreen

@callback('start_screen')
async def start_screen(update, context, args):
  yield ActionScreen(text='Это приветственный экран')

@message
async def check_numbers(update, context, args):
    if update.message.text.lower() == 'Привет':
        await ActionManager.redirect('start_screen', update, context)
    else:
        yield ActionScreen(text=f'Вы написали: {update.message.text}')
```

Редирект возможен только на функции, обернутые декоратором `@callback`. 

## Привязка маршрутов к боту
Все зарегистрированные маршруты автоматически привязываются к Telegram-приложению при запуске BojangoBot. 
Однако, если требуется вручную привязать их, можно использовать Router:

```python
from bojango.core.routing import Router

router = Router()
router.register_command('start', start_command)
router.register_callback('next_step', next_step_callback)
router.register_message(handle_text_message)
```

## Требования
- Python 3.10+
- Telegram Bot API

## Лицензия
Bojango распространяется под лицензией MIT. Подробнее см. в файле LICENSE.