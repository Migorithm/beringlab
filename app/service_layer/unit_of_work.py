import abc

from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters import repository
from app.db import async_transactional_session_factory
from app.domain import models

DEFAULT_ALCHEMY_TRANSACTIONAL_SESSION_FACTORY = async_transactional_session_factory


class AbstractUnitOfWork(abc.ABC):
    async def __aenter__(self):
        return self

    async def commit(self):
        await self._commit()

    @abc.abstractmethod
    async def _commit(self):
        raise NotImplementedError

    async def rollback(self):
        await self._rollback()

    @abc.abstractmethod
    async def _rollback(self):
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=None):
        self.session_factory = (
            DEFAULT_ALCHEMY_TRANSACTIONAL_SESSION_FACTORY
            if session_factory is None
            else session_factory
        )

    async def __aenter__(self):
        self.session: AsyncSession = self.session_factory()
        self.works = repository.SqlAlchemyRepository(
            model=models.Work, session=self.session
        )
        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def _commit(self):
        await self.session.commit()

    async def _rollback(self):
        await self.session.rollback()
