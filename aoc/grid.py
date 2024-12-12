class Grid:
    def __init__(self, default=0):
        self.grid = {}
        self.default = default
        self._ranges = {}

    def copy(self) -> "Grid":
        ret = Grid()
        ret.grid = self.grid.copy()
        ret.default = self.default
        return ret

    @staticmethod
    def from_text(values) -> "Grid":
        grid = Grid()
        if isinstance(values, str):
            if "\n" in values:
                values = values.split("\n")
            else:
                values = [values]
        for y, row in enumerate(values):
            for x, cur in enumerate(row):
                grid.set(cur, x, y)
        return grid

    def __getitem__(self, key):
        if isinstance(key, tuple):
            return self.grid.get(key, self.default)
        else:
            return self.grid.get((key,), self.default)

    def __setitem__(self, key, value):
        self._ranges = {}
        if isinstance(key, tuple):
            self.grid[key] = value
        else:
            self.grid[(key,)] = value

    def __delitem__(self, key):
        if isinstance(key, tuple):
            del self.grid[key]
        else:
            del self.grid[(key,)]

    def __iter__(self):
        return self.grid.values().__iter__()

    def __contains__(self, key):
        if isinstance(key, tuple):
            return key in self.grid
        else:
            return (key,) in self.grid

    def get(self, *coords):
        return self.grid.get(*coords, self.default)

    def set(self, value, *coords):
        self._ranges = {}
        self.grid[*coords] = value

    def axis_min(self, axis):
        if self._ranges.get(axis, None) is None:
            self._ranges[axis] = (
                min([x[axis] for x in self.grid]),
                max([x[axis] for x in self.grid]),
            )
        return self._ranges[axis][0]

    def axis_max(self, axis):
        if self._ranges.get(axis, None) is None:
            self._ranges[axis] = (
                min([x[axis] for x in self.grid]),
                max([x[axis] for x in self.grid]),
            )
        return self._ranges[axis][1]

    def axis_size(self, axis):
        return self.axis_max(axis) - self.axis_min(axis) + 1

    def width(self):
        return self.axis_size(0)

    def height(self):
        return self.axis_size(1)

    def neighbors(self, *args, diagonals=False, valid_only=False):
        """
        Returns the neighbors of the given location.
        If diagonals is True, returns the 8 neighbors of the given location.
        If valid_only is True, only returns neighbors that are in the grid.
        """
        if isinstance(args[0], tuple):
            x, y = args[0]
        else:
            x, y = args
        if diagonals:
            offsets = (
                (-1, -1),
                (-1, 0),
                (-1, 1),
                (0, -1),
                (0, 1),
                (1, -1),
                (1, 0),
                (1, 1),
            )
        else:
            offsets = ((0, -1), (1, 0), (0, 1), (-1, 0))
        for ox, oy in offsets:
            ox = ox + x
            oy = oy + y
            if not valid_only or (ox, oy) in self.grid:
                yield ox, oy

    def next_location(self, location, wrap=False):
        """
        Returns the next location in the grid, or None if there is no next
        location.
        If wrap is True, the grid wraps around.
        """
        if isinstance(location, tuple):
            x, y = location
        else:
            x, y = location.x, location.y
        if x < self.axis_max(0):
            x += 1
        elif y < self.axis_max(1):
            x = self.axis_min(0)
            y += 1
        elif wrap:
            x = self.axis_min(0)
            y = self.axis_min(1)
        else:
            return None
        return x, y

    def is_valid(self, *coords):
        """
        Checks if the given coordinates are valid within the grid.

        Determines whether the provided coordinates exist in the current grid. 
        Returns a boolean indicating the presence of the coordinates.

        Args:
            *coords: Variable number of coordinate arguments to check.

        Returns:
            bool: True if coordinates are in the grid, False otherwise.
        """
        return coords in self.grid
    