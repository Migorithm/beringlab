from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from app.adapters import queues
from app.entrypoints.router import router


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

    return app
