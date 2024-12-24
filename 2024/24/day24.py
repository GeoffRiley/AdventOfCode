"""
Advent of code 2024
Day 24: Crossed Wires
"""

from collections import Counter
from enum import Enum
import re
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import (
    extract_ints,
    lines_to_list,
    to_list_int,
    batched,
    grouped,
    lines_to_list_int,
    pairwise,
    sequence_to_int,
    tee,
    to_list,
)
from aoc.binary_feeder import BinaryFeeder
from aoc.geometry import Point, Rectangle, Size
from aoc.edge import Edge
from aoc.grid import Grid
from aoc.maths import (
    factorial,
    fibonacci,
    manhattan_distance,
    sign,
)
from aoc.search import (
    astar,
    bfs,
    dfs,
    binary_contains,
    linear_contains,
    Comparable,
    Node,
    PriorityQueue,
    Queue,
    node_to_path,
    Stack,
)


def part1(lines: list[str]) -> int:
    """
    Given lines of puzzle input (strings) describing wire initial values and gates,
    returns the decimal value computed from wires starting with 'z'.
    """
    # Regexes to match lines of the form:
    #   x00: 1
    wire_re = re.compile(r"^\s*([a-zA-Z0-9]+)\s*:\s*([01])\s*$")

    #   x00 AND y00 -> z00
    #   x01 XOR y01 -> z01
    #   x02 OR  y02 -> z02
    gate_re = re.compile(
        r"^\s*([a-zA-Z0-9]+)\s+(AND|OR|XOR)\s+([a-zA-Z0-9]+)\s*->\s*([a-zA-Z0-9]+)\s*$"
    )

    # Dictionary of wire -> known boolean value (0 or 1).
    wires = {}
    # List of gates: each gate is (input1, op, input2, output_wire).
    gates = []

    # 1) Parse lines into initial wire values and gate definitions
    for line in lines[0]:
        line = line.strip()
        if not line:
            continue
        if m_init := wire_re.match(line):
            wire_name, val_str = m_init.groups()
            wires[wire_name] = int(val_str)
            continue

        raise ValueError(f"Unrecognized wire line: {line}")

    for line in lines[1]:
        line = line.strip()
        if not line:
            continue
        if m_gate := gate_re.match(line):
            in1, op, in2, out = m_gate.groups()
            gates.append((in1, op, in2, out))
            continue

        raise ValueError(f"Unrecognized gate line: {line}")

    # 2) Keep computing until no more outputs can be set
    # Because there are no loops, each gate will eventually produce its output
    # once both inputs are known.

    changed = True
    # To avoid re-evaluating gates whose outputs are already known:
    gate_done = set()

    while changed:
        changed = False
        for i, (in1, op, in2, out) in enumerate(gates):
            if out in wires:
                # Output already known; skip
                gate_done.add(i)
                continue

            # Check if input wires have known values
            val1 = wires.get(in1, None)
            val2 = wires.get(in2, None)
            if val1 is not None and val2 is not None:
                # We can compute the output!
                if op == "AND":
                    out_val = 1 if (val1 == 1 and val2 == 1) else 0
                elif op == "OR":
                    out_val = 1 if (val1 == 1 or val2 == 1) else 0
                elif op == "XOR":
                    out_val = 1 if (val1 != val2) else 0
                else:
                    raise ValueError(f"Unrecognized gate operator {op}")

                wires[out] = out_val
                gate_done.add(i)
                changed = True

        # Optionally, we could remove the gates from `gates` if done,
        # but it's enough just to mark them done and skip next time.

    # 3) Collect wires starting with 'z' and figure out the order
    #    "z00" is the least significant bit, "z01" the next, etc.
    #    We'll parse the numeric part after 'z' to get an integer index for sorting.

    z_wires = []
    for wire_name, val in wires.items():
        if wire_name.startswith("z"):
            # Extract the numeric part: e.g. "z00" -> 00 -> integer 0
            # A simple way: remove 'z' then convert the remainder to int
            # If 'z' lines can have letters, you'd need a more robust parse;
            # this puzzle uses numeric suffixes, so we can parse directly.
            try:
                index = int(wire_name[1:])
            except ValueError:
                # If there's something else after 'z', skip or handle differently
                continue
            z_wires.append((index, val))

    # Sort by integer index ascending
    z_wires.sort(key=lambda x: x[0])

    # 4) Build the binary number with z00 as LSB and zNN as MSB
    #    So z00's bit is the rightmost bit in the final binary string.
    #    We'll build from least significant to most significant:
    bit_string = "".join(
        str(bit_val) for (_, bit_val) in z_wires[::-1]
    )  # reverse for left-to-right
    # Alternatively, you can build it in normal order and then do int(bit_string, 2),
    # but be careful about reversing vs. not reversing.
    # If z00 is LSB, it should appear on the right in a binary literal, e.g. bXYZ...z00.
    #
    # If you prefer to build the binary string with z00 as rightmost, do:
    #     bit_string_reversed = "".join(str(bit_val) for (_, bit_val) in z_wires)
    #     # Then reverse it before int()
    #
    # We'll do it in a simple, direct way:
    bit_string_reversed = "".join(str(bit_val) for (_, bit_val) in z_wires)
    # Now z00 is at the left of that string, so we reverse it:
    bit_string = bit_string_reversed[::-1]
    if not bit_string:
        # No z wires at all, interpret that as 0
        return 0

    # 5) Convert to decimal
    decimal_value = int(bit_string, 2)
    return decimal_value


def part2(lines: list[str]) -> int:
    """ """
    ...


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
