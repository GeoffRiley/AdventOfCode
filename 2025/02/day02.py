"""
Advent of code 2025
Day 02: Gift Shop
"""

import re
from textwrap import dedent

from aoc.loader import LoaderLib


def part1(lines: list[str]) -> int:
    """ """
    count = 0
    #
    for line in lines:
        s, e = line.split('-')
        for i in range(int(s), int(e) + 1):
            si = str(i)
            l = len(si)
            if l % 2 == 0 and si[:l // 2] == si[l // 2:]:
                count += i

    return count


def part2(lines: list[str]) -> int:
    """ """
    r = re.compile(r'^(\d+?)\1+$')
    count = 0
    for line in lines:
        s, e = line.split('-')
        for i in range(int(s), int(e) + 1):
            si = str(i)
            if r.match(si):
                count += i
    return count


def main():
    loader = LoaderLib(2025)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(2)
    else:
        input_text = dedent(
            """\
                11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124
            """
        ).strip("\n")
    # lines = [(extract_ints(param)) for param in list(lines_to_list(input_text))]
    # lines = [lines_to_list(line) for line in input_text.split("\n\n")]
    # lines = lines_to_list(input_text)
    lines = input_text.split(',')

    loader.print_solution("setup", f"{len(lines)=} ...")
    loader.print_solution(
        1,
        part1(
            lines,
        ),
    )

    # if testing:
    #     input_text = dedent(
    #         """\
    #         """
    #     ).strip("\n")
    #     lines = lines_to_list(input_text)

    loader.print_solution(
        2,
        part2(
            lines,
        ),
    )


if __name__ == "__main__":
    main()
    # --
    # --------------------------------------------------------------------------------
    #  LAP -> 0.000223        |        0.000223 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : len(lines)=36 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.643700        |        0.643923 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 28146997880
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 1.369189        |        2.013112 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 40028128307
    # --------------------------------------------------------------------------------
