import httpx
import pytest
import sqlalchemy as sa

from app.domain import commands
from app.entrypoints import dependencies
from app.main import app
from app.service_layer import unit_of_work
from app.service_layer.handlers import BackgroundJob


@pytest.mark.asyncio
async def test_create_work(session_factory):
    session = session_factory()
    q = await session.execute(sa.text("SELECT * FROM test_work"))
    res = q.fetchall()
    assert not res
    session.close()

    url = app.url_path_for("create_fibonacci_work")
    app.dependency_overrides[
        dependencies.get_unit_of_work
    ] = lambda: unit_of_work.SqlAlchemyUnitOfWork(session_factory=session_factory)

    async with httpx.AsyncClient(app=app, base_url="http://test") as cl:
        res = await cl.post(url=url, params=dict(n=20))

    assert res.json() == "Work Done!"

    session = session_factory()
    q = await session.execute(sa.text("SELECT * FROM test_work"))
    res = q.fetchall()

    session.close()
