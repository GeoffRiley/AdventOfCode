"""
Advent of code 2023
Day 14: Parabolic Reflector Dish
"""
from copy import deepcopy
from functools import cache
from pprint import pprint
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


def print_grid(grid: tuple[str]) -> None:
    # print the grid
    xlate = {
        "O": "O",
        "#": ".",
        ".": " ",
    }
    print("-" * (len(grid[0])))
    for row in grid:
        for char in row:
            if char in xlate:
                print(xlate[char], end="")
            else:
                print(char, end="")
        print()
    print("-" * (len(grid[0])))


@cache
def tilt_west(grid: tuple[str]) -> tuple[str]:
    """
    Move all boulders northward as far as possible.

    Scan across the grid column by column from north to south. For each
    boulder found, move it northward as far as possible. If it hits an
    immovable object, it stops moving. If it hits another boulder, it stops
    moving. If it hits the edge of the grid, it stops moving.
    """
    # print("before")
    # print_grid(grid)
    new_grid = list(grid)
    for grid_idx, line in enumerate(grid):
        # Form the 'O' and '.' into groups separated by '#'
        line = "".join(line).split("#")
        line_copy = deepcopy(line)
        for idx, section in enumerate(line_copy):
            if section != "":
                line_copy[idx] = "".join(
                    # Sorting each section will move the 'O' to the end,
                    # reversing that will move them to the front.
                    sorted(section, reverse=True)
                )
        # Rejoin the line parts with #s in between
        new_grid[grid_idx] = "#".join(line_copy)
    return tuple(new_grid)


@cache
def tilt_north(grid: tuple[str]) -> tuple[str]:
    """
    Move all boulders northward as far as possible.

    Scan across the grid column by column from north to south. For each
    boulder found, move it northward as far as possible. If it hits an
    immovable object, it stops moving. If it hits another boulder, it stops
    moving. If it hits the edge of the grid, it stops moving.
    """
    # print("*** before ***")
    # print_grid(grid)
    new_grid = rotate(grid)
    # print("first rotate")
    # print_grid(new_grid)
    new_grid = tilt_west(new_grid)
    # print("after tilt west")
    # print_grid(new_grid)
    new_grid = rotate(new_grid, clockwise=True)
    # print("after second rotate")
    # print_grid(new_grid)
    return new_grid


@cache
def rotate(curr_map: tuple[str], clockwise: bool = False) -> tuple[str]:
    # Reverse all lines and return the columns to simulate a single rotation
    if clockwise:
        return tuple(["".join(reversed(line)) for line in zip(*curr_map)])
    return tuple(["".join(line) for line in zip(*map(reversed, curr_map))])


@cache
def do_field_spin(grid: tuple[str]) -> tuple[str]:
    # tilt the grid north: move all boulders northward as far as possible.
    for _ in range(4):
        grid = rotate(tilt_north(grid), clockwise=True)
        # print(f"set {_} = {calc_mass_effect(grid)}")
        # print_grid(grid)
    return grid


@cache
def do_1000_spin(grid: tuple[str]) -> tuple[str]:
    # tilt the grid north: move all boulders northward as far as possible.
    for _ in range(1_000):
        grid = do_field_spin(grid)
        # print(f"set {_} = {calc_mass_effect(grid)}")
        # print_grid(grid)
    return grid


def calc_mass_effect(grid: tuple[str]) -> int:
    # calculate the total mass effect of all boulders in the grid
    height = len(grid)
    return sum(row.count('O') * (height - y) for y, row in enumerate(grid))


def part1(lines: list[str]) -> int:
    """
    Boulders, "O", move around the grid in a stright line until they hit an
    immovable object, "#", am already stationary boulder or the edge of the
    grid. When they hit an immovable object, they stop moving until a new
    force is applied to them. Bolders have a mass effect of 1 for each row
    from the south border of the grid.

    Our task is to calculate the total mass effect of all boulders in the
    grid after the grid has been tilted north an all boulders have come to
    rest.
    """
    grid = tuple(lines)
    # tilt the grid north: move all boulders northward as far as possible.
    grid = tilt_north(grid)
    # calculate the total mass effect of all boulders in the grid
    return calc_mass_effect(grid)


def part2(lines: list[str]) -> int:
    """
    We are required to test the weight of the boulders in the grid after
    1_000_000_000 iterations of the cycle funtion. The cycle function tilts
    the grid north and then west and then south and then east. After each
    tilt, the boulders are allowed to come to rest before the next tilt.
    """
    grid = tuple(lines)

    for _ in range(1_000_000):
        grid = do_1000_spin(grid)
        # print(f"set {_} = {calc_mass_effect(grid)}")
        # print_grid(grid)

    return calc_mass_effect(grid)


def main():
    loader = LoaderLib(2023)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(14)
    else:
        input_text = dedent(
            """\
            O....#....
            O.OO#....#
            .....##...
            OO.#O....O
            .O.....O#.
            O.#..O.#.#
            ..O..#O..O
            .......O..
            #....###..
            #OO..#....
            """
        ).strip("\n")
    # lines = [
    #     (pat, to_list_int(param))
    #     for pat, param in [line.split() for line in lines_to_list(input_text)]
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
    # --------------------------------------------------------------------------------
    # LAP -> 0.001096        |        0.001096 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : len(lines)=100 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    # LAP -> 0.263587        |        0.264683 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 105208
    # --------------------------------------------------------------------------------
