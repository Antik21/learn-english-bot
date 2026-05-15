from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class MessengerContext:
    messenger: str
    chat_id: str
    external_user_id: str
    language_code: str | None = None
    message_id: str | None = None
    callback_id: str | None = None


@dataclass(frozen=True)
class MessengerButton:
    text: str
    payload: str


@dataclass(frozen=True)
class MessengerKeyboard:
    rows: tuple[tuple[MessengerButton, ...], ...]


@dataclass(frozen=True)
class SendMessage:
    chat_id: str
    text: str
    keyboard: MessengerKeyboard | None = None


@dataclass(frozen=True)
class EditMessage:
    chat_id: str
    message_id: str
    text: str
    keyboard: MessengerKeyboard | None = None


@dataclass(frozen=True)
class AnswerCallback:
    callback_id: str
    text: str | None = None
    show_alert: bool = False


MessengerAction = SendMessage | EditMessage | AnswerCallback


class MessengerClient(Protocol):
    async def execute(self, actions: Sequence[MessengerAction]) -> None:
        pass

