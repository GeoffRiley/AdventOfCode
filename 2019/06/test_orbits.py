import pytest

from orbits import orbit_count, indirect_orbits, orbit_transfer_count, MAP, MAP2


@pytest.mark.parametrize('element, count', [
    ('D', 3),
    ('L', 7),
    ('COM', 0)
])
def test_orbit_count(element, count):
    assert orbit_count(MAP, element) == count


def test_indirect_orbits():
    assert indirect_orbits(MAP) == 42


def test_orbit_transfer_count():
    assert orbit_transfer_count(MAP2, 'YOU', 'SAN') == 4
