"""
Advent of code 2021
Day 6: Lanternfish
"""
from collections import Counter
from typing import List, Dict

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list, to_list_int


def swim_for_a_day(life_counts: Dict[int, int]):
    """Process the shoal, decrement the life_counts:
    any that get to -1 have procreated in the last day, their offspring are
    created with 8 day life_counts, whilst they get reset to 6 days… and are
    added to the count of any fish that moved down from 7 days.
    """
    new_counts = {d - 1: p for d, p in life_counts.items()}
    if -1 in new_counts.keys():
        new_counts[8] = new_counts[-1]
        new_counts[6] = new_counts[-1] + new_counts.get(6, 0)
        del new_counts[-1]

    return new_counts


def part1(life_timers: List[int]):
    """Oh look a squirrel!  Nope, it's a lanternfish.
    Use the `Counter` class to summarise the shoal into a more
    convenient lump of data, then process them for 80 days.
    """
    life_counts = Counter(life_timers)
    for _ in range(80):
        life_counts = swim_for_a_day(life_counts)

    return f'{sum(life_counts.values())} fish'


def part2(life_timers):
    """It's that shoal again.
    Doing the same as before, but for 256 days.
    This could easily have been combined with the first pass, but it's
    so fast as to not need such an optimisation.
    """
    life_counts = Counter(life_timers)
    for _ in range(256):
        life_counts = swim_for_a_day(life_counts)

    return f'{sum(life_counts.values())} fish'


def main():
    loader = LoaderLib(2021)
    input_text = loader.get_aoc_input(6)
    # input_text = '3,4,3,1,2'
    lines = lines_to_list(input_text)

    life_timers = to_list_int(lines[0])

    # assert len(lines) == len(...)
    loader.print_solution('setup', f'{len(life_timers)} fishy life timers')
    loader.print_solution(1, part1(life_timers))
    loader.print_solution(2, part2(life_timers))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.003169        |        0.003169 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 300 fishy life timers
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.000777        |        0.003946 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 387413 fish
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.001435        |        0.005381 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 1738377086345 fish
    # --------------------------------------------------------------------------------
