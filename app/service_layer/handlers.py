from celery import shared_task

from app.domain import commands, models
from app.service_layer import unit_of_work


class BackgroundJob:
    @classmethod
    @shared_task
    async def create_work(
        cls,
        cmd: commands.CreateFibonacciWork,
        *,
        sql_uow: unit_of_work.SqlAlchemyUnitOfWork
    ):
        async with sql_uow:
            work = models.Work.execute(cmd)
            sql_uow.works.add(work)
            await sql_uow.commit()
