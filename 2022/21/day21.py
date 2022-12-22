"""
Advent of code 2022
Day 21: Monkey Math
"""
from functools import lru_cache
from operator import add, sub, mul, floordiv
from pathlib import Path
from typing import List

import sympy as smp

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list

OP_LIST = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': floordiv
}


@lru_cache(maxsize=0)
def find_value(apes, ape) -> int:
    if ape not in apes:
        raise ValueError(f'{ape} not in apes array')
    action = apes[ape]
    if len(action) == 1:
        return int(action[0])
    ape1, op, ape2 = action
    resp1 = find_value(apes, ape1)
    resp2 = find_value(apes, ape2)
    result = OP_LIST[op](resp1, resp2)
    return result


def part1(lines: List[str]) -> int:
    """
    """
    apes = {}
    for line in lines:
        nam, ops = line.split(': ')
        apes[nam] = ops.split()

    return find_value(apes, 'root')


@lru_cache(maxsize=0)
def make_equation(apes, ape) -> str:
    if ape not in apes:
        raise ValueError(f'{ape} not found in apes array')
    # See if the ape involved is me… the unknown value
    if ape == 'humn':
        return 'x'
    action = apes[ape]
    if len(action) == 1:
        return action[0]
    ape1, op, ape2 = action
    resp1 = make_equation(apes, ape1)
    resp2 = make_equation(apes, ape2)
    return f'({resp1} {op} {resp2})'


def part2(lines: List[str]) -> int:
    """
    """
    apes = {}
    for line in lines:
        nam, ops = line.split(': ')
        apes[nam] = ops.split()

    root = apes['root']
    se1 = make_equation(apes, root[0])
    se2 = make_equation(apes, root[2])
    x = smp.symbols('x')
    p_se1 = smp.parse_expr(se1, local_dict={'x': x})
    p_se2 = smp.parse_expr(se2, local_dict={'x': x})

    result = smp.solve(smp.Eq(p_se1, p_se2))

    return result[0]


def main():
    loader = LoaderLib(2022)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(21)
    else:
        input_text = (Path.cwd() / 'testdata.txt').read_text().strip('\n')
        # input_text = dedent('''\
        # ''').strip('\n')

    lines = lines_to_list(input_text)

    loader.print_solution('setup', f'{len(lines)} ...')
    loader.print_solution(1, part1(lines))
    loader.print_solution(2, part2(lines))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.003812        |        0.003812 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 2153 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.009063        |        0.012874 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 82225382988628
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.390306        |        0.403180 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 3429411069028
    # --------------------------------------------------------------------------------
