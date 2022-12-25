"""
Advent of code 2022
Day 24: Blizzard Basin
"""
from textwrap import dedent
from typing import List, Dict, Tuple, Set

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list

DIRECTIONS = {
    '>': (0, 1),
    '<': (0, -1),
    'v': (1, 0),
    '^': (-1, 0),
    0: (0, 0)
}

TICK = WIDTH = HEIGHT = 0
BLIZZARDS = None


def build_grid(lines: List[str]):
    global WIDTH, HEIGHT
    WIDTH, HEIGHT = len(lines[0]) - 2, len(lines) - 2
    blizzards = {
        (i, j, lines[i + 1][j + 1])
        for i in range(HEIGHT)
        for j in range(WIDTH)
        if lines[i + 1][j + 1] not in ('#', '.')
    }
    parameters = {
        'start': (-1, 0),
        'finish': (HEIGHT, WIDTH - 1)
    }
    return blizzards, parameters


def find_route(start, finish, blizzards_in):
    global TICK, BLIZZARDS
    pos = [(start[0], start[1], TICK)]
    seen = set()
    while pos:
        loc_x, loc_y, tick = pos.pop(0)
        if BLIZZARDS is None or tick > TICK:  # evolve
            BLIZZARDS = blizzards_in
            blizzards_in = {
                (
                    (i + DIRECTIONS[c][0]) % HEIGHT,
                    (j + DIRECTIONS[c][1]) % WIDTH,
                    c
                )
                for i, j, c in BLIZZARDS
            }
            TICK = tick

        for X, Y in ((loc_x + x, loc_y + y)
                     for x, y in DIRECTIONS.values()):
            if (X, Y) == finish:
                return blizzards_in
            if ((X, Y) != start) and (X < 0 or Y < 0 or X >= HEIGHT or Y >= WIDTH):
                continue
            if any(1 for d in DIRECTIONS.keys() if d and (X, Y, d) in blizzards_in):
                continue

            n = (X, Y, tick + 1)
            if n not in seen:
                pos.append(n)
                seen.add(n)


def part1(blizzards: Set[Tuple[Tuple[int, int], Tuple[int, int]]],
          parameters: Dict[str, Tuple[int, int]]) -> int:
    """
    """
    part1.blizzards = find_route(parameters['start'], parameters['finish'], blizzards)

    return TICK + 1


part1.blizzards = None


def part2(blizzards: Set[Tuple[Tuple[int, int], Tuple[int, int]]],
          parameters: Dict[str, Tuple[int, int]]) -> int:
    """
    """
    blizzards = find_route(parameters['finish'], parameters['start'], blizzards)
    part2.blizzards = find_route(parameters['start'], parameters['finish'], blizzards)

    return TICK + 1


def main():
    loader = LoaderLib(2022)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(24)
    else:
        # input_text = (Path.cwd() / 'testdata.txt').read_text().strip('\n')
        input_text = dedent('''\
            #.######
            #>>.<^<#
            #.<..<<#
            #>v.><>#
            #<^v^^>#
            ######.#
        ''').strip('\n')

    lines = lines_to_list(input_text)
    blizzards, parameters = build_grid(lines)

    loader.print_solution('setup', f'{len(blizzards)} ({parameters}) ...')
    loader.print_solution(1, part1(blizzards, parameters))
    # Sneaky passing updated blizzard out of part1 to avoid yet another global variable!!
    loader.print_solution(2, part2(part1.blizzards, parameters))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.010132        |        0.010132 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 3162 ({'start': (-1, 0), 'finish': (35, 99)}) ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 4.853624        |        4.863756 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 225
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 10.310220       |       15.173976 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 711
    # --------------------------------------------------------------------------------
