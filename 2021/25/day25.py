"""
Advent of code 2021
Day 25:
"""

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


def grid_adust(shape, position, direction):
    x, y = position
    if direction == '>':
        x += 1
        if x >= shape[0]:
            x = 0
    else:
        y += 1
        if y >= shape[1]:
            y = 0
    return x, y


def move_cucumbers(shape, easterly, southerly):
    moved = False

    new_easterly = set()
    for x, y in easterly:
        new_pos = ((x + 1) % shape[0], y)
        if new_pos in easterly or new_pos in southerly:
            new_easterly.add((x, y))
        else:
            new_easterly.add(new_pos)
            moved = True
    easterly = new_easterly

    new_southerly = set()
    for x, y in southerly:
        new_pos = (x, (y + 1) % shape[1])
        if new_pos in easterly or new_pos in southerly:
            new_southerly.add((x, y))
        else:
            new_southerly.add(new_pos)
            moved = True
    southerly = new_southerly

    return easterly, southerly, moved


def part1(grid, shape):
    """
    """
    easterly = {k for k, v in grid.items() if v == '>'}
    southerly = {k for k, v in grid.items() if v == 'v'}
    move_count = 0
    moved = True
    while moved:
        move_count += 1
        easterly, southerly, moved = move_cucumbers(shape, easterly, southerly)

    return f"No movement after {move_count} moves."


def part2():
    """
    """

    return "No part 2! ;)"


def main():
    loader = LoaderLib(2021)
    input_text = loader.get_aoc_input(25)

    #     input_text = """v...>>.vv>
    # .vv>>.vv..
    # >>.>v>...v
    # >>v>>.>.v.
    # v>v.vv.v..
    # >.>>..v...
    # .vv..>.>v.
    # v.v..>>v.v
    # ....v..v.>"""

    lines = lines_to_list(input_text)
    grid = {(x, y): v for y, line in enumerate(lines) for x, v in enumerate(line)}

    # assert len(lines) == len(...)
    loader.print_solution('setup', f'{len(grid)} ...')
    loader.print_solution(1, part1(grid.copy(), (len(lines[0]), len(lines))))
    loader.print_solution(2, part2())


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.016809        |        0.016809 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 19043 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 7.283629        |        7.300438 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : No movement after 489 moves.
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.001423        |        7.301860 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : No part 2! ;)
    # --------------------------------------------------------------------------------
