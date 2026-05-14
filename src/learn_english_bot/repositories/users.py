from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from learn_english_bot.db.models import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_telegram_id(self, telegram_user_id: int) -> User | None:
        result = await self._session.execute(
            select(User).where(User.telegram_user_id == telegram_user_id)
        )
        return result.scalar_one_or_none()

    async def get_or_create(
        self,
        *,
        telegram_user_id: int,
        telegram_language_code: str | None,
    ) -> User:
        user = await self.get_by_telegram_id(telegram_user_id)
        if user is not None:
            user.telegram_language_code = telegram_language_code
            return user

        user = User(
            telegram_user_id=telegram_user_id,
            telegram_language_code=telegram_language_code,
        )
        self._session.add(user)
        await self._session.flush()
        return user

    async def set_base_language(self, user: User, language_code: str) -> None:
        user.base_language = language_code
        await self._session.flush()

    async def mark_onboarding_completed(self, user: User) -> None:
        user.onboarding_completed_at = datetime.utcnow()
        await self._session.flush()
