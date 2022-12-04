"""
Advent of code 2022
Day 04: Camp Cleanup
"""
from typing import List

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list, extract_ints


def part1(lines: List[List[int]]) -> int:
    """
    Each line is a pair of ranges: a-b,c-d
    We must count instances of a-b being contained in c-d
    or c-d being contained in a-b
    """
    hits = 0
    for a, b, c, d in lines:
        if (a <= c <= d <= b) or (c <= a <= b <= d):
            hits += 1

    return hits


def part2(lines: List[List[int]]) -> int:
    """
    Each line is a pair of ranges: a-b,c-d
    We must count instances of a-b overlapping c-d
    """
    hits = 0
    for a, b, c, d in lines:
        if (
                a >= c >= b or
                a <= d <= b or
                c >= a >= d or
                c <= b <= d
        ):
            hits += 1

    return hits


def main():
    loader = LoaderLib(2022)
    input_text = loader.get_aoc_input(4)

    # input_text = dedent('''\
    #     2-4,6-8
    #     2-3,4-5
    #     5-7,7-9
    #     2-8,3-7
    #     6-6,4-6
    #     2-6,4-8
    # ''').strip('\n')

    lines = list(map(extract_ints, lines_to_list(input_text)))

    loader.print_solution('setup', f'{len(lines)} ...')
    loader.print_solution(1, part1(lines))
    loader.print_solution(2, part2(lines))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.016750        |        0.016750 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 1000 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.001474        |        0.018224 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 526
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.001034        |        0.019259 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 886
    # --------------------------------------------------------------------------------
