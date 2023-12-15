"""
Advent of code 2023
Day 14: Parabolic Reflector Dish
"""
from pprint import pprint
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list
from grid import Grid


def print_grid(grid):
    # print the grid
    xlate = {
        "O": "O",
        "#": ".",
        ".": " ",
    }
    print("-" * (grid.width()))
    for row in range(grid.height()):
        for col in range(grid.width()):
            if grid[col, row] in xlate:
                print(xlate[grid[col, row]], end="")
            else:
                print(grid[col, row], end="")
        print()
    print("-" * (grid.width()))


def tilt_north(grid: Grid) -> None:
    """
    Move all boulders northward as far as possible.

    Scan across the grid column by column from north to south. For each
    boulder found, move it northward as far as possible. If it hits an
    immovable object, it stops moving. If it hits another boulder, it stops
    moving. If it hits the edge of the grid, it stops moving.
    """
    # print("before")
    # print_grid(grid)
    for col in range(grid.width()):
        available_cell = False
        for row in range(grid.height()):
            character = grid[col, row]
            if character == ".":
                if not available_cell:
                    available_cell = (col, row)
                    grid[available_cell] = "×"
                    # print("available cell found")
                    # print_grid(grid)
            elif character == "#":
                if available_cell:
                    grid[available_cell] = "."
                available_cell = False
            elif character == "O":
                if available_cell:
                    grid[col, row] = "."
                    grid[available_cell] = character
                    available_cell = (available_cell[0], available_cell[1]+1)
                    grid[available_cell] = "×"
                    # print("move boulder")
                    # print_grid(grid)
    # print("after")
    # print_grid(grid)
    # print()


def part1(lines: list[list[str]]) -> int:
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
    grid = Grid.from_text(lines)
    # tilt the grid north: move all boulders northward as far as possible.
    tilt_north(grid)
    # calculate the total mass effect of all boulders in the grid
    total_mass_effect = 0
    for row in range(grid.height()):
        for col in range(grid.width()):
            if grid[col, row] == "O":
                total_mass_effect += grid.height() - row
    return total_mass_effect


def part2(lines) -> int:
    """
    """
    ...


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
