from dataclasses import dataclass
from numbers import Complex, Number, Real
from types import NotImplementedType
from typing import Any, Generator, Union


@dataclass
class Size:
    """A height and width in 2-dimensional space.

    Attributes:
        cx : int
            The width component of the Size.
        cy : int
            The height component of the Size.

    Methods
        __add__
        __sub__
    """

    cx: int = 0
    cy: int = 0

    def __add__(self, other: "Size") -> "Size":
        """Return the sum of two sizes."""
        return Size(self.cx + other.cx, self.cy + other.cy)

    def __sub__(self, other: "Size") -> "Size":
        """Return the difference of two sizes."""
        return Size(self.cx - other.cx, self.cy - other.cy)


class Point(tuple):
    """A point in 2-dimensional space.

    Attributes:
        x: int
            horizontal offset
        y: int
            vertical offset

    Methods:
        offset
        __sub__
        __add__
        manhattan_distance
    """

    x: int = 0
    y: int = 0

    def __new__(cls, x: int, y: int):
        return super().__new__(cls, (x, y))

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @property
    def real(self) -> int:
        return self.x

    @property
    def imag(self) -> int:
        return self.y

    def offset(self, x_offset: int, y_offset: int) -> None:
        """Offset the point by the given values."""
        self.x += x_offset
        self.y += y_offset

    def __neg__(self) -> "Point":
        """-self"""
        x, y = self
        return type(self)(-x, -y)

    def __sub__(self, other: Union["Point", complex, int]) -> "Point":
        """self - other"""
        return self + (-other)

    def __rsub__(self, other: Union["Point", complex, int]) -> "Point":
        """other - self"""
        return (type(self)(0, 0) + other) + (-self)

    def __add__(self, other) -> Union[NotImplementedType, "Point"]:
        """Return the sum of two points."""
        x, y = self
        if isinstance(other, (type(self), tuple)):
            ox, oy = other
        elif isinstance(other, Real):
            ox, oy = other, 0
        elif isinstance(other, Complex):
            ox, oy = self.from_complex(other)
        elif isinstance(other, Number):
            ox, oy = other, 0
        else:
            return NotImplemented
        return type(self)(x + ox, y + oy)

    __radd__ = __add__

    def __mul__(self, other):
        """
        self * other

        points multiply with one another like complex numbers
        """
        new = type(self)
        x, y = self
        if isinstance(other, (type(self), tuple)):
            ox, oy = other
        elif isinstance(other, Real):
            return new(x * other, y * other)
        elif isinstance(other, Complex):
            ox, oy = self.from_complex(other)
        elif isinstance(other, Number):
            return new(x * other, y * other)
        else:
            return NotImplemented

        return new(x * ox - y * oy, x * oy + y * ox)

    __rmul__ = __mul__

    def __mod__(self, other: Union[int, "Point", tuple[int, int]]) -> "Point":
        """
        self % otro
        if other is a number apply the mod to each coordinate
        if other is a Point apply the mod point-wise ( Point(self.x % otro.x, self.y % otro.y) )
        """
        if isinstance(other, int):
            return type(self)(self.x % other, self.y % other)
        if isinstance(other, (tuple, type(self))):
            ox, oy = other
            return type(self)(self.x % ox, self.y % oy)
        return NotImplemented

    def __complex__(self) -> complex:
        return complex(self.x, self.y)

    def __divmod__(
        self, other: Union[int, "Point", tuple[int, int]]
    ) -> tuple["Point", "Point"]:
        """divmod(self, other)"""
        if isinstance(other, int):
            x, y = self
            dx, mx = divmod(x, other)
            dy, my = divmod(y, other)
            return Point(dx, dy), Point(mx, my)
        if isinstance(other, (tuple, type(self))):
            x, y = self
            ox, oy = other
            dx, mx = divmod(x, ox)
            dy, my = divmod(y, oy)
            return Point(dx, dy), Point(mx, my)
        return NotImplemented

    def __rdivmod__(
        self, other: Union[int, "Point", tuple[int, int]]
    ) -> tuple["Point", "Point"]:
        """divmod(other, self)"""
        if isinstance(other, int):
            x, y = self
            dx, mx = divmod(other, x)
            dy, my = divmod(other, y)
            return Point(dx, dy), Point(mx, my)
        if isinstance(other, (tuple, type(self))):
            x, y = self
            ox, oy = other
            dx, mx = divmod(ox, x)
            dy, my = divmod(oy, y)
            return Point(dx, dy), Point(mx, my)
        return NotImplemented

    def __getitem__(self, item):
        """Return the x or y value."""
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise IndexError("Index out of range.")

    def __setitem__(self, key, value):
        """Set the x or y value."""
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError("Index out of range.")

    def __len__(self):
        """Return the number of dimensions."""
        return 2

    def __eq__(self, other):
        """Return True if the x and y values are equal."""
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __iter__(self) -> Generator[int, Any, None]:
        """Yield the x and y values."""
        yield self.x
        yield self.y

    def manhattan_distance(self, other) -> int:
        """Calculate the Manhattan distance between `self` and `other`."""
        return abs(self.x - other.x) + abs(self.y - other.y)

    @classmethod
    def from_complex(cls, number: Complex) -> "Point":
        """return an integer point from the given complex number"""
        return cls(int(number.real), int(number.imag))


@dataclass
class Point3:
    """A point in 3-dimensional space.

    Attributes:
        x: int
            horizontal offset
        y: int
            vertical offset
        z: int
            depth offset

    Methods:
        offset
        __sub__
        __add__
        manhattan_distance
    """

    x: int = 0
    y: int = 0
    z: int = 0

    def offset(self, x_offset: int, y_offset: int, z_offset: int):
        """Offset the point by the given values."""
        self.x += x_offset
        self.y += y_offset
        self.z += z_offset

    def __sub__(self, rhs):
        """Return the difference of two points."""
        return Point3(self.x - rhs.x, self.y - rhs.y, self.z - rhs.z)

    def __add__(self, rhs):
        """Return the sum of two points."""
        return Point3(self.x + rhs.x, self.y + rhs.y, self.z + rhs.z)

    def __mul__(self, other):
        """Increase the magnitude of all dimensions."""
        return Point3(self.x * other, self.y * other, self.z * other)

    def __iter__(self):
        """Yield the x, y, and z values."""
        yield self.x
        yield self.y
        yield self.z

    def manhattan_distance(self, other) -> int:
        """Calculate the Manhattan distance between `self` and `other`."""
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)


@dataclass
class Rectangle:
    """A rectangle in 2-dimensional space.

    Attributes:
        left: int
        top: int
        right: int
        bottom: int
            offsets for the various rectangle positions

    Methods:
        bottom_right
        center_point
        top_left
        width
        height
        deflate
        deflate_rect
        inflate
        inflate_rect
        intersect
        is_empty
        is_null
        move_to_x
        move_to_y
        move_to_xy
        normalize
        offset
        __add__
        __sub__
        pt_in_rect
        set_empty
        set_position
        size
        union
    """

    left: int = 0
    top: int = 0
    right: int = 0
    bottom: int = 0

    def bottom_right(self) -> Point:
        """Return the bottom-right point of the rectangle."""
        return Point(self.right, self.bottom)

    def center_point(self) -> Point:
        """Return the center point of the rectangle."""
        return Point(self.left + (self.width() // 2), self.top + (self.height() // 2))

    def top_left(self) -> Point:
        """Return the top-left point of the rectangle."""
        return Point(self.left, self.top)

    def width(self) -> int:
        """Return the width of the rectangle."""
        return self.right - self.left

    def height(self) -> int:
        """Return the height of the rectangle."""
        return self.bottom - self.top

    def deflate(self, cx: int, cy: int) -> None:
        """Deflate the rectangle by moving the sides towards the center."""
        self.left += cx
        self.top += cy
        self.right -= cx
        self.bottom -= cy

    def deflate_rect(self, rhs) -> None:
        """Deflate the rectangle by moving the sides towards the center."""
        self.left += rhs.left
        self.top += rhs.top
        self.right -= rhs.right
        self.bottom -= rhs.bottom

    def inflate(self, cx: int, cy: int) -> None:
        """Inflate the rectangle by moving the sides away from the center."""
        self.left -= cx
        self.top -= cy
        self.right += cx
        self.bottom += cy

    def inflate_rect(self, rhs) -> None:
        """Inflate the rectangle by moving the sides away from the center."""
        self.left -= rhs.left
        self.top -= rhs.top
        self.right += rhs.right
        self.bottom += rhs.bottom

    def intersect(self, other):
        """Create a rectangle equal to the intersection of the given rectangles."""
        return Rectangle(
            max(self.left, other.left),
            max(self.top, other.top),
            min(self.right, other.right),
            min(self.bottom, other.bottom),
        )

    def is_empty(self) -> bool:
        """Return True if the rectangle height and or width are <= 0."""
        return self.height() <= 0 or self.width() <= 0

    def is_null(self) -> bool:
        """Return True if all values in the rectangle are 0."""
        return self.left == 0 and self.top == 0 and self.right == 0 and self.bottom == 0

    def move_to_x(self, x: int) -> None:
        """Move the rectangle to the absolute coordinate specified by x."""
        self.right = self.width() + x
        self.left = x

    def move_to_y(self, y: int) -> None:
        """Move the rectangle to the absolute coordinate specified by y."""
        self.bottom = self.height() + y
        self.top = y

    def move_to_xy(self, x: int, y: int) -> None:
        """Move the rectangle to the absolute x- and y- coordinates specified."""
        self.move_to_x(x)
        self.move_to_y(y)

    def normalize(self) -> None:
        """Normalizes the rectangle so both the height and the width are positive."""
        if self.left > self.right:
            self.left, self.right = self.right, self.left
        if self.top > self.bottom:
            self.top, self.bottom = self.bottom, self.top

    def offset(self, x_offset: int, y_offset: int) -> None:
        """Offset the point by the given values."""
        self.left += x_offset
        self.top += y_offset
        self.right += x_offset
        self.bottom += y_offset

    def __add__(self, rhs):
        """Displace the rectangle by the specified offsets."""
        new_rect = self
        if isinstance(rhs, Point):
            new_rect.left += rhs.x
            new_rect.top += rhs.y
            new_rect.right += rhs.x
            new_rect.bottom += rhs.y
        elif isinstance(rhs, Rectangle):
            new_rect.left += rhs.left
            new_rect.top += rhs.top
            new_rect.right += rhs.right
            new_rect.bottom += rhs.bottom
        else:
            raise TypeError("rhs must be a Point or a Rect.")
        return new_rect

    def __sub__(self, rhs):
        """Displace the rectangle by the specified offsets."""
        new_rect = self
        if isinstance(rhs, Point):
            new_rect.left -= rhs.x
            new_rect.top -= rhs.y
            new_rect.right -= rhs.x
            new_rect.bottom -= rhs.y
        elif isinstance(rhs, Rectangle):
            new_rect.left -= rhs.left
            new_rect.top -= rhs.top
            new_rect.right -= rhs.right
            new_rect.bottom -= rhs.bottom
        else:
            raise TypeError("rhs must be a Point or a Rect.")
        return new_rect

    def pt_in_rect(self, point: Point) -> bool:
        """Returns True if the given point is inside the rectangle."""
        return self.left <= point.x <= self.right and self.top <= point.y <= self.bottom

    def set_empty(self) -> None:
        """Make a null rectangle by setting all coordinates to zero."""
        self.left = 0
        self.top = 0
        self.right = 0
        self.bottom = 0

    def set_position(self, left: int, top: int, right: int, bottom: int) -> None:
        """Set the dimension of the rectangle."""
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def size(self) -> Size:
        """Get a Size object representing the width and height of the rectangle."""
        return Size(self.width(), self.height())

    def union(self, other):
        """Make a rectangle that is a union of the two given rectangles."""
        return Rectangle(
            min(self.left, other.left),
            min(self.top, other.top),
            max(self.right, other.right),
            max(self.bottom, other.bottom),
        )
