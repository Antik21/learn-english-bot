from aiogram.filters.callback_data import CallbackData


class LanguageCallback(CallbackData, prefix="onboarding_language"):
    code: str


class LanguagePageCallback(CallbackData, prefix="onboarding_languages"):
    page: int
