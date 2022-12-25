"""
Advent of code 2022
Day 25: Full of Hot Air
"""
from functools import lru_cache
from textwrap import dedent
from typing import List

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


def decimal_to_snafu(i: int):
    digits = []
    while i:
        carry = 0
        r = i % 5
        if r < 3:
            digits.append(str(r))
        else:
            digits.append('=-'[r - 3])
            carry = 1
        i = i // 5 + carry

    return ''.join(digits[::-1])


@lru_cache()
def snafu_to_decimal(s):
    convert_string = "=-012"
    a, b = s[:-1], s[-1]
    v = convert_string.index(b) - 2
    if a:
        return snafu_to_decimal(a) * 5 + v
    else:
        return v


def part1(lines: List[str]) -> str:
    """
    """
    v = sum(snafu_to_decimal(s) for s in lines)

    return f'{v}:  {decimal_to_snafu(v)}'


def part2(lines: List[str]) -> int:
    """
    """

    return NotImplemented


def main():
    loader = LoaderLib(2022)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(25)
    else:
        # input_text = (Path.cwd() / 'testdata.txt').read_text().strip('\n')
        input_text = dedent('''\
            1=-0-2
            12111
            2=0=
            21
            2=01
            111
            20012
            112
            1=-1=
            1-12
            12
            1=
            122
        ''').strip('\n')

    lines = lines_to_list(input_text)

    # assert len(lines) == len(...)
    loader.print_solution('setup', f'{len(lines)} ...')
    loader.print_solution(1, part1(lines))
    loader.print_solution(2, part2(lines))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.002391        |        0.002391 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 120 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.002673        |        0.005064 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 31487399529835:  2=112--220-=-00=-=20
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.000216        |        0.005281 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : NotImplemented
    # --------------------------------------------------------------------------------
