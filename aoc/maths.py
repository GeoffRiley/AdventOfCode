from functools import reduce
from operator import mul
from typing import Tuple


def factorial(n: int) -> int:
    """Calculate the Factorial of N."""
    if n < 1:
        return 1
    return reduce(mul, range(1, n + 1))


def fibonacci(n: int, f0: int = 0, f1: int = 1) -> int:
    """Calculate the Nth Fibonacci Number."""
    for _ in range(n):
        f0, f1 = f1, f0 + f1
    return f0


def manhattan_distance(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    """Return the Manhattan distance between two points."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def sign(x) -> int:
    """Return the sign of the argument.  [-1, 0, 1]"""
    return bool(x > 0) - bool(x < 0)
