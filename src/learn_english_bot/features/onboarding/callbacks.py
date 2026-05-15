LANGUAGE_CALLBACK_PREFIX = "onboarding:language:"
LANGUAGE_PAGE_CALLBACK_PREFIX = "onboarding:languages_page:"


def build_language_callback(code: str) -> str:
    return f"{LANGUAGE_CALLBACK_PREFIX}{code}"


def build_language_page_callback(page: int) -> str:
    return f"{LANGUAGE_PAGE_CALLBACK_PREFIX}{page}"


def parse_language_callback(data: str | None) -> str | None:
    if data is None or not data.startswith(LANGUAGE_CALLBACK_PREFIX):
        return None

    code = data.removeprefix(LANGUAGE_CALLBACK_PREFIX)
    return code or None


def parse_language_page_callback(data: str | None) -> int | None:
    if data is None or not data.startswith(LANGUAGE_PAGE_CALLBACK_PREFIX):
        return None

    page = data.removeprefix(LANGUAGE_PAGE_CALLBACK_PREFIX)
    try:
        return int(page)
    except ValueError:
        return None
