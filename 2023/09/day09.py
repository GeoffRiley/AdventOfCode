"""
Advent of code 2023
Day 09: Mirage Maintenance
"""
from itertools import pairwise
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import extract_ints, lines_to_list


def part1(lines) -> int:
    """
    Each line is a list of numbers, our task is to find the next number in the
    sequence. This is achieved by finding the difference between each number
    in the list, repeatedly until we reduce the list to all zeros.
    Appending a new zero to the end of the final list and working back up the
    list, we can find the next number in the sequence.
    """
    # Find the difference between each number in the list
    new_vals = []
    for line in lines:
        diff_tails = []
        val_list = extract_ints(line, negative=True)
        diff_tails.append(val_list[-1:])
        diff = [b - a for a, b in pairwise(val_list)]
        diff_tails.append(diff[-1:])
        while set(diff) != {0}:
            diff = [b - a for a, b in pairwise(diff)]
            diff_tails.append(diff[-1:])
        # Append a zero to the end of the final list
        diff_tails[-1].append(0)
        # Work back up the list to find the next number in the sequence
        for i in range(len(diff_tails) - 1, 0, -1):
            diff_tails[i - 1].append(diff_tails[i - 1][-1] + diff_tails[i][-1])
        new_vals.append(diff_tails[0][-1])
    return sum(new_vals)


def part2(lines) -> int:
    """
    Similar to part 1, but we need to find the previous number in the sequence.
    """
    # Find the difference between each number in the list
    new_vals = []
    for line in lines:
        diff_tails = []
        val_list = extract_ints(line, negative=True)
        diff_tails.append(val_list[:1])
        diff = [b - a for a, b in pairwise(val_list)]
        diff_tails.append(diff[:1])
        while set(diff) != {0}:
            diff = [b - a for a, b in pairwise(diff)]
            diff_tails.append(diff[:1])
        # Append a zero to the end of the final list
        diff_tails[-1].append(0)
        # Work back up the list to find the next number in the sequence
        for i in range(len(diff_tails) - 1, 0, -1):
            diff_tails[i - 1].append(diff_tails[i - 1][-1] - diff_tails[i][-1])
        new_vals.append(diff_tails[0][-1])
    return sum(new_vals)


def main():
    loader = LoaderLib(2023)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(9)
    else:
        input_text = dedent(
            """\
            0 3 6 9 12 15
            1 3 6 10 15 21
            10 13 16 21 30 45
            """
        ).strip("\n")
    lines = lines_to_list(input_text)

    loader.print_solution("setup", f"{len(lines)=} ...")
    loader.print_solution(
        1,
        part1(
            lines,
        ),
    )
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
    #  LAP -> 0.000137        |        0.000137 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : len(lines)=200 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.003938        |        0.004075 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 1939607039
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.003297        |        0.007372 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 1041
    # --------------------------------------------------------------------------------
