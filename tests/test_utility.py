import pytest
import re
from typing import List, Any

from aoc.utility import (
    to_list,
    extract_ints,
    to_list_int,
    lines_to_list,
    lines_to_list_int,
    sequence_to_int,
    grouped,
    pairwise,
    batched,
)


@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("a, b, c", ["a", "b", "c"]),
        ("x,y,z", ["x", "y", "z"]),
        (" a , b , c ", ["a", "b", "c"]),
    ],
    ids=["spaces_around_comma", "no_spaces", "extra_spaces"],
)
def test_to_list(input_str, expected):
    # Act
    result = to_list(input_str)

    # Assert
    assert result == expected


@pytest.mark.parametrize(
    "input_str,negative,expected",
    [
        ("abc 123 def", False, [123]),
        ("abc -123 def", True, [-123]),
        ("no numbers", False, []),
        ("multiple 45 and 67", False, [45, 67]),
    ],
    ids=["positive_int", "negative_int", "no_numbers", "multiple_ints"],
)
def test_extract_ints(input_str, negative, expected):
    # Act
    result = extract_ints(input_str, negative)

    # Assert
    assert result == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [("1,2,3", [1, 2, 3]), (" 4 , 5 , 6 ", [4, 5, 6])],
    ids=["simple_ints", "spaced_ints"],
)
def test_to_list_int(input_str, expected):
    # Act
    result = to_list_int(input_str)

    # Assert
    assert result == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [("a\nb\nc", ["a", "b", "c"]), ("x\ny\nz", ["x", "y", "z"])],
    ids=["simple_lines", "multiple_lines"],
)
def test_lines_to_list(input_str, expected):
    # Act
    result = lines_to_list(input_str)

    # Assert
    assert result == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [("1\n2\n3", [1, 2, 3]), ("4\n5\n6", [4, 5, 6])],
    ids=["simple_int_lines", "multiple_int_lines"],
)
def test_lines_to_list_int(input_str, expected):
    # Act
    result = lines_to_list_int(input_str)

    # Assert
    assert result == expected


@pytest.mark.parametrize(
    "input_str,expected",
    [("123", [1, 2, 3]), ("456", [4, 5, 6])],
    ids=["single_sequence", "another_sequence"],
)
def test_sequence_to_int(input_str, expected):
    # Act
    result = sequence_to_int(input_str)

    # Assert
    assert result == expected


@pytest.mark.parametrize(
    "iterable,n,expected",
    [([1, 2, 3, 4], 2, [(1, 2), (3, 4)]), ("ABCD", 2, [("A", "B"), ("C", "D")])],
    ids=["list_grouped", "string_grouped"],
)
def test_grouped(iterable, n, expected):
    # Act
    result = list(grouped(iterable, n))

    # Assert
    assert result == expected


@pytest.mark.parametrize(
    "iterable,expected",
    [
        ([1, 2, 3, 4], [(1, 2), (2, 3), (3, 4)]),
        ("ABCD", [("A", "B"), ("B", "C"), ("C", "D")]),
    ],
    ids=["list_pairwise", "string_pairwise"],
)
def test_pairwise(iterable, expected):
    # Act
    result = list(pairwise(iterable))

    # Assert
    assert result == expected


@pytest.mark.parametrize(
    "iterable,n,expected",
    [
        ("ABCDEFG", 3, [["A", "B", "C"], ["D", "E", "F"], ["G"]]),
        ([1, 2, 3, 4, 5], 2, [[1, 2], [3, 4], [5]]),
    ],
    ids=["string_batched", "list_batched"],
)
def test_batched(iterable, n, expected):
    # Act
    result = list(batched(iterable, n))

    # Assert
    assert result == expected


def test_batched_invalid_batch_size():
    # Assert
    with pytest.raises(ValueError, match="Batch size must be greater than 1."):
        # Act
        list(batched([1, 2, 3], 0))
