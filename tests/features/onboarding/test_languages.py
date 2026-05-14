from learn_english_bot.features.onboarding.languages import (
    get_language_page,
    has_next_language_page,
    is_supported_language,
    normalize_language_page,
)


def test_first_language_page_contains_five_languages() -> None:
    assert len(get_language_page(0)) == 5


def test_language_pages_have_next_page_until_last_page() -> None:
    assert has_next_language_page(0) is True
    assert has_next_language_page(1) is False


def test_normalize_language_page_wraps_unknown_page_to_start() -> None:
    assert normalize_language_page(-1) == 0
    assert normalize_language_page(99) == 0


def test_is_supported_language_checks_known_language_codes() -> None:
    assert is_supported_language("ru") is True
    assert is_supported_language("unknown") is False
