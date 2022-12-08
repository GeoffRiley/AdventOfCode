"""
Advent of code 2022
Day 08: Treetop Tree House
"""
from typing import List, Dict, Tuple

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


def scan_grid(grid: Dict[complex, int], visible: set, x_max: int, y_max: int, scan_y: bool = False):
    """ Scan the whole grid in either the horizontal or vertical direction
        calculating how many trees can be seen from outside the copse.
        Using a 'set' prevents duplication of trees in error.
    """
    axis1 = y_max if scan_y else x_max
    axis2 = x_max if scan_y else y_max

    def coord(a: int, b: int) -> complex:
        if scan_y:
            return a + 1j * b
        else:
            return b + 1j * a

    for ax1 in range(axis1):
        check_height = -1
        for ax2 in range(axis2):
            location = coord(ax1, ax2)
            tree_height = grid[location]
            if tree_height > check_height:
                check_height = tree_height
                visible.add(location)
    # check visibility in the negative ax1 axis
    for ax1 in range(axis1):
        check_height = -1
        for ax2 in reversed(range(axis2)):
            location = coord(ax1, ax2)
            tree_height = grid[location]
            if tree_height > check_height:
                check_height = tree_height
                visible.add(location)
    return visible


def part1(grid: Dict[complex, int], x_max: int, y_max: int) -> int:
    """
    given a grid of tree heights:
        30373
        25512
        65332
        33549
        35390
    calculate how many trees are visible from the outside
    """
    visible = set()
    # check visibility in the positive x axis
    visible = scan_grid(grid, visible, x_max, y_max)
    # check visibility in the positive y axis
    visible = scan_grid(grid, visible, y_max, x_max, True)

    return len(visible)


def calculate_scenic(grid: Dict[complex, int], x: int, y: int, x_max: int, y_max: int) -> int:
    """ Calculate the scenic value by multiply the visibility for each direction together """
    this_height = grid[x + 1j * y]
    scenic = 1
    xp = x - 1
    while xp > 0 and grid[xp + 1j * y] < this_height:
        xp -= 1
    scenic *= x - max(xp, 0)
    xp = x + 1
    while xp < x_max and grid[xp + 1j * y] < this_height:
        xp += 1
    scenic *= min(xp, x_max - 1) - x
    yp = y - 1
    while yp > 0 and grid[x + 1j * yp] < this_height:
        yp -= 1
    scenic *= y - max(yp, 0)
    yp = y + 1
    while yp < y_max and grid[x + 1j * yp] < this_height:
        yp += 1
    scenic *= min(yp, y_max - 1) - y
    return scenic


def part2(grid: Dict[complex, int], x_max: int, y_max: int) -> int:
    """
    given a grid of tree heights:
        30373
        25512
        65332
        33549
        35390
    locate the best place to hide a tree-house
    Now calculate how many trees are visible from each tree
    and get it's scenic score
    """
    scores = {}
    for x in range(x_max):
        for y in range(y_max):
            scores[x + 1j * y] = calculate_scenic(grid, x, y, x_max, y_max)
    best = max(scores.values())

    return best


def generate_grid(lines: List[str]) -> Tuple[Dict[complex, int], int, int]:
    y_max = len(lines)
    x_max = len(lines[0])
    grid = {}
    for y, line in enumerate(lines):
        for x, height in enumerate(line):
            grid[x + 1j * y] = int(height)
    return grid, x_max, y_max


def main():
    loader = LoaderLib(2022)
    input_text = loader.get_aoc_input(8)

    # input_text = dedent('''\
    #     30373
    #     25512
    #     65332
    #     33549
    #     35390
    # ''').strip('\n')

    lines = lines_to_list(input_text)

    grid, x_max, y_max = generate_grid(lines)
    loader.print_solution('setup', f'{len(lines)} ...')
    loader.print_solution(1, part1(grid, x_max, y_max))
    loader.print_solution(2, part2(grid, x_max, y_max))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.015627        |        0.015627 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 99 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.060739        |        0.076366 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 1870
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.188950        |        0.265316 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 517440
    # --------------------------------------------------------------------------------
