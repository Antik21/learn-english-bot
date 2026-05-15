from aiogram import Bot, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from learn_english_bot.features.onboarding.flow import OnboardingFlow
from learn_english_bot.features.start.service import get_onboarding_completed_message
from learn_english_bot.messengers.contracts import SendMessage
from learn_english_bot.messengers.telegram.adapter import (
    TelegramMessengerClient,
    message_to_context,
)
from learn_english_bot.repositories.users import UserRepository

router = Router(name="start")


@router.message(CommandStart())
async def handle_start(message: Message, session: AsyncSession, bot: Bot) -> None:
    messenger = TelegramMessengerClient(bot)
    context = message_to_context(message)

    if context is None:
        await messenger.execute(
            [
                SendMessage(
                    chat_id=str(message.chat.id),
                    text=get_onboarding_completed_message(),
                )
            ]
        )
        return

    users = UserRepository(session)
    user = await users.get_or_create(
        telegram_user_id=int(context.external_user_id),
        telegram_language_code=context.language_code,
    )

    if user.onboarding_completed_at is not None:
        await messenger.execute(
            [
                SendMessage(
                    chat_id=context.chat_id,
                    text=get_onboarding_completed_message(),
                )
            ]
        )
        return

    actions = await OnboardingFlow(session).start_or_continue(context, user)
    await messenger.execute(actions)
