import os
from typing import Literal, cast

from pydantic import BaseSettings

STAGE = cast(
    Literal["local", "ci-testing", "testing", "develop", "staging", "production"],
    os.getenv("STAGE", "local"),
)


class DBInfo(BaseSettings):
    PROTOCOL: str = "sqlite+aiosqlite"
    SERVER: str = ""
    USER: str = ""
    PASSWORD: str = ""
    DB: str = ""
    PORT: str = ""

    def get_uri(self):
        return "{}://{}:{}@{}:{}/{}".format(
            self.PROTOCOL,
            self.USER,
            self.PASSWORD,
            self.SERVER,
            self.PORT,
            self.DB,
        )

    def get_test_uri(self):
        return "{}:///{}".format(self.PROTOCOL, "test.db")


DB_INFO = DBInfo()


CELERY_BROKER_URL: str = os.environ.get("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
CELERY_RESULT_BACKEND: str = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0"
)
