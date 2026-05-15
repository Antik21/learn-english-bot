from collections.abc import Sequence

from aiogram import Bot
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from learn_english_bot.messengers.contracts import (
    AnswerCallback,
    EditMessage,
    MessengerAction,
    MessengerContext,
    MessengerKeyboard,
    SendMessage,
)

TELEGRAM_MESSENGER = "telegram"


class TelegramMessengerClient:
    def __init__(self, bot: Bot) -> None:
        self._bot = bot

    async def execute(self, actions: Sequence[MessengerAction]) -> None:
        for action in actions:
            if isinstance(action, SendMessage):
                await self._bot.send_message(
                    chat_id=action.chat_id,
                    text=action.text,
                    reply_markup=_to_telegram_keyboard(action.keyboard),
                )
                continue

            if isinstance(action, EditMessage):
                await self._bot.edit_message_text(
                    chat_id=action.chat_id,
                    message_id=int(action.message_id),
                    text=action.text,
                    reply_markup=_to_telegram_keyboard(action.keyboard),
                )
                continue

            if isinstance(action, AnswerCallback):
                await self._bot.answer_callback_query(
                    callback_query_id=action.callback_id,
                    text=action.text,
                    show_alert=action.show_alert,
                )


def message_to_context(message: Message) -> MessengerContext | None:
    if message.from_user is None:
        return None

    return MessengerContext(
        messenger=TELEGRAM_MESSENGER,
        chat_id=str(message.chat.id),
        external_user_id=str(message.from_user.id),
        language_code=message.from_user.language_code,
        message_id=str(message.message_id),
    )


def callback_to_context(callback: CallbackQuery) -> MessengerContext | None:
    if not isinstance(callback.message, Message):
        return None

    return MessengerContext(
        messenger=TELEGRAM_MESSENGER,
        chat_id=str(callback.message.chat.id),
        external_user_id=str(callback.from_user.id),
        language_code=callback.from_user.language_code,
        message_id=str(callback.message.message_id),
        callback_id=callback.id,
    )


def _to_telegram_keyboard(keyboard: MessengerKeyboard | None) -> InlineKeyboardMarkup | None:
    if keyboard is None:
        return None

    builder = InlineKeyboardBuilder()
    row_widths: list[int] = []
    for row in keyboard.rows:
        if not row:
            continue

        row_widths.append(len(row))
        for button in row:
            builder.button(text=button.text, callback_data=button.payload)

    if not row_widths:
        return None

    builder.adjust(*row_widths)
    return builder.as_markup()
