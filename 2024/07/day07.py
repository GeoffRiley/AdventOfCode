"""
Advent of code 2024
Day 07: Bridge Repair
"""

from itertools import product
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import extract_ints, lines_to_list


def evaluate_expression(numbers, operators):
    """
    Evaluates the expression with given numbers and operators left-to-right.
    """
    result = numbers[0]
    for i, op in enumerate(operators):
        if op == "+":
            result += numbers[i + 1]
        elif op == "*":
            result *= numbers[i + 1]
        elif op == "|":
            result = int(str(result) + str(numbers[i + 1]))
    return result


def get_calibration(lines, operator_set):
    total_calibration = 0
    for line in lines:
        # Parse test value and numbers
        test_value, numbers = line

        # Get all combinations of operators
        operator_count = len(numbers) - 1

        operator_combinations = product(operator_set, repeat=operator_count)

        # Check if any combination produces the test value
        for ops in operator_combinations:
            if evaluate_expression(numbers, ops) == test_value:
                total_calibration += test_value
                break
    return total_calibration


def part1(lines: list[str]) -> int:
    """ """
    operator_set = "+*"
    total_calibration = get_calibration(lines, operator_set)

    return total_calibration


def part2(lines: list[str]) -> int:
    """ """
    operator_set = "+*|"
    total_calibration = get_calibration(lines, operator_set)

    return total_calibration


def main():
    loader = LoaderLib(2024)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(7)
    else:
        input_text = dedent(
            """\
                190: 10 19
                3267: 81 40 27
                83: 17 5
                156: 15 6
                7290: 6 8 6 15
                161011: 16 10 13
                192: 17 8 14
                21037: 9 7 18 13
                292: 11 6 16 20

            """
        ).strip("\n")
    lines = [
        (int(pat), extract_ints(param))
        for pat, param in [line.split(":") for line in lines_to_list(input_text)]
    ]
    # lines = [
    #     (extract_ints(param)) for param in [line for line in lines_to_list(input_text)]
    # ]
    # lines = [lines_to_list(line) for line in input_text.split("\n\n")]
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
    # LAP -> 0.002670        |        0.002670 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : len(lines)=850 ...
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.076372        |        0.079042 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 2941973819040
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 5.636603        |        5.715645 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 2   : 249943041417600
    # --------------------------------------------------------------------------------
