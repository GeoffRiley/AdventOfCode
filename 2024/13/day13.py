"""
Advent of code 2024
Day 13: Claw Contraption
"""

from fractions import Fraction

from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import extract_ints, lines_to_list


def valid(n: Fraction) -> bool:
    return n is not None and n.denominator == 1


def solve_all_claw_machines(
    machines, part2: bool = False
) -> tuple[None, None] | tuple[int, int]:
    """
    Solve for all claw machines and return total cost and count of prizes won.

    Each machine is a tuple of 6 integers:
    (a1, b1, a2, b2, p1, p2)

    In equation form:
    a1*x + b1*y = p1
    a2*x + b2*y = p2

    Using Cramer's Rule:
    x = (p1 * b2 - p2 * b1) / (a1 * b2 - a2 * b1)
    y = (a1 * p2 - a2 * p1) / (a1 * b2 - a2 * b1)

    The cost function is: cost = 3 * x + y
    """
    total_cost = 0
    prizes_won = 0

    for a1, b1, a2, b2, p1, p2 in machines:
        # print(f"*** Solving for {a1=} {b1=} {a2=} {b2=} {p1=} {p2=}")
        # Calculate the determinant:
        determinant = a1 * b2 - a2 * b1
        # print(f"    {determinant=} = {a1=} * {b2=} - {a2=} * {b1=}")
        if determinant == 0:
            return None, None

        # Work in fractions from here to avoid floating point errors
        # Solve the simultaneous equations
        a_presses = Fraction(p1 * b2 - p2 * b1, determinant)
        # print(f"    {a_presses=} = ({p1=} * {b2=} - {p2=} * {b1=}) / {determinant=}")
        b_presses = Fraction(a1 * p2 - a2 * p1, determinant)
        # print(f"    {b_presses=} = ({a1=} * {p2=} - {a2=} * {p1=}) / {determinant=}")

        if (
            valid(a_presses)
            and valid(b_presses)
            and (part2 or (0 <= a_presses <= 100 and 0 <= b_presses <= 100))
        ):
            total_cost += 3 * int(a_presses) + int(b_presses)
            prizes_won += 1
        # print(f"*** *** {a_presses=} {b_presses=}")

    return prizes_won, total_cost


def part1(lines: list[str]) -> int:
    # Parse the input lines to get the claw machines
    # machines = [(a1, b1, p1, a2, b2, p2) for a1, b1, p1, a2, b2, p2 in lines]
    machines = []
    # Each line has 3 parts: Button A, Button B, Prize
    # These are simultaneous equations of the form:
    # a1*x + b1*y = p1 and a2*x + b2*y = p2
    for line in lines:
        a1, a2 = extract_ints(line[0])
        b1, b2 = extract_ints(line[1])
        p1, p2 = extract_ints(line[2])
        # Add the claw machine to the list of machines
        machines.append((a1, b1, a2, b2, p1, p2))

    # The cost function is: cost = 3 * x + y
    # where x is the number of times Button A is pressed
    # and y is the number of times Button B is pressed.
    prizes_won, total_cost = solve_all_claw_machines(machines)
    return f"{prizes_won=} for a total cost of {total_cost=}"


def part2(lines: list[str]) -> int:
    """add 10000000000000 to x and y"""
    machines = []
    # Each line has 3 parts: Button A, Button B, Prize
    # These are simultaneous equations of the form:
    # a1*x + b1*y = p1 and a2*x + b2*y = p2
    for line in lines:
        a1, a2 = extract_ints(line[0])
        b1, b2 = extract_ints(line[1])
        p1, p2 = extract_ints(line[2])
        # Add the claw machine to the list of machines
        machines.append((a1, b1, a2, b2, p1 + 10000000000000, p2 + 10000000000000))

    # The cost function is: cost = 3 * x + y
    # where x is the number of times Button A is pressed
    # and y is the number of times Button B is pressed.
    prizes_won, total_cost = solve_all_claw_machines(machines, part2=True)
    return f"{prizes_won=} for a total cost of {total_cost=}"


def main():
    loader = LoaderLib(2024)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(13)
    else:
        input_text = dedent(
            """\
                Button A: X+94, Y+34
                Button B: X+22, Y+67
                Prize: X=8400, Y=5400

                Button A: X+26, Y+66
                Button B: X+67, Y+21
                Prize: X=12748, Y=12176

                Button A: X+17, Y+86
                Button B: X+84, Y+37
                Prize: X=7870, Y=6450

                Button A: X+69, Y+23
                Button B: X+27, Y+71
                Prize: X=18641, Y=10279
            """
        ).strip("\n")
    # lines = [
    #     (extract_ints(param)) for param in [line for line in lines_to_list(input_text)]
    # ]
    lines = [lines_to_list(line) for line in input_text.split("\n\n")]
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
    # -
