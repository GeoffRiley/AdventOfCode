"""
Advent of code 2022
Day 10: Cathode-Ray Tube
"""
from functools import lru_cache
from pathlib import Path
from typing import List, Tuple

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


@lru_cache(maxsize=0)
def decode_instruction(line: str) -> Tuple[int, int]:
    inst = line.split()
    if inst[0] == 'noop':
        delta_clk = 1
        delta_x = 0
    elif inst[0] == 'addx':
        delta_clk = 2
        delta_x = int(inst[1])
    else:
        raise SyntaxError(f'Unrecognised instruction: {inst[0]}')
    return delta_clk, delta_x


def part1(lines: List[str]) -> int:
    """
    We're a processor once more!
    Instructions:
        noop:
            1 clock cycle
            no effect
        addx:
            3 clock cycles
            increments X by parameter
    """
    ip = 0
    regs = {'x': 1}
    clk = 0
    signal_strength = 0
    while ip < len(lines) and clk < 220:
        delta_clk, delta_x = decode_instruction(lines[ip])
        while delta_clk > 0:
            clk += 1
            delta_clk -= 1
            if (clk - 20) % 40 == 0:
                strength = clk * regs['x']
                print(f'strength @{clk} = {strength}')
                signal_strength += strength
            if delta_clk == 0:
                regs['x'] += delta_x
        ip += 1

    return signal_strength


def part2(lines: List[str]) -> str:
    """
    Build a CRT display simulation
    """
    ip = 0
    regs = {'x': 1}
    clk = 0
    display = ['' for _ in range(6)]
    crt_x = 0
    crt_y = 0
    while ip < len(lines):
        delta_clk, delta_x = decode_instruction(lines[ip])
        while delta_clk > 0:
            clk += 1
            delta_clk -= 1
            if crt_x in range(regs['x'] - 1, regs['x'] + 2):
                display[crt_y] += '#'
            else:
                display[crt_y] += ' '
            if delta_clk == 0:
                regs['x'] += delta_x
            crt_x += 1
            if crt_x > 39:
                crt_y += 1
                crt_x = 0
        ip += 1

    return '\n' + '\n'.join(display)


def main():
    loader = LoaderLib(2022)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(10)
    else:
        input_text = (Path.cwd() / 'testdata.txt').read_text().strip('\n')

    lines = lines_to_list(input_text)

    loader.print_solution('setup', f'{len(lines)} ...')
    loader.print_solution(1, part1(lines))
    loader.print_solution(2, part2(lines))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.003136        |        0.003136 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 138 ...
    # --------------------------------------------------------------------------------
    #
    # strength @20 = 560
    # strength @60 = 1260
    # strength @100 = 2100
    # strength @140 = 2380
    # strength @180 = 3780
    # strength @220 = 4840
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.001432        |        0.004568 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 14920
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.001492        |        0.006059 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   :
    # ###  #  #  ##   ##   ##  ###  #  # ####
    # #  # #  # #  # #  # #  # #  # #  #    #
    # ###  #  # #    #  # #    ###  #  #   #
    # #  # #  # #    #### #    #  # #  #  #
    # #  # #  # #  # #  # #  # #  # #  # #
    # ###   ##   ##  #  #  ##  ###   ##  ####
    # --------------------------------------------------------------------------------
