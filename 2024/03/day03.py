"""
Advent of code 2024
Day 03: Mull It Over
"""

import re
from textwrap import dedent

from aoc.loader import LoaderLib


def part1(lines: str) -> int:
    """ """
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    total = 0
    for x, y in re.findall(pattern, lines):
        total += int(x) * int(y)
    return total


def part2(lines: str) -> int:
    """ """
    mul_pattern = re.compile(r"mul\((\d+),(\d+)\)")
    do_pattern = re.compile(r"do\(\)")
    dont_pattern = re.compile(r"don't\(\)")
    total = 0
    enabled = True
    working_tokens = re.split(r"(do\(\)|don't\(\)|mul\(\d{1,3},\d{1,3}\))", lines)
    for tok in working_tokens:
        if do_pattern.match(tok):
            enabled = True
        elif dont_pattern.match(tok):
            enabled = False
        elif vars := mul_pattern.match(tok):
            if enabled:
                x, y = map(int, vars.groups())
                total += x * y
    return total


def main():
    loader = LoaderLib(2024)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(3)
    else:
        input_text = dedent(
            """\
                xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
            """
        ).strip("\n")
    # lines = [
    #     (extract_ints(param)) for param in [line for line in lines_to_list(input_text)]
    # ]
    # lines = [lines_to_list(line) for line in input_text.split("\n\n")]
    # lines = lines_to_list(input_text)
    lines = input_text

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
    # LAP -> 0.000127        |        0.000127 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : len(lines)=19738 ...
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.000369        |        0.000496 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 183669043
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.000845        |        0.001342 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 2   : 59097164
    # --------------------------------------------------------------------------------
