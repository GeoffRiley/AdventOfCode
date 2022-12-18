"""
Advent of code 2022
Day 18: Boiling Boulders
"""
from itertools import combinations, tee
from textwrap import dedent
from typing import List, Tuple, Any

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list, extract_ints


def part1(blocks: List[List[int]]) -> int:
    """
    Single blocks are located at the (x,y,z) coordinates held in the blocks list
    """
    # if all were separate, then each would have six sides
    side_count = len(blocks) * 6

    # Now we can scan through all the combinations of blocks to find those
    # that are adjacent and subtract the two facing sides
    for cube1, cube2 in combinations(blocks, 2):
        if (
                abs(cube1[0] - cube2[0]) +
                abs(cube1[1] - cube2[1]) +
                abs(cube1[2] - cube2[2])
        ) == 1:
            side_count -= 2

    return side_count


def minmax(*args) -> Tuple[Any, Any]:
    args1, args2 = tee(*args)
    mn = min(*list(args1))
    mx = max(*list(args2))
    return mn, mx


# Cell states
UNKNOWN = 0
WATER = 1
LAVA = 2

# Coordinates of adjoining cells
NEIGHBOURS = [
    (-1, 0, 0),
    (0, -1, 0),
    (0, 0, -1),
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1)
]


def part2(blocks: List[List[int]]) -> int:
    """
    We need the outer dimensions of the enclosing cube in order to evaluate
    the inner positions

    Probably better done with 'pandas' for the arrays
    """
    min_x, max_x = minmax(b[0] for b in blocks)
    min_y, max_y = minmax(b[1] for b in blocks)
    min_z, max_z = minmax(b[2] for b in blocks)

    # set up our outer cube of water—insides unknown
    cells = []
    for x in range(0, max_x + 2):
        cells_x = []
        for y in range(0, max_y + 2):
            cells_y = []
            for z in range(0, max_z + 2):
                if (
                        x in (min_x, max_x) or
                        y in (min_y, max_y) or
                        z in (min_z, max_z)
                ):
                    cells_y.append(WATER)
                else:
                    cells_y.append(UNKNOWN)
            cells_x.append(cells_y)
        cells.append(cells_x)

    # 'plop' in our lava
    for x, y, z in blocks:
        cells[x][y][z] = LAVA

    # Now we can go around growing the water into the unknown areas
    while True:
        grown = False
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                for z in range(min_z, max_z + 1):
                    if cells[x][y][z] == UNKNOWN:
                        # See if there's water in the neighbours and suck it in
                        for x1, y1, z1 in NEIGHBOURS:
                            if cells[x + x1][y + y1][z + z1] == WATER:
                                cells[x][y][z] = WATER
                                grown = True
        # If we didn't increase the water, just leave
        if not grown:
            break

    # Now to tot up the sides
    sides = 0
    for x, y, z in blocks:
        # check for water on each side—max and min always have water
        for x1, y1, z1 in NEIGHBOURS:
            x1, y1, z1 = x + x1, y + y1, z + z1
            if x1 < min_x or x1 > max_x or y1 < min_y or y1 > max_y or z1 < min_z or z1 > max_z:
                sides += 1
            else:
                if cells[x1][y1][z1] == WATER:
                    sides += 1

    return sides


def main():
    loader = LoaderLib(2022)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(18)
    else:
        # input_text = (Path.cwd() / 'testdata.txt').read_text().strip('\n')
        input_text = dedent('''\
            2,2,2
            1,2,2
            3,2,2
            2,1,2
            2,3,2
            2,2,1
            2,2,3
            2,2,4
            2,2,6
            1,2,5
            3,2,5
            2,1,5
            2,3,5
        ''').strip('\n')

    blocks = [extract_ints(line) for line in lines_to_list(input_text)]

    loader.print_solution('setup', f'{len(blocks)} ...')
    loader.print_solution(1, part1(blocks))
    loader.print_solution(2, part2(blocks))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.042539        |        0.042539 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 2694 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 8.628574        |        8.671113 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 4580
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.108845        |        8.779958 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 2610
    # --------------------------------------------------------------------------------
