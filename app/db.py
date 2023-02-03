from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.adapters import orm
from app.config import DB_INFO, STAGE

engine: AsyncEngine | None = None
autocommit_engine: AsyncEngine | None = None
async_transactional_session_factory: sessionmaker | None = None

if STAGE not in ("testing", "ci-testing"):
    engine = create_async_engine(DB_INFO.get_test_uri(), future=True)
    async_transactional_session_factory = sessionmaker(
        engine, expire_on_commit=False, autoflush=False, class_=AsyncSession
    )
    orm.start_mapper()
