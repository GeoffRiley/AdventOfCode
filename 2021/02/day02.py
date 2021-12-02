"""
Advent of code 2021
Day 2: Dive!
"""
from typing import List, Tuple

from aoc.geometry import Point
from aoc.loader import LoaderLib
from aoc.utility import lines_to_list

# This dictionary defines the displacement of our 'submarine' for
# each of the three directional instructions.
# Note that 'x' is the horizontal motion and 'y' is the depth, with
# depth increasing downwards.
VECTORS = {
    'forward': Point(1, 0),
    'up': Point(0, -1),
    'down': Point(0, 1),
}


def part1(instructions: List[Tuple[str, int]]):
    """Interpret instructions literally for the initial run.
        "forward" means move forward one unit
        "up" means surface one unit shallower
        "down" means dive one unit deeper
        each of these directions get a magnification factor applied.
    """
    position = Point()
    for inst, mag in instructions:
        position += VECTORS[inst] * mag
    return position.x * position.y


def part2(instructions: List[Tuple[str, int]]):
    """Handbook found: instructions mean something a little different.
        "forward" means move ahead and up/down according to the subs aim
        "up" means change the aim towards the surface
        "down" means change the aim towards the floor
        again, the directions are modified by the magnification factor.
    """
    position = Point()
    aim = 0
    for inst, mag in instructions:
        x, y = VECTORS[inst]
        if y == 0:
            position += Point(x, aim) * mag
        else:
            aim += y * mag
    return position.x * position.y


def main():
    loader = LoaderLib(2021)
    input_text = loader.get_aoc_input(2)
    lines = [line.split() for line in lines_to_list(input_text)]
    instructions = [(direction, int(magnitude)) for direction, magnitude in lines]
    # Make sure we translated all the lines
    assert (len(lines) == len(instructions))
    loader.print_solution('setup', f'{len(instructions)} lines of instruction decoded')
    loader.print_solution(1, part1(instructions))
    loader.print_solution(2, part2(instructions))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.005539        |        0.005539 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 1000 lines of instruction decoded
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.003697        |        0.009235 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 2117664
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.003168        |        0.012403 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 2073416724
    # --------------------------------------------------------------------------------
