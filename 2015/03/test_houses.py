import pytest

from houses import houses, robot_santa


@pytest.mark.parametrize('house_route, house_count', [
    ('>', 2),
    ('^>v<', 4),
    ('^v^v^v^v^v', 2)
])
def test_houses(house_route, house_count):
    assert houses(house_route) == house_count


@pytest.mark.parametrize('house_route, house_count', [
    ('^v', 3),
    ('^>v<', 3),
    ('^v^v^v^v^v', 11)
])
def test_robot_santa(house_route, house_count):
    assert robot_santa(house_route) == house_count
