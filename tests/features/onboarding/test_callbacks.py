from learn_english_bot.features.onboarding.callbacks import (
    build_language_callback,
    build_language_page_callback,
    parse_language_callback,
    parse_language_page_callback,
)


def test_language_callback_roundtrip() -> None:
    payload = build_language_callback("ru")

    assert parse_language_callback(payload) == "ru"


def test_language_page_callback_roundtrip() -> None:
    payload = build_language_page_callback(2)

    assert parse_language_page_callback(payload) == 2


def test_invalid_callbacks_return_none() -> None:
    assert parse_language_callback("unknown") is None
    assert parse_language_page_callback("unknown") is None
    assert parse_language_page_callback(build_language_page_callback(page=0) + "x") is None

