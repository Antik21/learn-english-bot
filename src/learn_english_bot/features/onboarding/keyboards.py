from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from learn_english_bot.features.onboarding.callbacks import (
    LanguageCallback,
    LanguagePageCallback,
)
from learn_english_bot.features.onboarding.languages import (
    get_language_page,
    has_next_language_page,
    normalize_language_page,
)


def build_language_keyboard(page: int) -> InlineKeyboardMarkup:
    normalized_page = normalize_language_page(page)
    builder = InlineKeyboardBuilder()

    for language in get_language_page(normalized_page):
        builder.button(
            text=language.title,
            callback_data=LanguageCallback(code=language.code),
        )

    if has_next_language_page(normalized_page):
        next_page = normalized_page + 1
    else:
        next_page = 0

    builder.button(
        text="Еще",
        callback_data=LanguagePageCallback(page=next_page),
    )
    builder.adjust(2, 2, 2)
    return builder.as_markup()
