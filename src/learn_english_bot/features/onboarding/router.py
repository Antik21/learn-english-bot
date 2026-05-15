from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from learn_english_bot.features.onboarding.callbacks import (
    LANGUAGE_CALLBACK_PREFIX,
    LANGUAGE_PAGE_CALLBACK_PREFIX,
    parse_language_callback,
    parse_language_page_callback,
)
from learn_english_bot.features.onboarding.flow import ONBOARDING_FLOW, OnboardingFlow
from learn_english_bot.messengers.telegram.adapter import (
    TelegramMessengerClient,
    callback_to_context,
)
from learn_english_bot.repositories.flows import FlowRepository
from learn_english_bot.repositories.users import UserRepository

router = Router(name="onboarding")

START_REQUIRED_MESSAGE = "Отправьте /start, чтобы начать."


@router.callback_query(F.data.startswith(LANGUAGE_PAGE_CALLBACK_PREFIX))
async def handle_language_page(
    callback: CallbackQuery,
    session: AsyncSession,
    bot: Bot,
) -> None:
    page = parse_language_page_callback(callback.data)
    if page is None:
        await callback.answer()
        return

    context = callback_to_context(callback)
    if context is None:
        await callback.answer(START_REQUIRED_MESSAGE, show_alert=True)
        return

    user = await UserRepository(session).get_by_telegram_id(callback.from_user.id)
    if user is None:
        await callback.answer(START_REQUIRED_MESSAGE, show_alert=True)
        return

    flow = await FlowRepository(session).get_active(user_id=user.id, flow_name=ONBOARDING_FLOW)
    if flow is None:
        await callback.answer(START_REQUIRED_MESSAGE, show_alert=True)
        return

    actions = await OnboardingFlow(session).show_language_page(context, flow, page)
    await TelegramMessengerClient(bot).execute(actions)


@router.callback_query(F.data.startswith(LANGUAGE_CALLBACK_PREFIX))
async def handle_language_selected(
    callback: CallbackQuery,
    session: AsyncSession,
    bot: Bot,
) -> None:
    language_code = parse_language_callback(callback.data)
    if language_code is None:
        await callback.answer()
        return

    context = callback_to_context(callback)
    if context is None:
        await callback.answer(START_REQUIRED_MESSAGE, show_alert=True)
        return

    user = await UserRepository(session).get_by_telegram_id(callback.from_user.id)
    if user is None:
        await callback.answer(START_REQUIRED_MESSAGE, show_alert=True)
        return

    flow = await FlowRepository(session).get_active(user_id=user.id, flow_name=ONBOARDING_FLOW)
    if flow is None:
        await callback.answer(START_REQUIRED_MESSAGE, show_alert=True)
        return

    actions = await OnboardingFlow(session).select_language(
        context,
        user,
        flow,
        language_code,
    )
    await TelegramMessengerClient(bot).execute(actions)
