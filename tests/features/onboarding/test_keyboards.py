from learn_english_bot.features.onboarding.callbacks import (
    build_language_callback,
    build_language_page_callback,
)
from learn_english_bot.features.onboarding.keyboards import build_language_keyboard


def test_language_keyboard_contains_language_buttons_and_more_button() -> None:
    keyboard = build_language_keyboard(0)
    buttons = [button for row in keyboard.rows for button in row]

    assert len(buttons) == 6
    assert buttons[0].text == "Русский"
    assert buttons[0].payload == build_language_callback("ru")
    assert buttons[-1].text == "Еще"
    assert buttons[-1].payload == build_language_page_callback(1)


def test_last_language_keyboard_page_wraps_more_button_to_first_page() -> None:
    keyboard = build_language_keyboard(1)
    buttons = [button for row in keyboard.rows for button in row]

    assert buttons[-1].payload == build_language_page_callback(0)
