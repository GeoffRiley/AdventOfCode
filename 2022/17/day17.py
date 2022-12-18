"""
Advent of code 2022
Day 17: Pyroclastic Flow
"""
from itertools import cycle
from math import floor
from textwrap import dedent
from typing import List

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list

ROCK_CHUNKS = [
    [0b00111100],
    [0b00010000,
     0b00111000,
     0b00010000],
    [0b00111000,
     0b00001000,
     0b00001000],
    [0b00100000,
     0b00100000,
     0b00100000,
     0b00100000],
    [0b00110000,
     0b00110000]
]
WELL_WALL = 0b100000001


def chunk_to_bin(chunk):
    h = '[' + ','.join(format(v, "09b") for v in chunk) + ']'
    return h


def print_well(well: List[int]) -> None:
    for n in reversed(well):
        print(''.join('.#'[int(x)] for x in (format(n, "09b"))))
    print()


def well_height(well):
    height = len(well) - 1
    while well[height] == WELL_WALL:
        height -= 1
    return height


def part1(lines: List[str]) -> int:
    """
    """
    well = [0b111111111]
    wind = cycle(enumerate(lines[0]))
    for rock_number, r_index in zip(range(2022), cycle(range(len(ROCK_CHUNKS)))):
        # top up well—three clear spaces above the highest item
        # currently in the well
        while well[-3:] != [WELL_WALL, WELL_WALL, WELL_WALL]:
            well.append(WELL_WALL)
        chunk = ROCK_CHUNKS[r_index]
        well_pos = len(well)
        while True:
            _, blow = next(wind)
            if blow == '<':
                test_chunk = [c * 2 for c in chunk]
            else:
                test_chunk = [c // 2 for c in chunk]

            if all((c & w) == 0 for c, w in
                   zip(test_chunk, well[well_pos:well_pos + len(test_chunk) + 3])):
                chunk = test_chunk

            if all((c & w) == 0 for c, w in
                   zip(chunk, well[well_pos - 1:well_pos + len(chunk) + 3])):
                well_pos -= 1
            else:
                for p, e in zip(range(well_pos, well_pos + len(chunk)), chunk):
                    if p < len(well):
                        well[p] |= e
                    else:
                        well.append(WELL_WALL | e)
                break

    result = well_height(well)
    return result


def part2(lines: List[str]) -> int:
    """
    """
    well = [0b111111111]
    wind = cycle(enumerate(lines[0]))
    repeat_cycles = set()
    repeat_at = dict()
    w_index = 0
    target_rocks = 1_000_000_000_000
    rock_number = 0
    rock_pick = cycle(range(len(ROCK_CHUNKS)))
    pattern_matched = False
    extra_height = 0
    while rock_number < target_rocks:
        r_index = next(rock_pick)
        # top up well—three clear spaces above the highest item
        # currently in the well
        while well[-3:] != [WELL_WALL, WELL_WALL, WELL_WALL]:
            well.append(WELL_WALL)
        chunk = ROCK_CHUNKS[r_index]
        well_pos = len(well)
        while True:
            w_index, blow = next(wind)
            if blow == '<':
                test_chunk = [c * 2 for c in chunk]
            else:
                test_chunk = [c // 2 for c in chunk]

            if all((c & w) == 0 for c, w in
                   zip(test_chunk, well[well_pos:well_pos + len(test_chunk) + 3])):
                chunk = test_chunk

            if all((c & w) == 0 for c, w in
                   zip(chunk, well[well_pos - 1:well_pos + len(chunk) + 3])):
                well_pos -= 1
            else:
                for p, e in zip(range(well_pos, well_pos + len(chunk)), chunk):
                    if p < len(well):
                        well[p] |= e
                    else:
                        well.append(WELL_WALL | e)
                break

        if len(well) > 50 and not pattern_matched:
            pattern = (w_index, r_index, tuple(well[-20:]))
            if pattern in repeat_cycles:
                delta_height = well_height(well) - repeat_at[pattern][0]
                delta_rock = rock_number - repeat_at[pattern][1]
                rocks_left_cycles = floor((target_rocks - rock_number) / delta_rock)
                rock_number += delta_rock * rocks_left_cycles
                extra_height = delta_height * rocks_left_cycles
                pattern_matched = True
            else:
                repeat_cycles.add(pattern)
                repeat_at[pattern] = (well_height(well), rock_number)

        rock_number += 1

    result = well_height(well) + extra_height
    return result


def main():
    loader = LoaderLib(2022)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(17)
    else:
        # input_text = (Path.cwd() / 'testdata.txt').read_text().strip('\n')
        input_text = dedent('''\
            >>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
        ''').strip('\n')

    lines = lines_to_list(input_text)

    loader.print_solution('setup', f'{len(lines)} ...')
    loader.print_solution(1, part1(lines))  # 2022
    loader.print_solution(2, part2(lines))  # 1_000_000_000_000


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.002523        |        0.002523 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 1 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.150224        |        0.152747 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 3239
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.224940        |        0.377686 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 1594842406882
    # --------------------------------------------------------------------------------
