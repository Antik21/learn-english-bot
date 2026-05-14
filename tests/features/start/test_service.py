from learn_english_bot.features.start.service import get_onboarding_completed_message


def test_get_onboarding_completed_message_returns_expected_text() -> None:
    assert get_onboarding_completed_message() == "Привет"
