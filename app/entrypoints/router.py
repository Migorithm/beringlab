from fastapi import APIRouter, Depends

from app.domain import commands
from app.service_layer import handlers, unit_of_work

from . import dependencies

router = APIRouter(tags=["Work"])


@router.post("/fibonacci")
async def create_fibonacci_work(
    n: int,
    unit_of_work: unit_of_work.AbstractUnitOfWork = Depends(
        dependencies.get_unit_of_work
    ),
):
    cmd = commands.CreateFibonacciWork(n=n)
    await handlers.BackgroundJob.create_work(cmd=cmd, sql_uow=unit_of_work)
    return "Work Done!"
