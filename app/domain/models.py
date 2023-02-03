import abc
import time
from dataclasses import dataclass, field
from datetime import datetime
from functools import singledispatchmethod

from app.domain import commands

# Models are implemented with plain old python object
# so it dispenses with thirdparty dependencies


class Base(abc.ABCMeta):
    """
    Abstact base class for domain models
    """

    @classmethod
    def create(cls, msg):
        return cls._create(msg)

    @classmethod
    def _create(cls, msg):
        raise NotImplementedError


@dataclass(eq=False)
class Work:
    timestamp: datetime = field(init=False)
    n: int
    result: int
    elapsed_time: str

    @singledispatchmethod
    @classmethod
    def execute(cls, msg):
        """
        This is to dispatch works to relavent domain methods,
        particulary for things that are not instance-specific.
        """
        raise NotImplementedError("Cannot negate a")

    @execute.register
    @classmethod
    def _create(cls, msg: commands.CreateFibonacciWork):
        tick = time.time()
        return cls(
            n=msg.n,
            result=cls.fibonacci(msg.n),
            elapsed_time=str(time.time() - tick),
        )

    # the job is defined here because this is the work of business interest
    @staticmethod
    def fibonacci(n):
        return 1 if n <= 1 else Work.fibonacci(n - 1) + Work.fibonacci(n - 2)
