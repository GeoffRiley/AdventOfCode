"""
Advent of code 2024
Day 01: Historian Hysteria
"""

from collections import Counter
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import extract_ints, lines_to_list, to_list_int


def part1(lines: list[str]) -> int:
    """ """
    l1 = list()
    l2 = list()

    for line in lines:
        l1.append(line[0])
        l2.append(line[1])

    l1.sort()
    l2.sort()

    total_distance = 0
    for i in range(len(l1)):
        total_distance += abs(l1[i] - l2[i])

    return total_distance


def part2(lines: list[str]) -> int:
    """ """
    l1 = Counter()
    l2 = Counter()

    for line in lines:
        l1[line[0]] += 1
        l2[line[1]] += 1

    total_similar = 0
    for k in l1.keys():
        if k in l2.keys():
            total_similar += l1[k] * l2[k] * k

    return total_similar


def main():
    loader = LoaderLib(2024)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(1)
    else:
        input_text = dedent(
            """\
                3   4
                4   3
                2   5
                1   3
                3   9
                3   3
            """
        ).strip("\n")
    lines = [
        (extract_ints(param)) for param in [line for line in lines_to_list(input_text)]
    ]
    # lines = [lines_to_list(line) for line in input_text.split("\n\n")]
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
    # -
    # --------------------------------------------------------------------------------
    #  LAP -> 0.001823        |        0.001823 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : len(lines)=1000 ...
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    #  LAP -> 0.000275        |        0.002097 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 1873376
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    #  LAP -> 0.000394        |        0.002491 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 18997088
    # --------------------------------------------------------------------------------
