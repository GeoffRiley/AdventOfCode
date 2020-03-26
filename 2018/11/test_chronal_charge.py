import pytest
from chronal_charge import cell_power_level


@pytest.mark.parametrize('x, y, grid_serial, pwr', [
    (3, 5, 8, 4),
    (122, 79, 57, -5),
    (217, 196, 39, 0),
    (101, 153, 71, 4)
])
def test_cell_power_level(x, y, grid_serial, pwr):
    assert cell_power_level(x, y, grid_serial) == pwr
