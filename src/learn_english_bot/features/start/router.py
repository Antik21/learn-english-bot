from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from learn_english_bot.features.onboarding.flow import OnboardingFlow
from learn_english_bot.features.start.service import get_onboarding_completed_message
from learn_english_bot.repositories.users import UserRepository

router = Router(name="start")


@router.message(CommandStart())
async def handle_start(message: Message, session: AsyncSession) -> None:
    if message.from_user is None:
        await message.answer(get_onboarding_completed_message())
        return

    users = UserRepository(session)
    user = await users.get_or_create(
        telegram_user_id=message.from_user.id,
        telegram_language_code=message.from_user.language_code,
    )

    if user.onboarding_completed_at is not None:
        await message.answer(get_onboarding_completed_message())
        return

    await OnboardingFlow(session).start_or_continue(message, user)
