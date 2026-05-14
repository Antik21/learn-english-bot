from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from learn_english_bot.features.onboarding.callbacks import (
    LanguageCallback,
    LanguagePageCallback,
)
from learn_english_bot.features.onboarding.flow import ONBOARDING_FLOW, OnboardingFlow
from learn_english_bot.repositories.flows import FlowRepository
from learn_english_bot.repositories.users import UserRepository

router = Router(name="onboarding")


@router.callback_query(LanguagePageCallback.filter())
async def handle_language_page(
    callback: CallbackQuery,
    callback_data: LanguagePageCallback,
    session: AsyncSession,
) -> None:
    if callback.from_user is None:
        await callback.answer()
        return

    users = UserRepository(session)
    user = await users.get_by_telegram_id(callback.from_user.id)
    if user is None:
        await callback.answer("Отправьте /start, чтобы начать.", show_alert=True)
        return

    flows = FlowRepository(session)
    flow = await flows.get_active(user_id=user.id, flow_name=ONBOARDING_FLOW)
    if flow is None:
        await callback.answer("Отправьте /start, чтобы начать.", show_alert=True)
        return

    await OnboardingFlow(session).show_language_page(callback, flow, callback_data.page)


@router.callback_query(LanguageCallback.filter())
async def handle_language_selected(
    callback: CallbackQuery,
    callback_data: LanguageCallback,
    session: AsyncSession,
) -> None:
    if callback.from_user is None:
        await callback.answer()
        return

    users = UserRepository(session)
    user = await users.get_by_telegram_id(callback.from_user.id)
    if user is None:
        await callback.answer("Отправьте /start, чтобы начать.", show_alert=True)
        return

    flows = FlowRepository(session)
    flow = await flows.get_active(user_id=user.id, flow_name=ONBOARDING_FLOW)
    if flow is None:
        await callback.answer("Отправьте /start, чтобы начать.", show_alert=True)
        return

    await OnboardingFlow(session).select_language(callback, user, flow, callback_data.code)
