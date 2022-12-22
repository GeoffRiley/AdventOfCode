"""
Advent of code 2022
Day 20: Grove Positioning System
"""
from textwrap import dedent
from typing import List, Tuple

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list_int


def do_the_mix_thing(orig_list: List[Tuple[int, int]], mixed: List[Tuple[int, int]]):
    mixed_wrap = len(mixed) - 1
    for orig_pos, number in orig_list:
        from_idx = mixed.index((orig_pos, number))
        to_idx = (from_idx + number) % mixed_wrap
        mixed.insert(to_idx, mixed.pop(from_idx))
    zero_idx = [x[1] for x in mixed].index(0)
    return zero_idx


def part1(lines: List[int]) -> int:
    """
    """
    mixed = [(pos, line) for pos, line in enumerate(lines)]
    orig_list = mixed.copy()
    zero_idx = do_the_mix_thing(orig_list, mixed)
    return sum(mixed[(zero_idx + offset) % len(mixed)][1] for offset in [1000, 2000, 3000])


def part2(lines: List[int]) -> int:
    """
    """
    decryption_key = 811589153
    mixed = [(pos, line * decryption_key) for pos, line in enumerate(lines)]
    orig_list = mixed.copy()
    zero_idx = 0
    for _ in range(10):
        zero_idx = do_the_mix_thing(orig_list, mixed)
    return sum((mixed[(zero_idx + offset) % len(mixed)][1]) for offset in [1000, 2000, 3000])


def main():
    loader = LoaderLib(2022)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(20)
    else:
        # input_text = (Path.cwd() / 'testdata.txt').read_text().strip('\n')
        input_text = dedent('''\
            1
            2
            -3
            3
            -2
            0
            4
        ''').strip('\n')

    lines = lines_to_list_int(input_text)

    # assert len(lines) == len(...)
    loader.print_solution('setup', f'{len(lines)} ...')
    loader.print_solution(1, part1(lines))
    loader.print_solution(2, part2(lines))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.006392        |        0.006392 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 5000 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.610486        |        0.616878 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 3700
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 10.459152       |       11.076030 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 10626948369382
    # --------------------------------------------------------------------------------
