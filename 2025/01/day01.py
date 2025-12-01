"""
Advent of code 2025
Day 01: Secret Entrance
"""

from operator import add, sub
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


def part1(lines: list[str]) -> int:
    """ """
    # Initialised to 50
    pointer = 50
    count = 0

    for line in lines:
        direction = add if line[0] == 'R' else sub
        distance = int(line[1:])
        pointer = direction(pointer, distance) % 100
        if pointer == 0:
            count += 1

    return count


def part2(lines: list[str]) -> int:
    """ """
    # Initialised to 50
    pointer = 50
    count = 0

    for line in lines:
        prev_pointer = pointer

        direction = add if line[0] == 'R' else sub
        distance = int(line[1:])
        d, r = divmod(distance, 100)
        count += d

        pointer = direction(pointer, r)

        if pointer <= 0 or pointer >= 100:
            pointer %= 100
            if pointer != prev_pointer != 0:
                count += 1

    return count
    # 3231 too low!


def main():
    loader = LoaderLib(2025)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(1)
    else:
        input_text = dedent(
            """\
                L68
                L30
                R48
                L5
                R60
                L55
                L1
                L99
                R14
                L82
            """
        ).strip("\n")
    # lines = [(extract_ints(param)) for param in list(lines_to_list(input_text))]
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
    #  LAP -> 0.000441        |        0.000441 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : len(lines)=4510 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.001102        |        0.001543 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 1084
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.001700        |        0.003243 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 6475
    # --------------------------------------------------------------------------------
