import pytest
import math
from aoc.maths import factorial, fibonacci, manhattan_distance, sign


@pytest.mark.parametrize(
    "n, expected",
    [(0, 1), (1, 1), (5, 120), (10, 3628800)],
    ids=["zero", "one", "small_number", "larger_number"],
)
def test_factorial(n, expected):
    # Act
    result = factorial(n)

    # Assert
    assert result == expected


@pytest.mark.parametrize(
    "n, f0, f1, expected",
    [(0, 0, 1, 0), (1, 0, 1, 1), (5, 0, 1, 5), (10, 0, 1, 55)],
    ids=["zero_iteration", "first_iteration", "small_iteration", "larger_iteration"],
)
def test_fibonacci(n, f0, f1, expected):
    # Act
    result = fibonacci(n, f0, f1)

    # Assert
    assert result == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [((0, 0), (3, 4), 7), ((1, 2), (4, 6), 7), ((-1, -2), (1, 2), 6)],
    ids=["origin_point", "positive_coordinates", "negative_coordinates"],
)
def test_manhattan_distance(a, b, expected):
    # Act
    result = manhattan_distance(a, b)

    # Assert
    assert result == expected


@pytest.mark.parametrize(
    "x, expected",
    [(0, 0), (5, 1), (-5, -1), (math.inf, 1), (-math.inf, -1)],
    ids=["zero", "positive", "negative", "positive_infinity", "negative_infinity"],
)
def test_sign(x, expected):
    # Act
    result = sign(x)

    # Assert
    assert result == expected
