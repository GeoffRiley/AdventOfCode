"""
Advent of code 2021
Day 18: Snailfish
"""
from copy import deepcopy
from dataclasses import dataclass
from itertools import permutations
from typing import List, Union

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


class DoneExplode(Exception):
    pass


@dataclass
class FishFry:
    value: int
    depth: int

    def __add__(self, other):
        return FishFry(self.value + other.value, self.depth - 1)


def parse_fish(line: str) -> List[FishFry]:
    fry = []
    depth = 0
    for c in line:
        if c == '[':
            depth += 1
        elif c == ']':
            depth -= 1
        elif c.isnumeric():
            fry.append(FishFry(int(c), depth))
    return fry


class SnailFish:
    def __init__(self, line: Union[str, List[FishFry]]):
        fry = parse_fish(line) if isinstance(line, str) else deepcopy(line)
        while True:
            try:
                for idx, node in enumerate(fry):
                    if node.depth >= 5:
                        if idx > 0:
                            fry[idx - 1].value += node.value
                        if idx < len(fry) - 2:
                            fry[idx + 2].value += fry[idx + 1].value
                        fry[idx] = FishFry(0, fry.pop(idx).depth - 1)
                        raise DoneExplode
                for idx, node in enumerate(fry):
                    if node.value >= 10:
                        x = node.value // 2
                        y = node.value - x
                        fry[idx] = FishFry(y, fry[idx].depth + 1)
                        fry.insert(idx, FishFry(x, node.depth + 1))
                        raise DoneExplode
            except DoneExplode:
                pass
            else:
                break
        self.fry = fry

    def __add__(self, other):
        if isinstance(other, str):
            other = SnailFish(other)
        elif isinstance(other, int) and other == 0:
            return self
        s = deepcopy(self.fry + other.fry)
        for node in s:
            node.depth += 1
        return SnailFish(s)

    def __radd__(self, other):
        return self + other

    def magnitude(self):
        s = deepcopy(self.fry)
        done = False
        while not done:
            for i in range(len(s) - 1):
                if s[i].depth == s[i + 1].depth:
                    s[i] = FishFry(3 * s.pop(i).value + 2 * s[i].value, s[i].depth - 1)
                    break
            else:
                done = True
        return s[0].value


def part1(fish_numbers):
    """
    """
    return sum(fish_numbers).magnitude()
    # 3524


def part2(fish_numbers):
    """
    """
    magnitudes = set()
    for x, y in permutations(fish_numbers, 2):
        magnitudes.add((x + y).magnitude())
    return max(magnitudes)
    # 4656


def main():
    loader = LoaderLib(2021)
    input_text = loader.get_aoc_input(18)

    #     input_text = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
    # [[[5,[2,8]],4],[5,[[9,9],0]]]
    # [6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
    # [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
    # [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
    # [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
    # [[[[5,4],[7,7]],8],[[8,3],8]]
    # [[9,3],[[9,9],[6,[4,9]]]]
    # [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
    # [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""

    lines = lines_to_list(input_text)
    fish_numbers = []
    for line in lines:
        fish_numbers.append(SnailFish(line))

    loader.print_solution('setup', f'{len(fish_numbers)} fishy looking numbers')
    loader.print_solution(1, part1(fish_numbers))
    loader.print_solution(2, part2(fish_numbers))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.009586        |        0.009586 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 100 fishy looking numbers
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.299356        |        0.308942 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 3524
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 16.239285       |       16.548227 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 4656
    # --------------------------------------------------------------------------------
