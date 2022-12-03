"""
Advent of code 2022
Day 03: Rucksack Reorganization
"""
import string
from typing import List

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list, grouped

RUCKSACK_CONTENTS = string.ascii_lowercase + string.ascii_uppercase
PRIORITY_STATES = {c: v for v, c in enumerate(RUCKSACK_CONTENTS, 1)}


def part1(lines: List[str]) -> int:
    """
    List of strings representing the contents of backpacks.
    Each letter defines a different type of item in the backpack.
    Backpack have two compartments: front and back, their separate
    contents are describes by the string when split in twain.
    Our task is to identify the class of item duplicated in both
    compartments for each backpack. The sum of the priorities is
    the required result.
    """
    priority = 0
    for line in lines:
        line_split = len(line) // 2
        common = set(line[:line_split]).intersection(line[line_split:])
        priority += sum(PRIORITY_STATES[x] for x in common)

    return priority


def part2(lines: List[str]) -> int:
    """
    List of strings representing the contents of backpacks.
    The backpacks should be grouped into threes. Three elves
    work together in unison and have a group badge which may
    be identified as the one item type common to all three
    of their backpacks.
    """
    priority = 0
    for line in grouped(lines, 3):
        common = set(line[0]).intersection(line[1]).intersection(line[2])
        priority += sum(PRIORITY_STATES[x] for x in common)

    return priority


def main():
    loader = LoaderLib(2022)
    input_text = loader.get_aoc_input(3)

    # input_text = dedent("""\
    #     vJrwpWtwJgWrhcsFMMfFFhFp
    #     jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
    #     PmmdzqPrVvPwwTWBwg
    #     wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
    #     ttgJtRGJQctTZtZT
    #     CrZsJsPPZsGzwwsLwLmpwMDw
    # """).strip("\n")

    lines = lines_to_list(input_text)

    loader.print_solution('setup', f'{len(lines)} ...')
    loader.print_solution(1, part1(lines))
    loader.print_solution(2, part2(lines))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.003505        |        0.003505 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 300 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.002431        |        0.005937 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 7581
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.001382        |        0.007319 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 2525
    # --------------------------------------------------------------------------------
