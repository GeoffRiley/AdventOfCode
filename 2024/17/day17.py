"""
Advent of code 2024
Day 17: Chronospatial Computer
"""

from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list, to_list_int


def run_program(program, A_init, B_init, C_init):
    # Registers
    A = A_init
    B = B_init
    C = C_init

    # Instruction pointer
    ip = 0

    outputs = []

    def get_combo_value(operand):
        if operand <= 3:
            return operand
        elif operand == 4:
            return A
        elif operand == 5:
            return B
        elif operand == 6:
            return C
        # operand == 7 not expected

    # Run until we go past the program
    while ip < len(program):
        opcode = program[ip]
        if ip + 1 >= len(program):
            # No operand available, halt
            break
        operand = program[ip + 1]

        # Execute instruction
        if opcode == 0:  # adv
            # A = floor(A / (2^combo))
            denom = get_combo_value(operand)
            # denom is the exponent source: we do 2^(denom)
            # If denom is large, make sure to handle large power
            A = A // (2**denom)
            ip += 2

        elif opcode == 1:  # bxl
            # B = B XOR literal operand
            B = B ^ operand
            ip += 2

        elif opcode == 2:  # bst
            # B = (combo operand) % 8
            val = get_combo_value(operand) % 8
            B = val
            ip += 2

        elif opcode == 3:  # jnz
            # If A != 0, jump to operand literal
            if A != 0:
                ip = operand
            else:
                ip += 2

        elif opcode == 4:  # bxc
            # B = B XOR C (operand ignored)
            B = B ^ C
            ip += 2

        elif opcode == 5:  # out
            # output (combo operand) % 8
            val = get_combo_value(operand) % 8
            outputs.append(val)
            ip += 2

        elif opcode == 6:  # bdv
            # B = floor(A / (2^combo))
            denom = get_combo_value(operand)
            B = A // (2**denom)
            ip += 2

        elif opcode == 7:  # cdv
            # C = floor(A / (2^combo))
            denom = get_combo_value(operand)
            C = A // (2**denom)
            ip += 2

        else:
            # Invalid opcode, halt
            break

    return outputs


def part1(lines: list[str]) -> int:
    """ """
    program = to_list_int(lines[1][0].lstrip("Program: "))
    A_init, B_init, C_init = map(int, [l.split()[-1] for l in lines[0]])
    outputs = run_program(program, A_init, B_init, C_init)
    return ",".join(str(i) for i in outputs)


def part2(lines: list[str]) -> int:
    """ """
    program = to_list_int(lines[1][0].lstrip("Program: "))
    A_init, B_init, C_init = map(int, [l.split()[-1] for l in lines[0]])

    def run_part2(regA, posn):
        if posn == len(program):
            return regA
        for i in range(8):
            output = run_program(program, regA * 8 + i, 0, 0)
            if len(output) and output[0] == program[-(posn + 1)]:
                ret_val = run_part2((regA * 8 + i), posn + 1)
                if ret_val:
                    return ret_val

    return run_part2(0, 0)


def main():
    loader = LoaderLib(2024)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(17)
    else:
        input_text = dedent(
            """\
                Register A: 729
                Register B: 0
                Register C: 0

                Program: 0,1,5,4,3,0
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
    #
    # --------------------------------------------------------------------------------
    # LAP -> 0.000675        |        0.000675 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : len(lines)=2 ...
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.000101        |        0.000776 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 6,5,7,4,5,7,3,1,0
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.001086        |        0.001862 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 2   : 105875099912602
    # --------------------------------------------------------------------------------
