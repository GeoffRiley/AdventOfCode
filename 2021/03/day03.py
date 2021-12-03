"""
Advent of code 2021
Day 3: Binary Diagnostic
"""
from collections import Counter
from typing import List

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


def count_column(lines: List[str], column: int) -> int:
    c = Counter(line[column] for line in lines)
    return c['1'] - c['0']


def part1(lines: List[str]):
    gamma = ''
    epsilon = ''
    swap = {'1': '0', '0': '1'}
    for bit in range(len(lines[0])):
        c = count_column(lines, bit)
        t = '1' if c > 0 else '0'
        gamma += t
        epsilon += swap[t]

    return int(gamma, 2) * int(epsilon, 2)
    # 2967914


def eliminate_lines(lines, flag_fn):
    sum_vals = {'0': -1, '1': 1}
    bit_count = len(lines[0])
    for i in range(bit_count):
        cnt = sum(sum_vals[line[i]] for line in lines)
        flag_value = flag_fn(cnt)
        lines = list(line for line in lines if line[i] == flag_value)
        if len(lines) == 1:
            break
    return lines[0]


def part2(lines: List[str]):
    oxy_line = eliminate_lines(lines, lambda x: '1' if x >= 0 else '0')
    co2_line = eliminate_lines(lines, lambda x: '0' if x >= 0 else '1')

    oxygen_val = int(oxy_line, 2)
    co2_val = int(co2_line, 2)

    return (oxygen_val * co2_val,
            f'Oxy: {oxy_line} ({oxygen_val}), CO2: {co2_line} ({co2_val})')
    # 7105014 too high Oxy: 011110000110 (1926), CO2: 111001101001 (3689)
    # 7037604 too low  Oxy: 011110000110 (1926), CO2: 111001000110 (3654)
    # 7041258 Just right! Oxy: 011110000111 (1927), CO2: 111001000110 (3654)


def main():
    loader = LoaderLib(2021)
    input_text = loader.get_aoc_input(3)
    # lines = [sequence_to_int(line) for line in lines_to_list(input_text)]
    lines = lines_to_list(input_text)

    loader.print_solution('setup', f'{len(lines)} lines of diagnostic report decoded')
    loader.print_solution(1, part1(lines))
    loader.print_solution(2, part2(lines))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.004385        |        0.004385 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 1000 lines of diagnostic report decoded
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.003856        |        0.008241 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 2967914
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.002676        |        0.010917 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : (7041258, 'Oxy: 011110000111 (1927), CO2: 111001000110 (3654)')
    # --------------------------------------------------------------------------------
