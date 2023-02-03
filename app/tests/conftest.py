import asyncio
import sys

import pytest
import pytest_asyncio
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

from app import config
from app.adapters import orm


@pytest.fixture(scope="session")
def event_loop():
    """
    Creates an instance of the default event loop for the test session
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()

    # In case you are working on windows
    if sys.platform.lower().startswith("win") and sys.version_info[:2] >= (3, 8):
        # Avoid "RuntimeError: Event loop is closed" on Windows when tearing down tests
        # https://github.com/encode/httpx/issues/914
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def aio_engine():
    engine = create_async_engine(
        config.DB_INFO.get_test_uri(),
        future=True,
    )
    async with engine.begin() as conn:
        drop_stmt = f"DROP TABLE IF EXISTS {','.join(orm.metadata.tables.keys())};"
        await conn.execute(sa.text(drop_stmt))

        await conn.run_sync(orm.metadata.create_all)
    orm.start_mapper()
    yield engine
    clear_mappers()


@pytest_asyncio.fixture(scope="function")
async def session_factory(aio_engine: AsyncEngine):
    _session_factory: sessionmaker = sessionmaker(
        aio_engine, expire_on_commit=False, autoflush=False, class_=AsyncSession
    )
    yield _session_factory
    async with _session_factory() as session_:
        for trx_table in orm.metadata.tables.keys():
            truncate_stmt = f"DELETE FROM {trx_table};"
            # truncate_stmt = f"TRUNCATE TABLE {trx_table} CASCADE;"
            await session_.execute(sa.text(truncate_stmt))

        await session_.commit()


@pytest_asyncio.fixture(scope="function")
async def session(session_factory: sessionmaker):
    async with session_factory() as session_:
        yield session_
        for trx_table in orm.metadata.tables.keys():
            truncate_stmt = f"DELETE FROM {trx_table};"
            # truncate_stmt = f"TRUNCATE TABLE {trx_table} CASCADE;"
            await session_.execute(sa.text(truncate_stmt))

        await session_.commit()
