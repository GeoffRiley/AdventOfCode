import pytest
from aoc.grid import Grid


@pytest.mark.parametrize(
    "default_value,expected",
    [(0, 0), (42, 42), (None, None)],
    ids=["default_zero", "default_number", "default_none"],
)
def test_grid_initialization(default_value, expected):
    # Arrange / Act
    grid = Grid(default_value)

    # Assert
    assert grid.default == expected
    assert grid.grid == {}
    assert grid._ranges == {}


@pytest.mark.parametrize(
    "input_coords,value,expected",
    [((1, 2), 10, 10), (3, 20, 20), ((0, 0, 0), 30, 30)],
    ids=["tuple_coords", "single_coord", "multi_dim_coords"],
)
def test_grid_set_and_get(input_coords, value, expected):
    # Arrange
    grid = Grid()

    # Act
    grid.set(value, input_coords)
    result = grid[input_coords]

    # Assert
    assert result == expected


def test_grid_copy():
    # Arrange
    original_grid = Grid()
    original_grid.set(42, (1, 2))

    # Act
    copied_grid = original_grid.copy()

    # Assert
    assert copied_grid.grid == original_grid.grid
    assert copied_grid.default == original_grid.default
    assert copied_grid is not original_grid


@pytest.mark.parametrize(
    "input_text,expected_values",
    [
        ("ABC", [("A", 0, 0), ("B", 1, 0), ("C", 2, 0)]),
        ("A\nB\nC", [("A", 0, 0), ("B", 0, 1), ("C", 0, 2)]),
    ],
    ids=["single_line", "multi_line"],
)
def test_grid_from_text(input_text, expected_values):
    # Act
    grid = Grid.from_text(input_text)

    # Assert
    for value, x, y in expected_values:
        assert grid[(x, y)] == value


def test_grid_delete():
    # Arrange
    grid = Grid()
    grid.set(42, (1, 2))

    # Act
    del grid[(1, 2)]

    # Assert
    assert (1, 2) not in grid.grid


def test_grid_contains():
    # Arrange
    grid = Grid()
    grid.set(42, (1, 2))

    # Assert
    assert (1, 2) in grid
    assert 3 not in grid


def test_grid_iteration():
    # Arrange
    grid = Grid()
    grid.set(10, (0, 0))
    grid.set(20, (1, 1))

    # Act
    values = list(grid)

    # Assert
    assert set(values) == {10, 20}


@pytest.mark.parametrize(
    "coords,axis,expected_min",
    [([(0, 0), (1, 1), (2, 2)], 0, 0), ([(0, 0), (1, 1), (2, 2)], 1, 0)],
    ids=["x_axis_min", "y_axis_min"],
)
def test_grid_axis_min(coords, axis, expected_min):
    # Arrange
    grid = Grid()
    for coord in coords:
        grid.set(1, coord)

    # Act
    result = grid.axis_min(axis)

    # Assert
    assert result == expected_min


@pytest.mark.parametrize(
    "coords,axis,expected_max",
    [([(0, 0), (1, 1), (2, 2)], 0, 2), ([(0, 0), (1, 1), (2, 2)], 1, 2)],
    ids=["x_axis_max", "y_axis_max"],
)
def test_grid_axis_max(coords, axis, expected_max):
    # Arrange
    grid = Grid()
    for coord in coords:
        grid.set(1, coord)

    # Act
    result = grid.axis_max(axis)

    # Assert
    assert result == expected_max


def test_grid_axis_size():
    # Arrange
    grid = Grid()
    grid.set(1, (0, 0))
    grid.set(1, (2, 2))

    # Act & Assert
    assert grid.width() == 3
    assert grid.height() == 3


@pytest.mark.parametrize(
    "location,diagonals,expected_neighbors",
    [
        ((1, 1), False, [(1, 0), (2, 1), (1, 2), (0, 1)]),
        (
            (1, 1),
            True,
            [(0, 0), (1, 0), (2, 0), (0, 1), (2, 1), (0, 2), (1, 2), (2, 2)],
        ),
    ],
    ids=["cardinal_neighbors", "diagonal_neighbors"],
)
def test_grid_neighbors(location, diagonals, expected_neighbors):
    # Arrange
    grid = Grid()

    # Act
    neighbors = list(grid.neighbors(location, diagonals=diagonals))

    # Assert
    assert set(neighbors) == set(expected_neighbors)


@pytest.mark.parametrize(
    "location,wrap,expected",
    [
        ((0, 0), False, (1, 0)),
        ((2, 0), False, (0, 1)),
        ((2, 2), False, None),
        ((0, 0), True, (1, 0)),
    ],
    ids=["next_location", "next_row", "no_next_location", "wrap_location"],
)
def test_grid_next_location(location, wrap, expected):
    # Arrange
    grid = Grid()
    grid.set(1, (0, 0))
    grid.set(1, (1, 0))
    grid.set(1, (2, 0))
    grid.set(1, (0, 1))
    grid.set(1, (1, 1))
    grid.set(1, (2, 1))
    grid.set(1, (0, 2))
    grid.set(1, (1, 2))
    grid.set(1, (2, 2))

    # Act
    result = grid.next_location(location, wrap=wrap)

    # Assert
    assert result == expected
