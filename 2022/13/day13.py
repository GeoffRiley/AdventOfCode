"""
Advent of code 2022
Day 13: Distress Signal
"""
import json
from textwrap import dedent
from typing import List

from aoc.loader import LoaderLib
from aoc.utility import batched


class Packet:
    def __init__(self, packet):
        self.value = packet

    def __lt__(self, other):
        a = self.value
        ai, al = isinstance(a, int), isinstance(a, list)
        b = other.value
        bi, bl = isinstance(b, int), isinstance(b, list)

        if ai and bi:
            return a < b

        elif al and bl:
            for x, y in zip(a, b):
                if Packet(x) < Packet(y):
                    return True
                if Packet(y) < Packet(x):
                    return False

            return len(a) < len(b)

        elif ai and bl:
            return Packet([a]) < other

        elif al and bi:
            return self < Packet([b])

    def __repr__(self):
        return str(self.value)


def part1(lines: List[List[Packet]]) -> int:
    """
    """
    in_order = 0
    for n, (a, b) in enumerate(lines, start=1):
        if a < b:
            in_order += n
    return in_order


def part2(lines: List[Packet]) -> int:
    """
    """
    guard1, guard2 = Packet([[2]]), Packet([[6]])
    lines.extend([guard1, guard2])
    s_list = sorted(lines)
    guard1_pos = s_list.index(guard1) + 1
    guard2_pos = s_list.index(guard2) + 1

    return guard1_pos * guard2_pos


def main():
    loader = LoaderLib(2022)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(13)
    else:
        # input_text = (Path.cwd() / 'testdata.txt').read_text().strip('\n')
        input_text = dedent('''\
            [1,1,3,1,1]
            [1,1,5,1,1]
            
            [[1],[2,3,4]]
            [[1],4]
            
            [9]
            [[8,7,6]]
            
            [[4,4],4,4]
            [[4,4],4,4,4]
            
            [7,7,7,7]
            [7,7,7]
            
            []
            [3]
            
            [[[]]]
            [[]]
            
            [1,[2,[3,[4,[5,6,7]]]],8,9]
            [1,[2,[3,[4,[5,6,0]]]],8,9]
        ''').strip('\n')

    lines = [Packet(json.loads(line)) for line in input_text.splitlines() if line]
    # pairs = [lines_to_list(group) for group in input_text.split("\n\n")]
    pairs = list(batched(lines, 2))

    loader.print_solution('setup', f'{len(pairs)} {len(lines)} ...')
    loader.print_solution(1, part1(pairs))
    loader.print_solution(2, part2(lines))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.013180        |        0.013180 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 150 300 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.005049        |        0.018229 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 5350
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.088086        |        0.106316 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 19570
    # --------------------------------------------------------------------------------
