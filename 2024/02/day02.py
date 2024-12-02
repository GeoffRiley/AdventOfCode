"""
Advent of code 2024
Day 02: Red-Nosed Reports
"""

from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import extract_ints, lines_to_list


def part1(grid: list[list[int]]) -> int:
    """
    How many lines are safe?
    A line is safe if adjacent numbers are at least 1, but no more than 3 apart;
    and are all in ascending or descending order.
    """
    safe = 0
    for line in grid:
        if len(line) < 2:
            continue
        if check_line_safety(line):
            safe += 1
    return safe


def check_line_safety(line):
    diffs = [a - b for a, b in zip(line[1:], line)]
    return all(d in (1, 2, 3) for d in diffs) or all(d in (-1, -2, -3) for d in diffs)


def part2(grid: list[str]) -> int:
    """
    How many lines are safe?
    A line is safe if adjacent numbers are at least 1, but no more than 3 apart;
    and are all in ascending or descending order.
    Additionally, a line may have a single defect removed and still be
    considered safe if the rules are still confirmed.
    """
    safe = 0
    for line in grid:
        if len(line) < 2:
            continue
        if any(check_line_safety(line[:i] + line[i + 1:]) for i in range(len(line))):
            safe += 1
    return safe


def main():
    loader = LoaderLib(2024)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(2)
    else:
        input_text = dedent(
            """\
                7 6 4 2 1
                1 2 7 8 9
                9 7 6 2 1
                1 3 2 4 5
                8 6 4 4 1
                1 3 6 7 9
            """
        ).strip("\n")
    # lines = [
    #     (pat, to_list_int(param))
    #     for pat, param in [line.split()
    #         for line in lines_to_list(input_text)]
    # ]
    lines = [extract_ints(line) for line in lines_to_list(input_text)]
    # lines = lines_to_list(input_text)

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
    # LAP -> 0.002165        |        0.002165 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : len(lines)=1000 ...
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.001011        |        0.003176 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 218
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.005212        |        0.008388 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 2   : 290
    # --------------------------------------------------------------------------------
