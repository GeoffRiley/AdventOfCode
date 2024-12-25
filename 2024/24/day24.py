"""
Advent of code 2024
Day 24: Crossed Wires
"""

import operator
from textwrap import dedent
from typing import Any, Literal

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


class CircuitComputationError(Exception):
    """Raised when circuit outputs cannot be fully computed."""

    pass


def Solve(rules: list, wire_values: dict, z_outputs: set) -> Any | Literal[0]:
    """
    Solve a circuit simulation problem with given rules and wire values.

    Computes the output values for a set of circuit outputs by applying
    transformation rules to wire values. The function iteratively processes
    rules until all target outputs are computed.

    Args:
        rules: A list of rule tuples containing input wires, operation, and
            output wire.
        wire_values: A dictionary mapping wire names to their current values.
        z_outputs: A set of output wire names to be computed.

    Returns:
        The computed result as an integer, or 0 if computation cannot complete.

    Raises:
        AssertionError: If a rule computation results in a None value.
    """
    Done = set()
    remaining_outputs = len(z_outputs)

    lend = len(Done)
    while remaining_outputs > 0:
        for ip, op in rules:
            if op in Done:
                continue
            a, bl, b = ip
            if a in wire_values and b in wire_values:
                ans = None
                ans = bl(wire_values[a], wire_values[b])
                assert ans is not None
                wire_values[op] = ans
                Done.add(op)
                if op in z_outputs:
                    remaining_outputs -= 1
        if len(Done) == lend:
            # If we made no progress in this iteration, some outputs couldn't be computed
            uncomputed = set(z_outputs) - Done
            raise CircuitComputationError(
                f"Unable to compute outputs: {uncomputed}. Circuit may have missing or circular dependencies."
            )
        else:
            lend = len(Done)

    bits = sorted(z_outputs, reverse=True)
    ans = 0
    for b in bits:
        ans = ans << 1
        ans += wire_values[b]
    return ans


def TestAdder(swaps: set, rules: list, num: int, carry: int) -> str | Any | None:
    """
    Perform a complex adder test with bitwise operations and rule processing.

    Analyzes a set of bitwise operation rules to determine wire connections
    and potential swaps. The function systematically checks XOR, AND, and OR
    operations to identify specific wire transformations.

    Args:
        swaps: A set to track wire swaps during the test.
        rules: A list of rules defining bitwise operations between wires.
        num: A numeric identifier used to generate wire names.
        carry: The carry wire for bitwise addition operations.

    Returns:
        A wire name or None based on the rule processing results.
    """

    x = f"x{num:02}"
    y = f"y{num:02}"
    z = f"z{num:02}"

    xor1 = None
    xor2 = None
    and1 = None
    and2 = None
    for rule in rules:
        a, o, b = rule[0]
        if o == operator.xor and x in [a, b] and y in [a, b]:
            xor1 = rule[1]
        if o == operator.and_ and x in [a, b] and y in [a, b]:
            and1 = rule[1]

    if and1 == z:
        swaps.add(and1)

    for rule in rules:
        a, o, b = rule[0]
        if o == operator.xor and xor1 in [a, b] and carry in [a, b] and rule[1] != z:
            swaps.add(rule[1])
            swaps.add(z)

        if o == operator.and_ and xor1 in [a, b] and carry in [a, b]:
            and2 = rule[1]

    if and2 is None:
        swaps.add(and1)
        swaps.add(xor1)
        (and1, xor1) = (xor1, and1)
        for rule in rules:
            a, o, b = rule[0]
            if (
                o == operator.xor
                and xor1 in [a, b]
                and carry in [a, b]
                and rule[1] != z
            ):
                swaps.add(rule[1])
                swaps.add(z)

            if o == operator.and_ and xor1 in [a, b] and carry in [a, b]:
                and2 = rule[1]

    if and2 == z:
        swaps.add(and2)

    for rule in rules:
        a, o, b = rule[0]
        if o == operator.xor and xor1 in [a, b] and carry in [a, b]:
            xor2 = rule[1]
            break
    if xor2 != z:
        swaps.add(z)
        swaps.add(rule[1])
        if and1 == z:
            xor2 = z
            and1 = rule[1]

    for rule in rules:
        a, o, b = rule[0]
        if o == operator.or_ and and1 in [a, b] and and2 in [a, b]:
            if rule[1] == z:
                swaps.add(rule[1])
                if xor2 in swaps:
                    return xor2
            return rule[1]
        elif o == operator.or_ and and1 in [a, b] and xor2 in [a, b]:
            return rule[1]


def part1(
    rules,
    z_outputs,
    wire_values,
) -> int:
    """ """
    return Solve(rules, wire_values.copy(), z_outputs)


def part2(
    rules,
    z_outputs,
    wire_values,
) -> int:
    """ """
    carry = 0
    for r in rules:
        a, o, b = r[0]
        if a in ["x00", "y00"] and b in ["x00", "y00"] and o == operator.and_:
            carry = r[1]
            break

    swaps = set()
    for i in range(1, len(z_outputs) - 1):
        carry = TestAdder(swaps, rules, i, carry)

    return ",".join(sorted(swaps))


def main():
    loader = LoaderLib(2024)
    testing, variant = False, 2
    if not testing:
        input_text = loader.get_aoc_input(24)
    else:
        input_text_1 = dedent(
            """\
                x00: 1
                x01: 1
                x02: 1
                y00: 0
                y01: 1
                y02: 0

                x00 AND y00 -> z00
                x01 XOR y01 -> z01
                x02 OR y02 -> z02
            """
        ).strip("\n")
        input_text_2 = dedent(
            """\
                x00: 1
                x01: 0
                x02: 1
                x03: 1
                x04: 0
                y00: 1
                y01: 1
                y02: 1
                y03: 1
                y04: 1

                ntg XOR fgs -> mjb
                y02 OR x01 -> tnw
                kwq OR kpj -> z05
                x00 OR x03 -> fst
                tgd XOR rvg -> z01
                vdt OR tnw -> bfw
                bfw AND frj -> z10
                ffh OR nrd -> bqk
                y00 AND y03 -> djm
                y03 OR y00 -> psh
                bqk OR frj -> z08
                tnw OR fst -> frj
                gnj AND tgd -> z11
                bfw XOR mjb -> z00
                x03 OR x00 -> vdt
                gnj AND wpb -> z02
                x04 AND y00 -> kjc
                djm OR pbm -> qhw
                nrd AND vdt -> hwm
                kjc AND fst -> rvg
                y04 OR y02 -> fgs
                y01 AND x02 -> pbm
                ntg OR kjc -> kwq
                psh XOR fgs -> tgd
                qhw XOR tgd -> z09
                pbm OR djm -> kpj
                x03 XOR y03 -> ffh
                x00 XOR y04 -> ntg
                bfw OR bqk -> z06
                nrd XOR fgs -> wpb
                frj XOR qhw -> z04
                bqk OR frj -> z07
                y03 OR x01 -> nrd
                hwm AND bqk -> z03
                tgd XOR rvg -> z12
                tnw OR pbm -> gnj
            """
        ).strip("\n")
        input_text = input_text_1 if variant == 1 else input_text_2
    # lines = [
    #     (extract_ints(param)) for param in [line for line in lines_to_list(input_text)]
    # ]
    lines = [lines_to_list(line) for line in input_text.split("\n\n")]
    # lines = lines_to_list(input_text)

    rules = []
    z_outputs = set()
    for op in lines[1]:
        inp, out = op.split(" -> ")
        a, op, b = inp.split()
        if op == "AND":
            op = operator.and_
        if op == "OR":
            op = operator.or_
        if op == "XOR":
            op = operator.xor
        rules.append(((a, op, b), out))
        if out.startswith("z"):
            z_outputs.add(out)

    wire_values = {}
    for gate in lines[0]:
        gate, val = gate.split(": ")
        wire_values[gate] = val == "1"

    loader.print_solution(
        "setup", f"{len(rules)=}, {len(z_outputs)=}, {len(wire_values)=} ..."
    )
    loader.print_solution(
        1,
        part1(
            rules,
            z_outputs,
            wire_values,
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
            rules,
            z_outputs,
            wire_values,
        ),
    )


if __name__ == "__main__":
    main()
    # --
    # --------------------------------------------------------------------------------
    # LAP -> 0.000448        |        0.000448 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : len(rules)=222, len(z_outputs)=46, len(wire_values)=90 ...
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.000377        |        0.000825 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 53325321422566
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.001699        |        0.002524 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 2   : fkb,nnr,rdn,rqf,rrn,z16,z31,z37
    # --------------------------------------------------------------------------------
