import pytest

from app.domain import commands
from app.service_layer import unit_of_work
from app.service_layer.handlers import BackgroundJob


@pytest.mark.asyncio
async def test_create_work(session_factory):
    # GIVEN
    cmd = commands.CreateFibonacciWork(1, 1, "1")
    sql_uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory=session_factory)
    await BackgroundJob.create_work(cmd, sql_uow=sql_uow)
    assert 1
