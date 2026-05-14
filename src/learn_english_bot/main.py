import asyncio
import logging

from aiogram import Bot

from learn_english_bot.bot.app import create_dispatcher
from learn_english_bot.config import get_settings
from learn_english_bot.db.session import (
    create_database_schema,
    create_engine,
    create_session_factory,
)
from learn_english_bot.logging_config import configure_logging

logger = logging.getLogger(__name__)


async def run_bot() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)

    engine = create_engine(settings.database_url)
    await create_database_schema(engine)
    session_factory = create_session_factory(engine)

    bot = Bot(token=settings.bot_token)
    dispatcher = create_dispatcher(session_factory)

    logger.info("Starting bot", extra={"environment": settings.environment})
    try:
        await dispatcher.start_polling(bot)
    finally:
        await bot.session.close()
        await engine.dispose()


def cli() -> None:
    asyncio.run(run_bot())


if __name__ == "__main__":
    cli()
