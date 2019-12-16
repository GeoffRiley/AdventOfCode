import pytest

from advent_coins import mine


@pytest.mark.parametrize('secret, answer', [
    ('abcdef', 609043),
    ('pqrstuv', 1048970)
])
def test_mine(secret, answer):
    assert mine(secret) == answer
