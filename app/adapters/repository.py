import abc
from typing import Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.selectable import Select

ModelType = TypeVar("ModelType", bound=object)


class AbstractRepository(abc.ABC):
    def add(self, model):
        self._add(model)

    @abc.abstractmethod
    def _add(self, model):
        ...

    async def get(self):
        return await self._get()

    @abc.abstractmethod
    async def _get(self):
        ...

    async def list(self):
        return await self._list()

    @abc.abstractmethod
    async def _list(self):
        ...


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, *, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self._base_query: Select = select(self.model)
        self.session = session

    def _add(self, model):
        self.session.add(model)
        return model

    async def _list(self):
        q = await self.session.execute(self._base_query)
        return q.scalars().all()

    async def _get(self):
        q = await self.session.execute(self._base_query.limit(1))
        return q.scalars().first()
