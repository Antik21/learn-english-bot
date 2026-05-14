# learn-english-bot

Telegram-бот для помощи в изучении английского языка.

## Локальный запуск

Требуется Python 3.12+.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
```

После этого нужно указать в `.env` токен Telegram-бота:

```env
BOT_TOKEN=your-telegram-bot-token
```

Запуск:

```powershell
python -m learn_english_bot
```

Минимальный сценарий уже доступен: команда `/start` создает пользователя в базе,
запускает onboarding и предлагает выбрать язык. Если onboarding уже пройден,
бот отвечает `Привет`.

## Переменные окружения

Описание переменных находится в [docs/env.md](docs/env.md).
