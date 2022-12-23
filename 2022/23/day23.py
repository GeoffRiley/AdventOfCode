"""
Advent of code 2022
Day 23: Unstable Diffusion
"""
from collections import deque, Counter
from textwrap import dedent
from typing import Set

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list

NEIGHBOURS = {
    'all': {-1 - 1j, 0 - 1j, 1 - 1j, -1 + 0j, 1 + 0j, -1 + 1j, 0 + 1j, 1 + 1j},
    'north': (0 - 1j, {-1 - 1j, 0 - 1j, 1 - 1j}),
    'south': (0 + 1j, {-1 + 1j, 0 + 1j, 1 + 1j}),
    'west': (-1 + 0j, {-1 - 1j, -1 + 0j, -1 + 1j}),
    'east': (1 + 0j, {1 - 1j, 1 + 0j, 1 + 1j}),
}
DIRECTIONS = ['north', 'south', 'west', 'east']


# def print_elves(intro: str, elf_set: Set[complex]):
#     print(intro)
#     r = [int(elf.real) for elf in elf_set]
#     i = [int(elf.imag) for elf in elf_set]
#     x_min, x_max = min(r), max(r)
#     y_min, y_max = min(i), max(i)
#     c = {tuple((x, y)) for x, y in zip(r, i)}
#     for y in range(y_min - 3, y_max + 4):
#         s = ''
#         for x in range(x_min - 3, x_max + 4):
#             s += '#' if (x, y) in c else '.'
#         print(s)
#     print()


def update_elves(directions, elf_set):
    elf_intention = {}
    elf_targets = Counter()
    unmoved = 0
    for elf in elf_set:
        if any(elf + move in elf_set for move in NEIGHBOURS['all']):
            for d in directions:
                target, checks = NEIGHBOURS[d]
                if not any(elf + move in elf_set for move in checks):
                    elf_intention[elf] = elf + target
                    elf_targets[elf + target] += 1
                    break
            else:
                elf_intention[elf] = elf
                elf_targets[elf] += 1
        else:
            # we're staying put with no neighbours
            elf_intention[elf] = elf
            elf_targets[elf] += 1
            unmoved += 1
    # Make moves
    new_elf_set = set()
    for elf in elf_set:
        elf_intent = elf_intention[elf]
        if elf_targets[elf_intent] == 1:
            new_elf_set.add(elf_intent)
        else:
            new_elf_set.add(elf)
    elf_set = new_elf_set
    return elf_set, unmoved == len(elf_set)


def part1(elf_set: Set[complex]) -> int:
    """
    We have a large set of Elf locations.
    Let's get them moving.
    """
    directions = deque(DIRECTIONS)
    # print_elves('== Initial State ==', elf_set)
    for lap in range(10):
        elf_set, _ = update_elves(directions, elf_set)
        # print_elves(f'== End of round {lap} ==', elf_set)
        directions.append(directions.popleft())

    r = [int(e.real) for e in elf_set]
    i = [int(e.imag) for e in elf_set]
    x_min, x_max = min(r), max(r)
    y_min, y_max = min(i), max(i)

    result = (x_max - x_min + 1) * (y_max - y_min + 1) - len(elf_set)

    return result


def part2(elf_set: Set[complex]) -> int:
    """
    """
    directions = deque(DIRECTIONS)
    unmoved = False
    result = 0
    while not unmoved:
        elf_set, unmoved = update_elves(directions, elf_set)
        result += 1
        directions.append(directions.popleft())

    return result


def main():
    loader = LoaderLib(2022)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(23)
    else:
        # input_text = (Path.cwd() / 'testdata.txt').read_text().strip('\n')
        input_text = dedent('''\
            ....#..
            ..###.#
            #...#.#
            .#...##
            #.###..
            ##.#.##
            .#..#..
        ''').strip('\n')

    lines = lines_to_list(input_text)

    elf_set = set()
    for y, r in enumerate(lines):
        for x, c in enumerate(r):
            if c == '#':
                elf_set.add(x + y * 1j)

    loader.print_solution('setup', f'{len(elf_set)} ...')
    loader.print_solution(1, part1(elf_set))
    loader.print_solution(2, part2(elf_set))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.006635        |        0.006635 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 2578 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.483554        |        0.490188 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 4146
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 34.806464       |       35.296653 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 957
    # --------------------------------------------------------------------------------
