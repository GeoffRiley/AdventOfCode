"""
Advent of code 2025
Day 04: Printing Department
"""

from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import (
    lines_to_list,
)
from aoc.geometry import Point
from aoc.grid import Grid


def part1(lines: list[str]) -> int:
    """ """
    grid = Grid.from_text(lines)
    count, _ = get_accessible_rolls(grid)
    return count


def get_accessible_rolls(grid: Grid) -> tuple[int, list[Point]]:
    accessible_count = 0
    accessible_positions = []

    for point, value in grid.grid.items():
        if value != "@":
            continue

        adjacent_points = grid.neighbors(point, diagonals=True)
        adjacent_rolls = sum(
            1 for adj_point in adjacent_points if grid.get(adj_point) == "@"
        )

        if adjacent_rolls < 4:
            accessible_count += 1
            accessible_positions.append(point)

    return accessible_count, accessible_positions


def part2(lines: list[str]) -> int:
    """ """
    grid = Grid.from_text(lines)
    removed_count = 0
    while True:
        accessible_count, accessible_positions = get_accessible_rolls(grid)
        if accessible_count == 0:
            break

        for pos in accessible_positions:
            grid.set(".", pos)
            removed_count += 1

    return removed_count


def main():
    loader = LoaderLib(2025)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(4)
    else:
        input_text = dedent(
            """\
                ..@@.@@@@.
                @@@.@.@.@@
                @@@@@.@.@@
                @.@@@@..@.
                @@.@@@@.@@
                .@@@@@@@.@
                .@.@.@.@@@
                @.@@@.@@@@
                .@@@@@@@@.
                @.@.@@@.@.
            """
        ).strip("\n")
    # lines = [
    #     (extract_ints(param)) for param in [line for line in lines_to_list(input_text)]
    # ]
    # lines = [lines_to_list(line) for line in input_text.split("\n\n")]
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
        ),
    )


if __name__ == "__main__":
    main()
    # --
    # -
    # --------------------------------------------------------------------------------
    #  LAP -> 0.001080        |        0.001080 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : len(lines)=135 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.332828        |        0.333908 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 1370
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 7.224172        |        7.558079 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 8437
    # --------------------------------------------------------------------------------
