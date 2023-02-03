import datetime as dt

import sqlalchemy as sa
from sqlalchemy.orm import registry
from sqlalchemy.types import DateTime, TypeDecorator

from app.domain import models

metadata = sa.MetaData()
mapper_registry = registry(metadata=metadata)


# Type Decorator To Convert Time-naive to Time-aware
class TimeStamp(TypeDecorator):
    impl = DateTime
    LOCAL_TIMEZONE = dt.datetime.utcnow().astimezone().tzinfo
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if value.tzinfo is None:
            value = value.astimezone(self.LOCAL_TIMEZONE)

        return value.astimezone(dt.timezone.utc)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if value.tzinfo is None:
            return value.replace(tzinfo=dt.timezone.utc)

        return value.astimezone(dt.timezone.utc)


works = sa.Table(
    "test_work",
    mapper_registry.metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column(
        "timestamp", TimeStamp(), default=sa.func.now(), server_default=sa.func.now()
    ),
    sa.Column("n", sa.Integer),
    sa.Column("result", sa.Integer, nullable=False),
    sa.Column("elapsed_time", sa.String, nullable=False),
)


# to imperatively map domain models to persistent models
def start_mapper():
    mapper_registry.map_imperatively(models.Work, works)
