from typing import Any, Generator, Iterator


class Grid:
    """
    A grid data structure that stores values at arbitrary coordinates. The
    grid provides flexible storage and retrieval of values with a configurable
    default value. The grid supports multi-dimensional coordinates and
    provides convenient methods for iterating over, accessing, and modifying
    grid values.
    """

    def __init__(self, default=0) -> None:
        """
        Initializes a grid data structure with an optional default value. The
        grid allows flexible storage and retrieval of values with a
        configurable default.

        Args:
            default: The default value to return for unset grid coordinates.
            Defaults to 0.
        """
        self.grid = {}
        self.default = default
        self._ranges = {}

    def copy(self) -> "Grid":
        """
        Creates a deep copy of the current grid instance. The method ensures
        that modifications to the new grid do not affect the original grid.

        Returns:
            Grid: A new grid instance with the same grid contents and default
                value as the original.
        """
        ret = Grid()
        ret.grid = self.grid.copy()
        ret.default = self.default
        return ret

    @staticmethod
    def from_text(values) -> "Grid":
        """
        Creates a Grid instance from text input, supporting single strings or
        multi-line text. The method populates the grid by converting input
        text into grid coordinates with individual characters.

        Args:
            values: Input text to convert into a grid, which can be a single
            string or a list of strings.

        Returns:
            Grid: A new grid instance populated with characters from the input
            text.
        """
        grid = Grid()
        if isinstance(values, str):
            values = values.split("\n") if "\n" in values else [values]
        for y, row in enumerate(values):
            for x, cur in enumerate(row):
                grid.set(cur, (x, y))
        return grid

    def __getitem__(self, key) -> Any:
        """
        Provides dictionary-like access to grid values using coordinate keys.
        The method supports both single and multi-dimensional coordinate
        lookups, returning the default value if the coordinate is not set.

        Args:
            key: A coordinate tuple or single value representing the grid
            location to retrieve.

        Returns:
            The value at the specified grid coordinate, or the default value
            if the coordinate is unset.
        """
        if isinstance(key, tuple):
            return self.grid.get(tuple(key), self.default)
        else:
            return self.grid.get((key,), self.default)

    def __setitem__(self, key, value) -> None:
        """
        Enables dictionary-like assignment of values to grid coordinates with
        flexible key handling. The method supports setting grid values using
        single or multi-dimensional coordinate keys while resetting the grid's
        range cache.

        Args:
            key: A coordinate tuple or single value representing the grid
            location to set.
            value: The value to be stored at the specified grid coordinate.
        """
        self._ranges = {}
        if isinstance(key, tuple):
            self.grid[tuple(key)] = value
        else:
            self.grid[(key,)] = value

    def __delitem__(self, key) -> None:
        """
        Enables dictionary-like deletion of values from grid coordinates with
        flexible key handling. The method supports removing grid values using
        single or multi-dimensional coordinate keys.

        Args:
            key: A coordinate tuple or single value representing the grid
            location to delete.
        """
        if isinstance(key, tuple):
            del self.grid[key]
        else:
            del self.grid[(key,)]

    def __iter__(self) -> Iterator:
        """
        Enables iteration over the grid's values using the standard Python
        iteration protocol. The method allows direct iteration through the
        grid's stored values without needing to access the underlying grid
        dictionary explicitly.

        Returns:
            An iterator over the grid's values.
        """
        return self.grid.values().__iter__()

    def __contains__(self, key) -> bool:
        """
        Enables the use of the `in` operator to check for the presence of
        coordinates in the grid. The method supports checking both single
        and multi-dimensional coordinate keys.

        Args:
            key: A coordinate tuple or single value to check for existence in
            the grid.

        Returns:
            bool: True if the coordinate exists in the grid, False otherwise.
        """
        return key in self.grid if isinstance(key, tuple) else (key,) in self.grid

    def get(self, coords) -> Any:
        """
        Retrieves the value at specified grid coordinates with a fallback to
        the default value. The method provides a flexible way to access grid
        values while handling cases where coordinates may not exist.

        Args:
            coords: Variable number of coordinate arguments representing the
            grid location.

        Returns:
            The value at the specified coordinates, or the default value if
            the coordinates are not set.
        """
        if isinstance(coords, tuple):
            return self.grid.get(coords, self.default)
        else:
            return self.grid.get((coords,), self.default)

    def set(self, value, coords) -> None:
        """
        Sets the value at specified grid coordinates, updating the grid with
        the new value. The method supports flexible assignment of values to
        grid locations with a variable number of coordinate arguments.

        Args:
            value: The value to store at the specified grid coordinates.
            coords: A tuple representing the grid location.

        Returns:
            None
        """
        self._ranges = {}
        if isinstance(coords, tuple):
            self.grid[coords] = value
        else:
            self.grid[(coords,)] = value

    def axis_min(self, axis) -> Any:
        """
        Calculates and caches the minimum value for a specified grid axis. The
        method efficiently computes the minimum coordinate value along a given
        axis, storing the result for future use.

        Args:
            axis: The index of the axis to calculate the minimum value for.

        Returns:
            The minimum coordinate value along the specified axis.
        """
        if self._ranges.get(axis, None) is None:
            self._ranges[axis] = min(x[axis] for x in self.grid), max(
                x[axis] for x in self.grid
            )
        return self._ranges[axis][0]

    def axis_max(self, axis) -> Any:
        """
        Calculates and caches the maximum value for a specified grid axis. The
        method efficiently computes the maximum coordinate value along a given
        axis, storing the result for future use.

        Args:
            axis: The index of the axis to calculate the maximum value for.

        Returns:
            The maximum coordinate value along the specified axis.
        """
        if self._ranges.get(axis, None) is None:
            self._ranges[axis] = min(x[axis] for x in self.grid), max(
                x[axis] for x in self.grid
            )
        return self._ranges[axis][1]

    def axis_size(self, axis) -> Any:
        """
        Calculates the size of the grid along a specified axis by determining
        the range of coordinates. The method computes the total number of
        unique coordinate values for the given axis.

        Args:
            axis: The index of the axis to calculate the size for.

        Returns:
            The number of unique coordinate values along the specified axis.
        """
        return self.axis_max(axis) - self.axis_min(axis) + 1

    def width(self) -> Any:
        """
        Determines the width of the grid by calculating the size along the
        first axis (x-axis). The method provides a convenient way to retrieve
        the horizontal span of the grid.

        Returns:
            The number of unique x-coordinate values in the grid.
        """
        return self.axis_size(0)

    def height(self) -> Any:
        """
        Determines the height of the grid by calculating the size along the
        second axis (y-axis). The method provides a convenient way to retrieve
        the vertical span of the grid.

        Returns:
            The number of unique y-coordinate values in the grid.
        """
        return self.axis_size(1)

    def neighbors(
        self, *args, diagonals=False, valid_only=False
    ) -> Generator[tuple, Any, None]:
        """
        Generates the neighbors of a specified location in the grid. The
        method supports both cardinal and diagonal neighbors, as well as
        filtering for valid grid coordinates.

        Args:
            args: A tuple representing the location to find neighbors for.
            diagonals: A boolean indicating whether to include diagonal
            neighbors. Defaults to False.
            valid_only: A boolean indicating whether to filter out neighbors
            outside the grid. Defaults to False.

        Yields:
            tuple: The coordinates of each neighbor of the specified location.
        """
        x, y = args[0] if isinstance(args[0], tuple) else args
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

    def next_location(self, location, wrap=False) -> None | tuple[Any, Any]:
        """
        Returns the next location in the grid, or None if there is no next
        location.

        Args:
            location: The current location in the grid.
            wrap:
                A boolean indicating whether the grid wraps around.
                Defaults to False.
                If True, the grid wraps around. If False, the grid does
                not wrap around.

        Returns:
            The next location in the grid, or None if there is no next
            location.
        """
        x, y = location if isinstance(location, tuple) else (location.x, location.y)
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

    def transpose(self):
        """
        Transposes the grid, swapping the x and y axes.
        """
        new_grid = Grid()
        for x in range(self.axis_min(0), self.axis_max(0) + 1):
            for y in range(self.axis_min(1), self.axis_max(1) + 1):
                new_grid.set(self[x, y], (y, x))
        return new_grid

    def __str__(self):
        rep = ""
        for y in range(self.axis_min(1), self.axis_max(1) + 1):
            for x in range(self.axis_min(0), self.axis_max(0) + 1):
                rep += str(self[x, y])
            rep += "\n"
        return rep.strip()

    def __repr__(self):
        return str(self)
