"""
Advent of code 2022
Day 14: Regolith Reservoir
"""
from collections import defaultdict
from copy import deepcopy
from textwrap import dedent

from aoc.geometry import Point, Rectangle
from aoc.loader import LoaderLib
from aoc.search import Stack
from aoc.utility import lines_to_list
from aoc.utility import pairwise

SAND_ORIGIN = Point(500, 0)

AIR = 0
ROCK = 1
SAND = 2
SAND_GEN = 3


def dump_grid(grid: defaultdict, enclosure: Rectangle):
    for y in range(enclosure.top, enclosure.bottom + 1):
        line = ''
        for x in range(enclosure.left, enclosure.right + 1):
            line += ".#o+"[grid[(x, y)]]
        print(line)


def setup_grid(lines):
    grid = defaultdict(int)
    grid[tuple(SAND_ORIGIN)] = SAND_GEN
    # create an enclosure that all valid points are contained within
    enclosure = Rectangle(SAND_ORIGIN.x, SAND_ORIGIN.y, SAND_ORIGIN.x, SAND_ORIGIN.y)
    # Track the height
    height = 0
    for line in lines:
        corners = [tuple(int(c) for c in p.strip().split(',')) for p in line.split('->')]
        for (x1, y1), (x2, y2) in pairwise(corners):
            # Include this line in the main enclosure
            x1, x2 = min(x1, x2), max(x1, x2)
            y1, y2 = min(y1, y2), max(y1, y2)
            enclosure = enclosure.union(Rectangle(x1, y1, x2, y2))
            height = max(height, y1, y2)
            if x1 == x2:
                for y in range(y1, y2 + 1):
                    grid[(x1, y)] = ROCK
            elif y1 == y2:
                for x in range(x1, x2 + 1):
                    grid[(x, y1)] = ROCK
            else:
                raise ValueError("Wasn't expecting a diagonal!")
    # set the floor at two spaces below the lowest item
    height += 2
    return enclosure, grid, height


def inject_sand(grid, enclosure, check_function):
    sand_count = 0
    next_sand = SAND_ORIGIN
    frontier = Stack()
    while check_function(grid, enclosure, next_sand):
        sand = next_sand
        air_found = False
        for offset in [Point(0, 1), Point(-1, 1), Point(1, 1)]:
            next_sand = sand + offset
            if grid[tuple(next_sand)] == AIR:
                frontier.push(next_sand)
                air_found = True
                break
        if air_found:
            continue
        grid[tuple(sand)] = SAND
        # When the sand runs out, we create some more at the origin
        if frontier.empty:
            next_sand = SAND_ORIGIN
        else:
            next_sand = frontier.pop()
        if grid[tuple(next_sand)] not in [AIR, SAND_GEN]:
            continue
        sand_count += 1
        # print(f'Sand #{sand_count}')
        # dump_grid(grid, enclosure)
    return sand_count


def part1(grid, enclosure) -> int:
    """
    """

    # Now create the sand!
    def check_function(_, encl, next_sand) -> bool:
        return encl.pt_in_rect(next_sand)

    sand_count = inject_sand(grid, enclosure, check_function)

    return sand_count


def part2(grid, enclosure, height) -> int:
    """
    """
    # Draw in the floor
    floor_left = SAND_ORIGIN.x - height - 1
    floor_right = SAND_ORIGIN.x + height + 1
    for x in range(floor_left, floor_right + 1):
        grid[(x, height)] = ROCK

    # Now create the sand!
    def check_function(grd, *_) -> bool:
        return AIR in (grd[499, 1], grd[500, 1], grd[501, 1])

    sand_count = inject_sand(grid, enclosure, check_function)

    sand_count += 1
    # print(f'Sand #{sand_count}')
    # dump_grid(grd, enclosure)

    return sand_count


def main():
    loader = LoaderLib(2022)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(14)
    else:
        # input_text = (Path.cwd() / 'testdata.txt').read_text().strip('\n')
        input_text = dedent('''\
            498,4 -> 498,6 -> 496,6
            503,4 -> 502,4 -> 502,9 -> 494,9
        ''').strip('\n')

    lines = lines_to_list(input_text)
    enclosure, grid1, height = setup_grid(lines)
    grid2 = deepcopy(grid1)

    loader.print_solution('setup', f'{len(lines)} ...')
    loader.print_solution(1, part1(grid1, enclosure))
    loader.print_solution(2, part2(grid2, enclosure, height))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.050608        |        0.050608 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 151 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.053379        |        0.103987 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 768
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 1.319365        |        1.423351 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 26686
    # --------------------------------------------------------------------------------
