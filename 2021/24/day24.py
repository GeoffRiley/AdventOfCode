"""
Advent of code 2021
Day 24:
"""
from operator import add, mul, floordiv, mod, eq
from pprint import pprint
from typing import List, Any, Tuple, Iterable

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list

ALU_OPS = {
    'inp': (1, next),
    'add': (2, add),
    'mul': (2, mul),
    'div': (2, floordiv),
    'mod': (2, mod),
    'eql': (2, eq)
}


def run_prog(prog: List[Any], inputs: Iterable, *, trace: bool = False):
    # assert len(inputs) == 14
    # assert inputs.find(' ') == -1

    registers = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
    input_gen = iter(inputs)

    for line in prog:
        oper, *para = line.split()
        op = ALU_OPS[oper]
        if op[0] == 1:
            inp = int(op[1](input_gen))
            registers[para[0]] = inp
            if trace:
                pprint([line, registers, f'received {inp}'])
        else:
            registers[para[0]] = int(op[1](*[registers[p] if p in 'wxyz' else int(p) for p in para]))
            if trace:
                pprint([line, registers])

    return registers


def part1(lines: List[str], values: List[Tuple[int, int, int]]):
    """
    """
    guess_id = [9 for _ in range(14)]
    stack = []
    for n, (op, pop_mod, push_mod) in enumerate(values):
        if op == 1:
            stack.append((n, push_mod))
        else:
            m, p_mod = stack.pop()
            full_mod = abs(p_mod + pop_mod)
            if p_mod > -pop_mod:
                guess_id[m] -= full_mod
            else:
                guess_id[n] -= full_mod

    registers = run_prog(lines, guess_id)
    assert registers['z'] == 0

    return 'Maximum: ' + ''.join(str(d) for d in guess_id)
    # 94992992796199


def part2(lines: List[str], values: List[Tuple[int, int, int]]):
    """
    """
    guess_id = [1 for _ in range(14)]
    stack = []
    for n, (op, pop_mod, push_mod) in enumerate(values):
        if op == 1:
            stack.append((n, push_mod))
        else:
            m, p_mod = stack.pop()
            full_mod = abs(p_mod + pop_mod)
            if p_mod < -pop_mod:
                guess_id[m] += full_mod
            else:
                guess_id[n] += full_mod

    registers = run_prog(lines, guess_id)
    assert registers['z'] == 0

    return 'Minimum: ' + ''.join(str(d) for d in guess_id)
    # 11931881141161


def extract_para(line: str) -> int:
    *_, v = line.split()
    return int(v)


def main():
    loader = LoaderLib(2021)
    input_text = loader.get_aoc_input(24)

    #     input_text = """inp x
    # mul x -1"""

    #     input_text = """inp z
    # inp x
    # mul z 3
    # eql z x"""

    #     input_text = """inp w
    # add z w
    # mod z 2
    # div w 2
    # add y w
    # mod y 2
    # div w 2
    # add x w
    # mod x 2
    # div w 2
    # mod w 2"""

    lines = lines_to_list(input_text)

    # The code is in chunks of 18 lines, so we can split these chunks into individual parts
    code_chunks = [lines[i * 18:(i + 1) * 18] for i in range(len(lines) // 18)]

    # The difference between each chunk is the value appearing on lines 5,6 and 16
    # If the value on line 5 is '1' then the chunk works to 'push' the next value onto the
    # stack held in the z register.
    # If the value on line 5 is '26' then the chunk works to 'pop' the next value off the stack
    # held in the z register.
    # Each 'push' operation uses the modifier on line 16, and each 'pop' operation uses the modifier
    # on line 6.
    # Therefore, extracting those numbers from the whole sequence will give us enough information
    # to evaluate correct solutions for the task.
    key_values = [
        (extract_para(line[5 - 1]), extract_para(line[6 - 1]), extract_para(line[16 - 1]))
        for line in code_chunks
    ]

    # assert len(lines) == len(...)
    loader.print_solution('setup', f'{len(lines)} ...')
    loader.print_solution(1, part1(lines, key_values))
    loader.print_solution(2, part2(lines, key_values))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.004359        |        0.004359 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 252 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.001799        |        0.006158 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : Maximum: 94992992796199
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.001743        |        0.007901 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : Minimum: 11931881141161
    # --------------------------------------------------------------------------------
