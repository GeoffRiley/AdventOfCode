import pytest
from aoc.edge import Edge


@pytest.mark.parametrize(
    "u, v, expected_str",
    [(1, 2, "1 -> 2"), (0, 5, "0 -> 5"), (-3, 10, "-3 -> 10")],
    ids=["positive_vertices", "zero_vertex", "negative_vertex"],
)
def test_edge_str(u, v, expected_str):
    # Arrange
    edge = Edge(u, v)

    # Act
    result = str(edge)

    # Assert
    assert result == expected_str


@pytest.mark.parametrize(
    "u, v, expected_reversed_u, expected_reversed_v",
    [(1, 2, 2, 1), (0, 5, 5, 0), (-3, 10, 10, -3)],
    ids=["positive_vertices", "zero_vertex", "negative_vertex"],
)
def test_edge_reversed(u, v, expected_reversed_u, expected_reversed_v):
    # Arrange
    edge = Edge(u, v)

    # Act
    reversed_edge = edge.reversed()

    # Assert
    assert reversed_edge.u == expected_reversed_u
    assert reversed_edge.v == expected_reversed_v
