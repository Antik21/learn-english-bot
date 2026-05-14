from dataclasses import dataclass


LANGUAGES_PAGE_SIZE = 5


@dataclass(frozen=True)
class LanguageOption:
    code: str
    title: str


LANGUAGES = [
    LanguageOption(code="ru", title="Русский"),
    LanguageOption(code="en", title="English"),
    LanguageOption(code="ka", title="ქართული"),
    LanguageOption(code="es", title="Español"),
    LanguageOption(code="de", title="Deutsch"),
    LanguageOption(code="fr", title="Français"),
    LanguageOption(code="it", title="Italiano"),
    LanguageOption(code="tr", title="Türkçe"),
    LanguageOption(code="pl", title="Polski"),
    LanguageOption(code="uk", title="Українська"),
]


def get_language_page(page: int) -> list[LanguageOption]:
    start = page * LANGUAGES_PAGE_SIZE
    end = start + LANGUAGES_PAGE_SIZE
    return LANGUAGES[start:end]


def has_next_language_page(page: int) -> bool:
    return (page + 1) * LANGUAGES_PAGE_SIZE < len(LANGUAGES)


def normalize_language_page(page: int) -> int:
    if page < 0:
        return 0

    max_page = max((len(LANGUAGES) - 1) // LANGUAGES_PAGE_SIZE, 0)
    if page > max_page:
        return 0
    return page


def is_supported_language(code: str) -> bool:
    return any(language.code == code for language in LANGUAGES)
