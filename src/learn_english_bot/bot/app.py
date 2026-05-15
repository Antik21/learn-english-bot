from aiogram import Dispatcher
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from learn_english_bot.bot.middlewares import DatabaseSessionMiddleware
from learn_english_bot.features.onboarding.router import router as onboarding_router
from learn_english_bot.features.start.router import router as start_router


def create_dispatcher(session_factory: async_sessionmaker[AsyncSession]) -> Dispatcher:
    dispatcher = Dispatcher()
    dispatcher.update.middleware(DatabaseSessionMiddleware(session_factory))
    dispatcher.include_router(start_router)
    dispatcher.include_router(onboarding_router)
    return dispatcher
