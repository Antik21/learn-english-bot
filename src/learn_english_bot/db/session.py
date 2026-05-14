from importlib import import_module
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from learn_english_bot.db.base import Base


def ensure_sqlite_directory(database_url: str) -> None:
    prefix = "sqlite+aiosqlite:///"
    if not database_url.startswith(prefix):
        return

    database_path = database_url.removeprefix(prefix)
    if database_path in {":memory:", ""}:
        return

    Path(database_path).parent.mkdir(parents=True, exist_ok=True)


def create_engine(database_url: str) -> AsyncEngine:
    ensure_sqlite_directory(database_url)
    return create_async_engine(database_url)


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(engine, expire_on_commit=False)


async def create_database_schema(engine: AsyncEngine) -> None:
    import_module("learn_english_bot.db.models")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
