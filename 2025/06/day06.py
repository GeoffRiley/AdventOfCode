"""
Advent of code 2025
Day 06: Trash Compactor
"""

from textwrap import dedent

import pandas as pd
from pandas import DataFrame

from aoc.loader import LoaderLib
from aoc.utility import (
    lines_to_list,
)

op_list = {'+': lambda x, y: x + y, '*': lambda x, y: x * y}


def part1(lines: list[str], opers: str) -> int:
    """ """
    df = pd.DataFrame([list(map(int, line.split())) for line in lines])
    total = do_calculation(df, opers)
    return total


def part2(lines: list[str], opers: str) -> int:
    """ """
    # transpose the vertical and horizontal lines
    zipped_lines = list(zip(*lines))
    rotated_lines = [''.join(row) for row in zipped_lines]
    cols = []
    current = []
    for v in rotated_lines:
        if v.strip() == '':
            cols.append(current)
            current = []
        else:
            current.append(int(v))
    cols.append(current)

    df = pd.DataFrame(col for col in cols).transpose()
    total = do_calculation(df, opers)
    return total


def do_calculation(df: DataFrame, opers: str) -> int:
    ops = opers.split()
    total = 0
    col_totals = []
    for col_name, op in zip(df.columns, ops):
        s = df[col_name]
        if op == '+':
            col_totals.append(s.sum())
        elif op == '*':
            col_totals.append(s.prod())
        else:
            raise ValueError(f"Unknown operator: {op}")
    total = sum(col_totals)
    return total


def main():
    loader = LoaderLib(2025)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(6)
    else:
        input_text = dedent(
            """\
                123 328  51 64 
                 45 64  387 23 
                  6 98  215 314
                *   +   *   +
            """
        ).strip("\n")
    # lines = [
    #     (extract_ints(param)) for param in [line for line in lines_to_list(input_text)]
    # ]
    # lines = [lines_to_list(line) for line in input_text.split("\n\n")]
    lines = lines_to_list(input_text)

    loader.print_solution("setup", f"{len(lines)=} ...")
    loader.print_solution(
        1,
        part1(
            lines[:-1],
            lines[-1]
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
            lines[:-1],
            lines[-1]
        ),
    )


if __name__ == "__main__":
    main()
    # --
    # -
    # --------------------------------------------------------------------------------
    #  LAP -> 0.000240        |        0.000240 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : len(lines)=5 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.067073        |        0.067312 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 3261038365331
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.066237        |        0.133549 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 8342588849093.0
    # --------------------------------------------------------------------------------
