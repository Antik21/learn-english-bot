from learn_english_bot.features.onboarding.callbacks import (
    build_language_callback,
    build_language_page_callback,
)
from learn_english_bot.features.onboarding.languages import (
    get_language_page,
    has_next_language_page,
    normalize_language_page,
)
from learn_english_bot.messengers.contracts import MessengerButton, MessengerKeyboard


def build_language_keyboard(page: int) -> MessengerKeyboard:
    normalized_page = normalize_language_page(page)
    buttons = [
        MessengerButton(
            text=language.title,
            payload=build_language_callback(language.code),
        )
        for language in get_language_page(normalized_page)
    ]

    if has_next_language_page(normalized_page):
        next_page = normalized_page + 1
    else:
        next_page = 0

    buttons.append(
        MessengerButton(
            text="Еще",
            payload=build_language_page_callback(next_page),
        )
    )
    return MessengerKeyboard(rows=_chunk_buttons(buttons, row_size=2))


def _chunk_buttons(
    buttons: list[MessengerButton],
    *,
    row_size: int,
) -> tuple[tuple[MessengerButton, ...], ...]:
    return tuple(
        tuple(buttons[index : index + row_size])
        for index in range(0, len(buttons), row_size)
    )
