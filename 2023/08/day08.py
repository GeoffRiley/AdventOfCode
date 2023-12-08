"""
Advent of code 2023
Day 08: Haunted Wasteland
"""
from itertools import cycle
import math
from textwrap import dedent
from typing import Iterable

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


class Junction:
    """
    A junction is a node in the junction tree.  It has a name and two
    children, left and right.  The name is a string of the form 'ABC' or
    'XYZ'.
    """

    def __init__(self, name, left=None, right=None):
        self.name = name
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Junction({self.name}, {self.left}, {self.right})"


class JunctionTree:
    """
    A junction tree is a tree of junctions.  It has a root and a dictionary
    of junctions.  The junctions are named by a string of the form 'ABC' or
    'XYZ'.  The root is the name of the junction that is the root of the tree.
    The dictionary is a mapping of junction names to junctions.
    """

    def __init__(self):
        self.root = None
        self.junctions = {}

    def add_junction(self, name, left, right):
        if name not in self.junctions:
            self.junctions[name] = Junction(name, left, right)
        else:
            self.junctions[name].left = left
            self.junctions[name].right = right

    def add_root(self, name):
        self.root = name

    def __repr__(self):
        return f"JunctionTree({self.root}, {self.junctions})"

    def __len__(self):
        return len(self.junctions)


def parse_line(line) -> tuple:
    """
    The line is a string of the form:
    AAA = (BBB, CCC)
    """
    name, rest = line.split(" = ")
    left, right = rest.strip("()").split(", ")
    return name, left, right


def build_tree(lines) -> JunctionTree:
    tree = JunctionTree()
    tree.add_root("AAA")
    for line in lines:
        name, left, right = parse_line(line)
        tree.add_junction(name, left, right)
    return tree


def steps_to_Z(
    route_feed: Iterable, tree: JunctionTree, start: str, triple_zed_end: bool = True
) -> int:
    steps = 0
    current = start
    while True:
        steps += 1
        next_step = next(route_feed)
        if next_step == "L":
            current = tree.junctions[current].left
        elif next_step == "R":
            current = tree.junctions[current].right
        if (triple_zed_end and current == "ZZZ") or (
            not triple_zed_end and current.endswith("Z")
        ):
            return steps


def part1(route, tree) -> int:
    """
    The route is a string of 'L' and 'R' characters.  The tree is a junction
    tree.  The solution is the number of steps to reach the junction 'ZZZ'
    starting from the root of the tree and following the route.
    """
    route_feed = cycle(route)

    return steps_to_Z(route_feed, tree, tree.root)


def part2(route, tree) -> int:
    """
    It is observed that the route is a cycle, every route from '??A' to '??Z'
    leads to another route starting at '??A'.  The number of steps to reach
    '??Z' is not the same for all routes, but the number of steps are a
    multiple of the same number for all routes.
    The solution, therefore, is to find the number of steps to reach each '??Z'
    and find the least common multiple of all those numbers.
    """
    route_feed = cycle(route)
    # First we gather a list of all the '??A' junctions
    current_places = {name: 0 for name in tree.junctions if name.endswith("A")}
    # Then for each one we find the number of steps to reach '??Z'
    for name in current_places.keys():
        current_places[name] = steps_to_Z(route_feed, tree, name, triple_zed_end=False)

    # Now we find the least common multiple of all the steps
    return math.lcm(*current_places.values())


def main():
    loader = LoaderLib(2023)
    testing = False
    testA = False
    testB = False
    if not testing:
        input_text = loader.get_aoc_input(8)
    else:
        if testA:
            input_text = dedent(
                """\
                RL

                AAA = (BBB, CCC)
                BBB = (DDD, EEE)
                CCC = (ZZZ, GGG)
                DDD = (DDD, DDD)
                EEE = (EEE, EEE)
                GGG = (GGG, GGG)
                ZZZ = (ZZZ, ZZZ)
                """
            ).strip("\n")
        elif testB:
            input_text = dedent(
                """\
                LLR

                AAA = (BBB, BBB)
                BBB = (AAA, ZZZ)
                ZZZ = (ZZZ, ZZZ)
                """
            ).strip("\n")
        else:
            input_text = dedent(
                """\
                LR

                11A = (11B, XXX)
                11B = (XXX, 11Z)
                11Z = (11B, XXX)
                22A = (22B, XXX)
                22B = (22C, 22C)
                22C = (22Z, 22Z)
                22Z = (22B, 22B)
                XXX = (XXX, XXX)
                """
            ).strip("\n")
    route, lines = input_text.split("\n\n")
    tree = build_tree(lines_to_list(lines))

    loader.print_solution("setup", f"{len(route)=}, {len(tree)=} ...")
    if not testing or testA or testB:
        loader.print_solution(
            1,
            part1(
                route,
                tree,
            ),
        )
    loader.print_solution(
        2,
        part2(
            route,
            tree,
        ),
    )


if __name__ == "__main__":
    main()
    # --
    # --------------------------------------------------------------------------------
    #  LAP -> 0.000772        |        0.000772 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : len(route)=283, len(tree)=726 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.001030        |        0.001802 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 12169
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.009506        |        0.011308 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 12030780859469
    # --------------------------------------------------------------------------------
