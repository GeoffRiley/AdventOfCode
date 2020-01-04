import pytest

from find_bunny_hq import how_far_to_bunny


@pytest.mark.parametrize('route, result', [
    ('R2, L3', 5),
    ('R2, R2, R2', 2),
    ('R5, L5, R5, R3', 12)
])
def test_how_far_to_bunny(route, result):
    assert how_far_to_bunny(route) == result
