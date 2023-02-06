from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from app.adapters import orm, queues
from app.db import engine
from app.entrypoints.router import router


# create_app is a factory function,
# which can be called multiple times, that returns a FastAPI app for us to use.
# This is located in entrypoints so we can allow for other entries
def create_app() -> FastAPI:
    """
    Application factory for initializing app
    """
    app = FastAPI(title="BeringLab: Service")

    class APIExceptionErrorCodes:
        SCHEMA_ERROR = ("schema_error", status.HTTP_422_UNPROCESSABLE_ENTITY)

    setattr(app, "celery_app", queues.create_celery())

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=APIExceptionErrorCodes.SCHEMA_ERROR[1],
            content={
                "error": {
                    "message": "schema error. please refer to data for details",
                    "type": "validation",
                    "code": APIExceptionErrorCodes.SCHEMA_ERROR[0],
                    "data": exc.errors(),
                }
            },
        )

    app.include_router(router)

    # This is for test
    @app.on_event("startup")
    async def db_craete():
        assert engine
        async with engine.begin() as conn:
            # await conn.execute(sa.text(drop_stmt))
            await conn.run_sync(orm.metadata.create_all)

    return app
