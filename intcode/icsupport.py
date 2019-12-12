import math
from enum import IntEnum


class Heading(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class RobotPuck(object):
    def __init__(self, x=None, y=None, radius=None, angle=None, heading=None):
        self._x = 0
        self._y = 0
        self._radius = 0
        self._angle = 0
        if heading is not None:
            self._dir = heading
        else:
            self._dir = Heading.UP
        if type(x) == RobotPuck:
            self._x = x.x
            self._y = x.y
            self._update_polar()
            self.dir = x.dir
        elif type(x) == tuple:
            self._x = x[0]
            self._y = x[1]
            self._update_polar()
        elif x is not None and y is not None:
            self._x = x
            self._y = y
            self._update_polar()
        elif radius is not None and angle is not None:
            self._radius = radius
            self._angle = angle
            self._update_cartesian()

    def _update_polar(self):
        self._radius = math.hypot(self.x, self.y)
        self._angle = math.atan2(self.y, self.x)

    def _update_cartesian(self):
        self._x = self.radius * math.cos(self.angle)
        self._y = self.radius * math.sin(self.angle)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x
        self._update_polar()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y
        self._update_polar()

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius):
        self._radius = radius
        self._update_cartesian()

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, angle):
        self._angle = angle
        self._update_cartesian()

    @property
    def dir(self):
        return self._dir

    @dir.setter
    def dir(self, dir):
        self._dir = dir

    def turn(self, right: int = 1):
        self._dir = (self.dir + (1 if right == 1 else 3)) % 4

    MOVE_DELTA = {
        Heading.UP: (0, 1),
        Heading.RIGHT: (1, 0),
        Heading.DOWN: (0, -1),
        Heading.LEFT: (-1, 0)
    }

    def forward(self, places: int = 1):
        mv = self.MOVE_DELTA[self.dir]
        self._x += mv[0] * places
        self._y += mv[1] * places
        self._update_polar()
        return self.cartesian()

    def cartesian(self, x=None, y=None):
        if x is None:
            return self.x, self.y
        elif type(x) == tuple:
            self._x = x[0]
            self._y = x[1]
            self._update_polar()
        elif x is not None and y is not None:
            self._x = x
            self._y = y
            self._update_polar()

    def polar(self, radius=None, angle=None):
        if radius is None:
            return self.radius, self.angle
        elif type(radius) == tuple:
            self._radius = radius[0]
            self._angle = radius[1]
            self._update_cartesian()
        elif radius is not None and angle is not None:
            self._radius = radius
            self._angle = angle
            self._update_cartesian()

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x!r}, {self.y!r})"

    def __add__(self, other):
        return RobotPuck(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self._x += other.x
        self._y += other.y
        self._update_polar()
        return self

    def __sub__(self, other):
        return RobotPuck(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        self._x -= other.x
        self._y -= other.y
        self._update_polar()
        return self


class Rect(object):
    def __init__(self, left_or_point=None, param2=None, param3=None, param4=None):
        self._left = 0
        # self.right = 0
        # self.top = 0
        self._bottom = 0
        self._width = 0
        self._height = 0

        if type(left_or_point) == tuple:
            self._left = left_or_point[0]
            self._bottom = left_or_point[1]
            if type(param2) == tuple:
                self._width = param2[0]
                self._height = param2[1]
            elif type(param2) in (int, float):
                self._width = param2 - self.left
                self._height = param3 - self.bottom
        elif type(left_or_point) == RobotPuck:
            self._left = left_or_point.x
            self._bottom = left_or_point.y
            if type(param2) == tuple:
                self._width = param2[0]
                self._height = param2[1]
            elif type(param2) in (int, float):
                self._width = param2 - self.left
                self._height = param3 - self.bottom
        elif left_or_point is not None and param2 is not None:
            self._left = left_or_point
            self._bottom = param2
            if type(param3) == tuple:
                self._width = param3[0]
                self._height = param3[1]
            elif type(param3) in (int, float):
                self._width = param3
                self._height = param4

    def include(self, pt: RobotPuck):
        self.left = min(pt.x,self.left)
        self.right = max(pt.x,self.right)
        self.bottom = min(pt.y,self.bottom)
        self.top = max(pt.y,self.top)

    @property
    def bottom(self):
        return self._bottom

    @bottom.setter
    def bottom(self, bottom):
        self._height += self.bottom - bottom
        self._bottom = bottom

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, left):
        self._width += self.left - left
        self._left = left

    @property
    def right(self):
        return self.left + self.width

    @right.setter
    def right(self, right):
        self._width = right - self.left

    @property
    def top(self):
        return self.bottom + self.height

    @top.setter
    def top(self, top):
        self._height = top - self.bottom


    @property
    def top_right(self):
        return RobotPuck(self.left+self._width, self.bottom+self._height)

    @property
    def bottom_left(self):
        return RobotPuck(self.left, self.bottom)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height

    def __repr__(self):
        return f'{self.__class__.__name__}({self.bottom_left}, ({self.width}, {self.height}))'

    def __str__(self):
        return f'{self.__class__.__name__}({self.bottom_left}, {self.top_right})'
