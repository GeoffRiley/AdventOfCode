"""
Advent of code 2024
Day 25: Code Chronicle
"""

import itertools
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list
from aoc.grid import Grid


def part1(lines: list[list[str]]) -> int:
    """
    `lines` is a list of string lists, each string is a grid of # and .
    characters. The strings represent locks and keys.

    "The locks are schematics that have the top row filled (#) and the bottom
    row empty (.); the keys have the top row empty and the bottom row filled.
    If you look closely, you'll see that each schematic is actually a set of
    columns of various heights, either extending downward from the top (for
    locks) or upward from the bottom (for keys)."

    "For locks, those are the pins themselves; you can convert the pins in
    schematics to a list of heights, one per column. For keys, the columns
    make up the shape of the key where it aligns with pins; those can also be
    converted to a list of heights."

    "So, you could say the first lock has pin heights 0,5,3,4,3:"

        #####
        .####
        .####
        .####
        .#.#.
        .#...
        .....

    "Or, that the first key has heights 5,0,2,1,3:"

        .....
        #....
        #....
        #...#
        #.#.#
        #.###
        #####

    Having schematics as grids, we can count the number of pins in each column
    and convert the grid to a list of heights.
    """
    key_list = []
    lock_list = []
    for line in lines:
        grid = Grid.from_text(line)
        places = [
            sum(grid[j, i] == "#" for i in range(grid.height()))
            for j in range(grid.width())
        ]
        if grid[0, 0] == "#":
            lock_list.append(places)
        else:
            key_list.append(places)
    print(f"Count, locks:{len(lock_list)}, keys:{len(key_list)}")
    matches = 0
    for key, lock in itertools.product(key_list, lock_list):
        check = [x + y for x, y in zip(key, lock) if x + y <= 7]
        if len(check) == 5:
            matches += 1
    return matches


def part2(lines: list[str]) -> int:
    """ """
    ...


def main():
    loader = LoaderLib(2024)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(25)
    else:
        input_text = dedent(
            """\
                #####
                .####
                .####
                .####
                .#.#.
                .#...
                .....

                #####
                ##.##
                .#.##
                ...##
                ...#.
                ...#.
                .....

                .....
                #....
                #....
                #...#
                #.#.#
                #.###
                #####

                .....
                .....
                #.#..
                ###..
                ###.#
                ###.#
                #####

                .....
                .....
                .....
                #....
                #.#..
                #.#.#
                #####
            """
        ).strip("\n")
    # lines = [
    #     (extract_ints(param)) for param in [line for line in lines_to_list(input_text)]
    # ]
    lines = [lines_to_list(line) for line in input_text.split("\n\n")]
    # lines = lines_to_list(input_text)

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
    # LAP -> 0.000408        |        0.000408 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : len(lines)=500 ...
    # --------------------------------------------------------------------------------

    # Count, locks:250, keys:250

    # --------------------------------------------------------------------------------
    # LAP -> 0.023754        |        0.024162 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 3077
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.000081        |        0.024243 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 2   : None
    # --------------------------------------------------------------------------------
