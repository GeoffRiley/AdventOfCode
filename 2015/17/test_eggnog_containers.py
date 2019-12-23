import pytest

from eggnog_containers import how_many_ways


@pytest.mark.parametrize('qty, containers, ways', [
    (25, [20, 15, 10, 5, 5], 4)
])
def test_how_many_ways(qty, containers, ways):
    assert how_many_ways(qty, containers) == ways
