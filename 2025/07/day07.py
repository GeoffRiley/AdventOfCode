"""
Advent of code 2025
Day 07: Laboratories
"""

from textwrap import dedent

from aoc.geometry import Point
from aoc.grid import Grid
from aoc.loader import LoaderLib
from aoc.utility import lines_to_list

START_FLAG = "S"
SPACE_FLAG = "."
SPLITTER_FLAG = "^"
BEAM_FLAG = "|"

point_left = Point(-1, 0)
point_right = Point(1, 0)
point_down = Point(0, 1)


def part1(grid: Grid) -> int:
    """Solves part 1 of the puzzle by simulating the beam and counting splits.

        Determines the number of times the beam splits as it falls through the
        grid, starting from the initial position. Returns the total count of
        beam splits encountered during the simulation.

        Args:
            grid (Grid): The grid representing the laboratory layout.

        Returns:
            int: The number of beam splits encountered.
    """
    start_point = find_starting_point(grid)
    if start_point is None:
        raise ValueError("No starting point found.")

    return count_beam_splits(grid, start_point)


def count_beam_splits(grid: Grid, start_point: Point) -> int:
    """Counts the number of beam-splits as the beam travels through the grid.

            Simulates the movement of a beam starting from the given point
            and tracks how many times it splits upon encountering splitters.
            Returns the total number of splits that occur during the
            simulation.

            Args:
                grid (Grid): The grid representing the laboratory layout.
                start_point (Point): The starting position of the beam.

            Returns:
                int: The total number of beam splits encountered.
    """
    beam_list = [start_point]
    new_beam_list = []
    beam_split_count = 0

    while beam_list:
        beam = beam_list.pop(0)
        new_beam = beam + point_down

        if not grid.is_valid(*new_beam):
            continue

        cell_value = grid[new_beam]
        if cell_value == SPLITTER_FLAG:
            beam_split_count += 1
            _process_splitter(grid, new_beam, new_beam_list)
        elif cell_value == SPACE_FLAG:
            grid[new_beam] = BEAM_FLAG
            new_beam_list.append(new_beam)

        if not beam_list:
            beam_list = new_beam_list[:]
            new_beam_list = []

    return beam_split_count


def _process_splitter(grid: Grid, position: Point, next_beams: list) -> None:
    """Handles the splitting of a beam when it encounters a splitter.

            When a beam reaches a splitter, this function adds new beams to
            the left and right if those positions are open. Updates the grid
            and the list of next beams accordingly.

            Args:
                grid (Grid): The grid representing the laboratory layout.
                position (Point): The current position of the splitter.
                next_beams (list): The list to which new beam positions will be added.
    """
    for direction in (point_left, point_right):
        next_pos = position + direction
        if grid[next_pos] == SPACE_FLAG:
            grid[next_pos] = BEAM_FLAG
            next_beams.append(next_pos)


def find_starting_point(grid: Grid) -> Point:
    """Finds the starting point in the grid marked by the start flag.

        Searches the grid for the cell containing the start flag and returns
        its coordinates as a Point object. If no start flag is found, it
        returns None.

        Args:
            grid (Grid): The grid to search for the starting point.

        Returns:
            Point: The coordinates of the starting point, or None if not found.
    """
    start_point = None
    for row in range(grid.height()):
        for col in range(grid.width()):
            if grid[(col, row)] == START_FLAG:
                start_point = Point(col, row)
                break
        if start_point is not None:
            break
    return start_point


def part2(grid: Grid) -> int:
    """Solves part 2 of the puzzle by counting all possible ways the beam can reach the bottom.

            Calculates the number of distinct paths the beam can take
            from the starting point to the bottom of the grid,
            considering splitters and open spaces. Returns the total
            number of valid paths found.

            Args:
                grid (Grid): The grid representing the laboratory layout.

            Returns:
                int: The total number of valid beam paths to the bottom.
    """
    row_count = grid.height()
    col_count = grid.width()
    start_point = find_starting_point(grid)
    ways = [0] * col_count
    ways[start_point.x] = 1
    for row in range(start_point.y + 1, row_count):
        new_ways = [0] * col_count
        for col in range(col_count):
            if ways[col] == 0:
                continue
            cell_below = grid[(col, row)]
            # print(f"Checking cell ({col},{row}) = {cell_below}")
            if cell_below == SPACE_FLAG:
                new_ways[col] += ways[col]
            elif cell_below == SPLITTER_FLAG:
                if col > 0:
                    new_ways[col - 1] += ways[col]
                if col < col_count - 1:
                    new_ways[col + 1] += ways[col]
            else:
                raise ValueError(f"Unknown cell value: {cell_below} at ({col},{row})")
        ways = new_ways[:]
    return sum(ways)


def main():
    loader = LoaderLib(2025)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(7)
    else:
        input_text = dedent(
            """\
                .......S.......
                ...............
                .......^.......
                ...............
                ......^.^......
                ...............
                .....^.^.^.....
                ...............
                ....^.^...^....
                ...............
                ...^.^...^.^...
                ...............
                ..^...^.....^..
                ...............
                .^.^.^.^.^...^.
                ...............
            """
        ).strip("\n")
    # lines = [(extract_ints(param)) for param in list(lines_to_list(input_text))]
    # lines = [lines_to_list(line) for line in input_text.split("\n\n")]
    lines = lines_to_list(input_text)
    # lines = input_text.split(',')

    g = Grid.from_text(input_text)

    loader.print_solution("setup", f"{len(lines)=} ...")
    loader.print_solution(
        1,
        part1(
            g,
        ),
    )

    # if testing:
    #     input_text = dedent(
    #         """\
    #         """
    #     ).strip("\n")
    #     lines = lines_to_list(input_text)

    g = Grid.from_text(input_text)

    loader.print_solution(
        2,
        part2(
            g,
        ),
    )


if __name__ == "__main__":
    main()
    # --
    # --------------------------------------------------------------------------------
    #  LAP -> 0.007992        |        0.007992 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : len(lines)=142 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.031343        |        0.039336 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 1687
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.012046        |        0.051382 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 390684413472684
    # --------------------------------------------------------------------------------
