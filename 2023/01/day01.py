"""
Advent of code 2023
Day 01: Trebuchet?!
"""
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


def part1(lines):
    """
    What is the sum of the calibration values
    """
    digits_only: list[str] = []
    for x in lines:
        y = ''.join(filter(str.isdigit, x))
        z = f'{y[0]}{y[-1]}'
        digits_only.append(z)
        # print(f'Checking: {x}')
        # print(f'    Found: {y}')
        # print(f'    Extracted: {z}')
    return sum(int(s) for s in digits_only)


def part2(lines):
    """
    Sum of the 'proper' calibration values
    """
    digit_list = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9'
    }
    # print('Checking,Conv,Found,Extracted')
    digits_only: list[str] = []
    for x in lines:
        _ = x
        x1 = ''
        while x:
            for wd, dg in digit_list.items():
                if x.startswith(wd):
                    x1 += dg
                    # Allow for overlapping name digits
                    x = x[len(wd) - 1:]
                    break
            else:
                x1 += x[0]
                x = x[1:]
        x = x1
        y = ''.join(filter(str.isdigit, x))
        z = f'{y[0]}{y[-1]}'
        digits_only.append(z)
        # print(f'{_},{x},{y},{z}')
    return sum(int(s) for s in digits_only)


def main():
    loader = LoaderLib(2023)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(1)
    else:
        # input_text = dedent('''\
        #     1abc2
        #     pqr3stu8vwx
        #     a1b2c3d4e5f
        #     treb7uchet
        #     ''').strip('\n')
        input_text = dedent('''\
            two1nine
            eightwothree
            abcone2threexyz
            xtwone3four
            4nineeightseven2
            zoneight234
            7pqrstsixteen
            ''').strip('\n')

    lines = lines_to_list(input_text)

    loader.print_solution('setup', f'{len(lines)} ...')
    loader.print_solution(1, part1(lines))
    loader.print_solution(2, part2(lines))


if __name__ == '__main__':
    main()
    # --
    # --------------------------------------------------------------------------------
    #  LAP -> 0.000303        |        0.000303 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 1000 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.001323        |        0.001625 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 57346
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.021975        |        0.023600 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 57345
    # --------------------------------------------------------------------------------
