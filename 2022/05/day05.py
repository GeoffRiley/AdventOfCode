"""
Advent of code 2022
Day 05: Supply Stacks
"""
from typing import List

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list, extract_ints


def make_crate_list(crates: str) -> List[str]:
    """
    Receiving a block of text like:
            [D]
        [N] [C]
        [Z] [M] [P]
         1   2   3
    we need to create a list in the form
        [
            'ZN',
            'MCD',
            'P'
        ]

    :param crates:
    :return:
    """
    crate_lines = crates.splitlines()
    crate_transposed = [''.join(reversed(zipped))[1:].strip() for zipped in zip(*crate_lines) if
                        len(zipped) > 0 and zipped[-1].isdigit()]
    return crate_transposed


def part1(crate_list: List[str], move_lines: List[str]) -> str:
    """
    Receiving input in the form:
    [
        'ZN',
        'MCD',
        'P'
    ]
    and
    [
        move 1 from 2 to 1
        move 3 from 1 to 3
        move 2 from 2 to 1
        move 1 from 1 to 2
    ]
    we must perform the moves of 'n' crates from stack 'x' to stack 'y'
    — One Crate At A Time —
    Finally return the tops of each stack
    """
    for line in move_lines:
        n, x, y = extract_ints(line)
        moved = crate_list[x - 1][-n:][::-1]
        crate_list[x - 1] = crate_list[x - 1][:-n]
        crate_list[y - 1] += moved

    return ''.join(s[-1] for s in crate_list)


def part2(crate_list: List[str], move_lines: List[str]) -> str:
    """
    Receiving input in the form:
    [
        'ZN',
        'MCD',
        'P'
    ]
    and
    [
        move 1 from 2 to 1
        move 3 from 1 to 3
        move 2 from 2 to 1
        move 1 from 1 to 2
    ]
    we must perform the moves of 'n' crates from stack 'x' to stack 'y'
    — Multiple Crates At A Time —
    Finally return the tops of each stack
    """
    for line in move_lines:
        n, x, y = extract_ints(line)
        moved = crate_list[x - 1][-n:]
        crate_list[x - 1] = crate_list[x - 1][:-n]
        crate_list[y - 1] += moved

    return ''.join(s[-1] for s in crate_list)


def main():
    loader = LoaderLib(2022)
    input_text = loader.get_aoc_input(5)

    # input_text = dedent('''\
    #         [D]     *
    #     [N] [C]     *
    #     [Z] [M] [P] *
    #      1   2   3  *
    #
    #     move 1 from 2 to 1
    #     move 3 from 1 to 3
    #     move 2 from 2 to 1
    #     move 1 from 1 to 2
    # ''').strip('\n').strip('*')

    crates, moves = input_text.split('\n\n')
    crate_list1 = make_crate_list(crates)
    crate_list2 = crate_list1.copy()  # Duplicate the start position for the second pass
    move_lines = lines_to_list(moves)

    loader.print_solution('setup', f'{len(crates)}, {len(move_lines)} ...')
    loader.print_solution(1, part1(crate_list1, move_lines))
    loader.print_solution(2, part2(crate_list2, move_lines))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.003202        |        0.003202 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 323, 502 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.009815        |        0.013017 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : TBVFVDZPN
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.007443        |        0.020459 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : VLCWHTDSZ
    # --------------------------------------------------------------------------------
