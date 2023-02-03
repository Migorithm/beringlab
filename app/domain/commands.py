from dataclasses import dataclass


@dataclass(slots=True)
class CreateFibonacciWork:
    n: int
