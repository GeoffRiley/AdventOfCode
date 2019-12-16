import pytest

from not_quite_lisp import find_floor, find_basement_entry


@pytest.mark.parametrize('brackets, floor', [
    ('(())', 0),
    ('()()', 0),
    ('(((', 3),
    ('(()(()(', 3),
    ('))(((((', 3),
    ('())', -1),
    ('))(', -1),
    (')))', -3),
    (')())())', -3)
])
def test_find_floor(brackets, floor):
    assert find_floor(brackets) == floor


@pytest.mark.parametrize('brackets, position', [
    (')', 1),
    ('()())', 5)
])
def test_find_basement_entry(brackets, position):
    assert find_basement_entry(brackets) == position
