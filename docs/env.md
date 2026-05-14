# Environment

## Быстрый старт

1. Скопировать `.env.example` в `.env`.
2. Указать `BOT_TOKEN`, полученный у BotFather.
3. Запустить бота командой `python -m learn_english_bot`.

## Переменные окружения

| Переменная | Обязательная | Описание |
| --- | --- | --- |
| `BOT_TOKEN` | Да | Токен Telegram Bot API. |
| `ENVIRONMENT` | Нет | Текущий контур запуска: `development`, `staging` или `production`. |
| `LOG_LEVEL` | Нет | Уровень логирования: `DEBUG`, `INFO`, `WARNING`, `ERROR`. |
| `DATABASE_URL` | Нет | URL базы данных. По умолчанию используется локальная SQLite-база `sqlite+aiosqlite:///./data/app.sqlite3`. |
| `AMPLITUDE_ENABLED` | Нет | Флаг включения Amplitude-аналитики после реализации клиента. |
| `AMPLITUDE_API_KEY` | Нет | API key проекта Amplitude. Пока может быть пустым. |

Секреты из `.env` нельзя коммитить в репозиторий.
