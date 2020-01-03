import pytest
from fuel_check import (fuel_for_mass, fuel_addition)


@pytest.mark.parametrize('mass, fuel', [
    (12, 2),
    (14, 2),
    (1969, 654),
    (100756, 33583)
])
def test_fuel_for_mass(mass, fuel):
    assert fuel_for_mass(mass) == fuel


@pytest.mark.parametrize('mass, fuel', [
    (12, 2),
    (14, 2),
    (1969, 966),
    (100756, 50346)
])
def test_fuel_addition(mass, fuel):
    assert fuel_addition(mass) == fuel


if __name__ == '__main__':
    pytest.main()
