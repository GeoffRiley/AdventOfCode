"""
Advent of code 2021
Day 9: Smoke Basin
"""
from math import prod
from typing import List, Tuple

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list
from aoc.utility import sequence_to_int


def part1(lines: List[List[int]], load: LoaderLib):
    """
    """
    lows = []
    low_risk = 0
    line_len = len(lines[0]) + 2
    new_lines = [[9] * line_len] + [[9] + line + [9] for line in lines] + [[9] * line_len]
    for line in range(1, len(lines) + 1):
        for pos in range(1, line_len - 1):
            h = new_lines[line][pos]
            if ((new_lines[line][pos - 1] > h < new_lines[line][pos + 1]) and
                    (new_lines[line - 1][pos] > h < new_lines[line + 1][pos])):
                lows.append((pos - 1, line - 1))
                low_risk += 1 + int(h)

    load.cache_data(9, 'risk', lows)
    return f'Risk level for low points: {low_risk}'


def scan_basin(lines: List[List[int]], low: Tuple[int, int]) -> int:
    borders = (0, 0, len(lines[0]) - 1, len(lines) - 1)
    basin_elements = {low}
    frontier = [(low, lines[low[1]][low[0]])]
    while frontier:
        (col, row), height = frontier.pop(0)
        if col > borders[0]:
            h = lines[row][col - 1]
            if 9 != h > height:
                frontier.append(((col - 1, row), h))
                basin_elements.add((col - 1, row))
        if col < borders[2]:
            h = lines[row][col + 1]
            if 9 != h > height:
                frontier.append(((col + 1, row), h))
                basin_elements.add((col + 1, row))
        if row > borders[1]:
            h = lines[row - 1][col]
            if 9 != h > height:
                frontier.append(((col, row - 1), h))
                basin_elements.add((col, row - 1))
        if row < borders[3]:
            h = lines[row + 1][col]
            if 9 != h > height:
                frontier.append(((col, row + 1), h))
                basin_elements.add((col, row + 1))
    return len(basin_elements)


def part2(lines: List[List[int]], load: LoaderLib):
    """
    """
    lows = load.retrieve_data(9, 'risk')
    basin_list = []
    for low in lows:
        basin_list.append(scan_basin(lines, low))

    return prod(sorted(basin_list)[-3:])


def main():
    loader = LoaderLib(2021)
    input_text = loader.get_aoc_input(9)

    #     input_text = """2199943210
    # 3987894921
    # 9856789892
    # 8767896789
    # 9899965678"""
    lines = [sequence_to_int(line) for line in lines_to_list(input_text)]

    # assert len(lines) == len(...)
    loader.print_solution('setup', f'{len(lines)} ...')
    loader.print_solution(1, part1(lines, loader))
    loader.print_solution(2, part2(lines, loader))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.006016        |        0.006016 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 100 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.032310        |        0.038326 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : Risk level for low points: 480
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.096915        |        0.135241 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 1045660
    # --------------------------------------------------------------------------------
