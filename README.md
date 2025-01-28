# Bojango

Bojango — это фреймворк для упрощения разработки Telegram-ботов. Он предоставляет удобные инструменты для маршрутизации, управления экранами, локализации и работы с асинхронными функциями.

## Установка

Установить Bojango можно через `pip`:

```bash
pip install bojango
```

## Особенности

- **Маршрутизация**: Используйте удобные декораторы для регистрации команд и callback-обработчиков.
- **Управление экранами**: Легко создавайте и рендерьте интерфейсы с кнопками.
- **Локализация**: Поддержка мультиязычных приложений с помощью gettext.
- **Асинхронная архитектура**: Полная поддержка asyncio для высокопроизводительных приложений.
- **Гибкость**: Возможность расширения и кастомизации под ваши задачи.

## Быстрый старт

```python
from bojango.core.bot import BojangoBot
from bojango.action.screen import ActionScreen
from bojango.core.routing import command, callback


class MyBot(BojangoBot):
  api_token = 'ВАШ_API_ТОКЕН'
  localizer = None  # Опционально: настройте локализацию
  handlers_modules = ['mybot.handlers']  # Укажите модуль(и) с обработчиками


if __name__ == '__main__':
  bot = MyBot()
  bot.run()
```

## Пример обработчика

```python
from bojango.core.routing import command, callback
from bojango.action.screen import ActionScreen, ActionButton

@command('start')
async def start_handler(update, context):
  screen = ActionScreen(
    text='Добро пожаловать!',
    buttons=[[ActionButton(text='Кнопка 1', action_name='button_action')]]
  )
  await screen.render(update, context)

@callback('button_action')
async def button_handler(update, context, args):
  screen = ActionScreen(text='Вы нажали на кнопку!')
  await screen.render(update, context)
```

## Структура проекта

```text
myproject/
│
├── mybot/
│   ├── __init__.py
│   ├── handlers/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── locales/
│   │   ├── en/
│   │   └── ru/
│   └── main.py
│
└── README.md
```

## Требования
- Python 3.10+
- Telegram Bot API

## Лицензия
Bojango распространяется под лицензией MIT. Подробнее см. в файле LICENSE.