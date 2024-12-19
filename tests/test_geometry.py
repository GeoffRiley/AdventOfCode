import pytest
from aoc.geometry import Size, Point, Rectangle


# Size Tests
@pytest.mark.parametrize(
    "cx1,cy1,cx2,cy2,expected_cx,expected_cy",
    [(1, 2, 3, 4, 4, 6), (0, 0, 5, 5, 5, 5), (-1, -2, 1, 2, 0, 0)],
    ids=["positive_values", "zero_values", "mixed_values"],
)
def test_size_addition(cx1, cy1, cx2, cy2, expected_cx, expected_cy):
    # Arrange
    size1 = Size(cx1, cy1)
    size2 = Size(cx2, cy2)

    # Act
    result = size1 + size2

    # Assert
    assert result.cx == expected_cx
    assert result.cy == expected_cy


@pytest.mark.parametrize(
    "cx1,cy1,cx2,cy2,expected_cx,expected_cy",
    [(5, 6, 3, 4, 2, 2), (10, 10, 5, 5, 5, 5), (1, 2, 3, 4, -2, -2)],
    ids=["positive_subtraction", "equal_values", "negative_result"],
)
def test_size_subtraction(cx1, cy1, cx2, cy2, expected_cx, expected_cy):
    # Arrange
    size1 = Size(cx1, cy1)
    size2 = Size(cx2, cy2)

    # Act
    result = size1 - size2

    # Assert
    assert result.cx == expected_cx
    assert result.cy == expected_cy


# Point Tests


# Property Tests
def test_point_properties():
    # Arrange
    point = Point(3, 4)

    # Act & Assert
    assert point.real == 3
    assert point.imag == 4


# Offset Tests
@pytest.mark.parametrize(
    "x,y,x_offset,y_offset,expected_x,expected_y",
    [(0, 0, 1, 2, 1, 2), (5, 5, -3, -2, 2, 3), (-1, -1, 2, 3, 1, 2)],
    ids=["zero_start", "positive_offset", "negative_start"],
)
def test_point_offset(x, y, x_offset, y_offset, expected_x, expected_y):
    # Arrange
    point = Point(x, y)

    # Act
    point.offset(x_offset, y_offset)

    # Assert
    assert point.x == expected_x
    assert point.y == expected_y


# Negation Tests
@pytest.mark.parametrize(
    "x,y,expected_x,expected_y",
    [(1, 2, -1, -2), (0, 0, 0, 0), (-3, -4, 3, 4)],
    ids=["positive_values", "zero_values", "negative_values"],
)
def test_point_negation(x, y, expected_x, expected_y):
    # Arrange
    point = Point(x, y)

    # Act
    result = -point

    # Assert
    assert result.x == expected_x
    assert result.y == expected_y


# Addition Tests
@pytest.mark.parametrize(
    "x1,y1,other,expected_x,expected_y",
    [
        (1, 2, Point(3, 4), 4, 6),
        (0, 0, 5, 5, 0),
        (1, 2, complex(3, 4), 4, 6),
        (5, 5, 2, 7, 5),
    ],
    ids=["point_addition", "number_addition", "complex_addition", "scalar_addition"],
)
def test_point_addition(x1, y1, other, expected_x, expected_y):
    # Arrange
    point = Point(x1, y1)

    # Act
    result = point + other

    # Assert
    assert result.x == expected_x
    assert result.y == expected_y


# Subtraction Tests
@pytest.mark.parametrize(
    "x1,y1,other,expected_x,expected_y",
    [(5, 6, Point(3, 4), 2, 2), (10, 10, 5, 5, 10), (1, 2, complex(3, 4), -2, -2)],
    ids=["point_subtraction", "number_subtraction", "complex_subtraction"],
)
def test_point_subtraction(x1, y1, other, expected_x, expected_y):
    # Arrange
    point = Point(x1, y1)

    # Act
    result = point - other

    # Assert
    assert result.x == expected_x
    assert result.y == expected_y


# Multiplication Tests
@pytest.mark.parametrize(
    "x1,y1,other,expected_x,expected_y",
    [(2, 3, Point(4, 5), -7, 22), (1, 2, 3, 3, 6), (1, 2, complex(3, 4), -5, 10)],
    ids=["point_multiplication", "scalar_multiplication", "complex_multiplication"],
)
def test_point_multiplication(x1, y1, other, expected_x, expected_y):
    # Arrange
    point = Point(x1, y1)

    # Act
    result = point * other

    # Assert
    assert result.x == expected_x
    assert result.y == expected_y


# Modulo Tests
@pytest.mark.parametrize(
    "x1,y1,other,expected_x,expected_y",
    [(7, 8, 3, 1, 2), (10, 15, Point(4, 6), 2, 3), (7, 8, 5, 2, 3)],
    ids=["scalar_modulo", "point_modulo", "another_scalar_modulo"],
)
def test_point_modulo(x1, y1, other, expected_x, expected_y):
    # Arrange
    point = Point(x1, y1)

    # Act
    result = point % other

    # Assert
    assert result.x == expected_x
    assert result.y == expected_y


# Complex Conversion Tests
def test_point_complex_conversion():
    # Arrange
    point = Point(3, 4)

    # Act
    result = complex(point)

    # Assert
    assert result == complex(3, 4)


# Manhattan Distance Tests
@pytest.mark.parametrize(
    "x1,y1,x2,y2,expected_distance",
    [(0, 0, 3, 4, 7), (1, 1, 4, 5, 7), (-1, -1, 2, 2, 6)],
    ids=["positive_coordinates", "offset_coordinates", "negative_coordinates"],
)
def test_point_manhattan_distance(x1, y1, x2, y2, expected_distance):
    # Arrange
    point1 = Point(x1, y1)
    point2 = Point(x2, y2)

    # Act
    result = point1.manhattan_distance(point2)

    # Assert
    assert result == expected_distance


# From Complex Tests
@pytest.mark.parametrize(
    "complex_num,expected_x,expected_y",
    [(complex(3.7, 4.2), 3, 4), (complex(-1.6, 2.8), -1, 2), (complex(0, 0), 0, 0)],
    ids=["positive_complex", "mixed_complex", "zero_complex"],
)
def test_point_from_complex(complex_num, expected_x, expected_y):
    # Act
    result = Point.from_complex(complex_num)

    # Assert
    assert result.x == expected_x
    assert result.y == expected_y


# Iteration Tests
def test_point_iteration():
    # Arrange
    point = Point(3, 4)

    # Act
    result = list(point)

    # Assert
    assert result == [3, 4]


# Rectangle Tests
@pytest.mark.parametrize(
    "left,top,right,bottom,expected_width,expected_height",
    [(0, 0, 5, 5, 5, 5), (2, 3, 7, 8, 5, 5), (-1, -1, 4, 4, 5, 5)],
    ids=["zero_origin", "positive_offset", "negative_origin"],
)
def test_rectangle_dimensions(
    left, top, right, bottom, expected_width, expected_height
):
    # Arrange
    rect = Rectangle(left, top, right, bottom)

    # Act & Assert
    assert rect.width() == expected_width
    assert rect.height() == expected_height


@pytest.mark.parametrize(
    "left,top,right,bottom,x,y,expected_center_x,expected_center_y",
    [(0, 0, 10, 10, 5, 5, 5, 5), (2, 3, 7, 8, 4, 5, 4, 5), (-1, -1, 4, 4, 1, 1, 1, 1)],
    ids=["zero_origin", "positive_offset", "negative_origin"],
)
def test_rectangle_center_point(
    left, top, right, bottom, x, y, expected_center_x, expected_center_y
):
    # Arrange
    rect = Rectangle(left, top, right, bottom)

    # Act
    center = rect.center_point()

    # Assert
    assert center.x == expected_center_x
    assert center.y == expected_center_y


def test_rectangle_invalid_addition():
    # Arrange
    rect = Rectangle(0, 0, 5, 5)

    # Assert
    with pytest.raises(TypeError):
        # Act
        rect + 5
