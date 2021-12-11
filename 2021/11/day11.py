"""
Advent of code 2021
Day 11: Dumbo Octopus
"""
from copy import deepcopy
from typing import List

from aoc.geometry import Rectangle
from aoc.loader import LoaderLib
from aoc.utility import lines_to_list
from aoc.utility import sequence_to_int


def increment_rectangle(lines: List[List[int]], rect: Rectangle) -> None:
    for y in range(rect.top, rect.bottom + 1):
        for x in range(rect.left, rect.right + 1):
            lines[y][x] += 1


def do_flash(lines, whole_rect) -> int:
    flashed = set()
    more_flashes = True
    while more_flashes:
        more_flashes = False
        for y, line in enumerate(lines):
            for x, octopus in enumerate(line):
                if octopus > 9 and (x, y) not in flashed:
                    increment_rectangle(
                        lines,
                        Rectangle(x - 1, y - 1, x + 1, y + 1).intersect(whole_rect)
                    )
                    flashed.add((x, y))
                    more_flashes = True
    # set all flashed octopus back to zero
    for x, y in flashed:
        lines[y][x] = 0
    return len(flashed)


def part1(lines: List[List[int]]):
    """A modified Game of Life
    """
    flash_count = 0
    whole_rect = Rectangle(0, 0, len(lines[0]) - 1, len(lines) - 1)
    for _ in range(100):
        # First increment all octopus
        increment_rectangle(lines, whole_rect)
        # Now seek out all octopus with energy level 9
        # and increment neighbours
        flash_count += do_flash(lines, whole_rect)
    return flash_count
    # 1665


def part2(lines: List[List[int]]):
    """
    """
    whole_rect = Rectangle(0, 0, len(lines[0]) - 1, len(lines) - 1)
    step = 0
    while any(octopus > 0 for line in lines for octopus in line):
        increment_rectangle(lines, whole_rect)
        do_flash(lines, whole_rect)
        step += 1
    return step
    # 235


def main():
    loader = LoaderLib(2021)
    input_text = loader.get_aoc_input(11)

    #     input_text = """5483143223
    # 2745854711
    # 5264556173
    # 6141336146
    # 6357385478
    # 4167524645
    # 2176841721
    # 6882881134
    # 4846848554
    # 5283751526"""

    lines = [sequence_to_int(line) for line in lines_to_list(input_text)]
    p1_lines = deepcopy(lines)
    p2_lines = deepcopy(lines)

    # assert len(lines) == len(...)
    loader.print_solution('setup', f'{len(lines)} ...')
    loader.print_solution(1, part1(p1_lines))
    loader.print_solution(2, part2(p2_lines))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.004889        |        0.004889 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 10 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.037268        |        0.042157 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 1665
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.077167        |        0.119324 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 235
    # --------------------------------------------------------------------------------
