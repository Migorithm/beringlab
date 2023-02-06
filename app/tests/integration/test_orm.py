import pytest
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from app.adapters import orm


@pytest.mark.asyncio
async def test_create_tables(aio_engine: AsyncEngine):
    """
    To test if ORM integration was successful.
    """

    # GIVEN
    def get_table_names(conn):
        inspector = sa.inspect(conn)
        return inspector.get_table_names()

    # WHEN
    async with aio_engine.connect() as connection:
        table_names = await connection.run_sync(get_table_names)
        for table in orm.metadata.tables.keys():
            # THEN
            assert table in table_names


@pytest.mark.asyncio
async def test_session(session_factory):
    """
    To test if session object works properly.
    Record for test_work table is inserted first
    And it is then queried.
    """

    session: AsyncSession
    async with session_factory() as session:
        # GIVEN
        await session.execute(
            sa.text(
                """
            INSERT INTO test_work (n,result,elapsed_time)
            VALUES (1,1,'1');
            """
            )
        )
        # WHEN
        q = await session.execute(
            sa.text(
                """
            SELECT * FROM test_work limit 1
        """
            )
        )
        res = q.fetchall()

        # THEN
        assert res
        record = next(r for r in res)
        assert record.n == 1
        assert record.result == 1
        assert record.elapsed_time == "1"
