import time

from asgiref.sync import async_to_sync
from celery import shared_task

from app.domain import commands, models
from app.service_layer import unit_of_work


class BackgroundJob:
    @staticmethod
    @shared_task
    def dispatch_fibonacci_work(n):
        tick = time.time()
        result = models.Work.fibonacci(n)
        elapsed_time = str(time.time() - tick)
        cmd = commands.CreateFibonacciWork(
            n=n, result=result, elapsed_time=elapsed_time
        )
        sql_uow = unit_of_work.SqlAlchemyUnitOfWork()
        # Currently, celery doesn't natively support coroutine call, so I resorted to using the following.
        async_to_sync(BackgroundJob.create_work)(cmd, sql_uow=sql_uow)

    @staticmethod
    async def create_work(
        cmd: commands.CreateFibonacciWork, *, sql_uow: unit_of_work.SqlAlchemyUnitOfWork
    ):
        async with sql_uow:
            work = models.Work.execute(cmd)
            sql_uow.works.add(work)
            await sql_uow.commit()

    @staticmethod
    async def get_works(*, sql_uow: unit_of_work.SqlAlchemyUnitOfWork):
        async with sql_uow:
            works: list[models.Work] = await sql_uow.works.list()

            return [
                dict(
                    n=w.n,
                    result=w.result,
                    elapsed_time=w.elapsed_time,
                    timestamp=w.timestamp,
                )
                for w in works
            ]
