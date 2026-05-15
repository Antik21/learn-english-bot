# Telegram Messenger Adapter

## Назначение

Папка содержит Telegram-реализацию messenger-контракта.

Текущий статус: `Готово частично`.

## Правила

- Здесь разрешены импорты `aiogram`.
- Adapter преобразует `MessengerAction` в вызовы Telegram Bot API.
- Handler-ы могут преобразовывать входящие Telegram-события в `MessengerContext`.
- Бизнес-логика flow не должна переезжать в adapter или Telegram router.
- Если Telegram-специфичная возможность не выражается текущим контрактом, сначала нужно расширить общий контракт минимально необходимым способом.

