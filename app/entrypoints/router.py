from fastapi import APIRouter, Depends

from app.service_layer import handlers, unit_of_work

from . import dependencies

router = APIRouter(tags=["Work"])


@router.post("/fibonacci")
async def create_fibonacci_work(
    n: int,
):
    handlers.BackgroundJob.dispatch_fibonacci_work.delay(n=n)
    return "Work Done!"


@router.get("/fibonacci")
async def get_fibonacci_works(
    sql_uow: unit_of_work.SqlAlchemyUnitOfWork = Depends(dependencies.get_unit_of_work),
):
    work = await handlers.BackgroundJob.get_works(sql_uow=sql_uow)
    return work
