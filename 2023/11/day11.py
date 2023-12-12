"""
Advent of code 2023
Day 11: Cosmic Expansion
"""
# from pprint import pprint
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list
from geometry import Point


def find_empty_rows_and_cols(grid) -> tuple[list, list]:
    """
    Scan the grid for galaxies, and note the empty rows and columns
    between them.
    """
    empty_rows = []
    empty_cols = []
    for i, row in enumerate(grid):
        if "#" not in row:
            empty_rows.append(i)
    for i, col in enumerate(zip(*grid)):
        if "#" not in col:
            empty_cols.append(i)
    # pprint(empty_rows)
    # pprint(empty_cols)
    return empty_rows, empty_cols


def transpose(grid: list[str]) -> list[str]:
    return ["".join(row) for row in zip(*grid)]


def generate_galaxy_list(grid, empty_rows, empty_cols, galaxian_multiplier=2) -> list:
    galaxies = []
    y = 0
    for i, row in enumerate(grid):
        y += galaxian_multiplier if i in empty_rows else 1
        x = 0
        for j, col in enumerate(row):
            x += galaxian_multiplier if j in empty_cols else 1
            if col == "#":
                galaxies.append(Point(x, y))
    # pprint(galaxies)
    return galaxies


def get_galaxy_distances(galaxies) -> list:
    distances = []
    for i, galaxy in enumerate(galaxies):
        for j in range(i + 1, len(galaxies)):
            distances.append(galaxies[i].manhattan_distance(galaxies[j]))
    # pprint(distances)
    return distances


def part1(lines) -> int:
    """
    The text in lines is a representation of a 2D grid of space.
    Each character is either a '.', empty space, or '#', a galaxy.
    Since the image was taken, however, the galaxies have expanded.
    The expansion is not uniform though, but observations have shown
    that the expansion doubles the distance between galaxies every
    time there is an empty column or row between them.
    For example, the following image:
    ```
    .#.
    ...
    .#.
    ```
    Would expand to:
    ```
    ..#..
    .....
    .....
    ..#..
    ```
    Since there is an empty row and column between the two galaxies.

    The task is then to find the distance between each galaxy and
    return the sum of all distances.
    """
    grid = lines.copy()
    # pprint(grid)
    # print()

    # First, we need to find the empty rows and columns between galaxies.
    empty_rows, empty_cols = find_empty_rows_and_cols(grid)

    # Now we can generate a list of the coordinates of each galaxy,
    # inserting the extra rows and columns as we go.
    galaxies = generate_galaxy_list(grid, empty_rows, empty_cols)

    # Finally, we can calculate the distance between each galaxy
    # and sum them up.
    distances = get_galaxy_distances(galaxies)

    return sum(distances)


def part2(lines, galaxian_multiplier) -> int:
    """
    Of course, the universe is far older than we first thought.
    The insertion of empty rows and columns between galaxies
    has happened many times, in fast, a million times.
    This is far too much to simulate by actually expanding the
    grid, so we need to find a way to calculate the distance
    between galaxies without expanding the grid.
    Since we know the position of each expansion, we can create a
    list of the coordinates of each galaxy, and then calculate the
    distance between each pair of galaxies.
    """
    # As before, we need to generate list of the empty rows and columns
    # between galaxies; these will be the key positions of the expansions.
    grid = lines.copy()

    empty_rows, empty_cols = find_empty_rows_and_cols(grid)

    # Now we can generate a list of the coordinates of each galaxy.
    galaxies = generate_galaxy_list(
        grid,
        empty_rows,
        empty_cols,
        galaxian_multiplier
        )

    # Finally, we can calculate the distance between each galaxy
    # and sum them up.
    distances = get_galaxy_distances(galaxies)

    return sum(distances)


def main():
    loader = LoaderLib(2023)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(11)
    else:
        input_text = dedent(
            """\
            ...#......
            .......#..
            #.........
            ..........
            ......#...
            .#........
            .........#
            ..........
            .......#..
            #...#.....
            """
        ).strip("\n")
    lines = lines_to_list(input_text)

    loader.print_solution("setup", f"{len(lines)=} ...")
    loader.print_solution(
        1,
        part1(
            lines,
        ),
    )
    # if testing:
    #     input_text = dedent(
    #         """\
    #         """
    #     ).strip("\n")
    #     lines = lines_to_list(input_text)
    loader.print_solution(
        2,
        part2(
            lines,
            1_000_000,
        ),
    )


if __name__ == "__main__":
    main()
    # --
    # --------------------------------------------------------------------------------
    # LAP -> 0.001200        |        0.001200 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : len(lines)=140 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    # LAP -> 0.079324        |        0.080524 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 9974721
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    # LAP -> 0.071442        |        0.151966 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 2   : 702770569197
    # --------------------------------------------------------------------------------
