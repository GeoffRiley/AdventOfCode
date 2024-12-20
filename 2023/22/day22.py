"""
Advent of code 2023
Day 22: Sand Slabs
"""

import copy
import queue
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list
from geometry import Point3


class Brick:
    """
    A class representing a 3D brick with spatial positioning and support
    relationships.

    The Brick class models a three-dimensional brick with specific coordinates
    and methods to analyze its spatial relationships with other bricks. It
    tracks vertical positioning, overlaps, and support connections.

    Attributes:
        id: A unique identifier for the brick.
        pos1: First coordinate point of the brick.
        pos2: Second coordinate point of the brick.
        bricks_above: Set of bricks positioned above this brick.
        bricks_below: Set of bricks positioned below this brick.
    """

    def __init__(self, id, pos1, pos2):
        self.pos1 = pos1
        self.pos2 = pos2
        self.id = id
        self.bricks_above = set()
        self.bricks_below = set()
        self._supporting = None
        self._supported_by = None

    def on_ground(self):
        return self.lowest_point() == 1

    def highest_point(self):
        return max(self.pos1.z, self.pos2.z)

    def lowest_point(self):
        return min(self.pos1.z, self.pos2.z)

    def ranges_overlap(self, r1, r2):
        return r1[1] >= r2[0] and r1[0] <= r2[1]

    def overlaps(self, other):
        x1, y1, z1 = self.pos1
        x2, y2, z2 = self.pos2
        x_range1 = (min(x1, x2), max(x1, x2))
        y_range1 = (min(y1, y2), max(y1, y2))
        z_range1 = (min(z1, z2), max(z1, z2))

        x3, y3, z3 = other.pos1
        x4, y4, z4 = other.pos2
        x_range2 = (min(x3, x4), max(x3, x4))
        y_range2 = (min(y3, y4), max(y3, y4))
        z_range2 = (min(z3, z4), max(z3, z4))

        # Check for overlap in x, y, and z
        overlap_x = self.ranges_overlap(x_range1, x_range2)
        overlap_y = self.ranges_overlap(y_range1, y_range2)
        overlap_z = self.ranges_overlap(z_range1, z_range2)

        return (overlap_x, overlap_y, overlap_z)

    def is_level_below(self, other):
        return self.highest_point() == other.lowest_point() - 1

    def supported_by(self):
        if self._supported_by is None:
            self._supported_by = [
                b for b in self.bricks_below if b.is_level_below(self)
            ]

        return self._supported_by

    def supporting(self):
        if self._supporting is None:
            self._supporting = [b for b in self.bricks_above if self.is_level_below(b)]

        return self._supporting

    def is_under(self, other):
        x_overlap, y_overlap, _ = self.overlaps(other)
        return x_overlap and y_overlap

    def drop(self, amount=1):
        self.pos1 = Point3(self.pos1.x, self.pos1.y, self.pos1.z - amount)
        self.pos2 = Point3(self.pos2.x, self.pos2.y, self.pos2.z - amount)

    def __repr__(self):
        return f"Brick {self.id}: {self.pos1}, {self.pos2}"


def parse_bricks(lines) -> dict:
    """Parses input lines into a list of Brick objects.

    Converts raw coordinate strings into Brick instances with unique
    identifiers. Each line represents a brick's start and end coordinates,
    which are transformed into Point3 objects.

    Args:
        lines: A list of coordinate strings in the format "x1,y1,z1~x2,y2,z2".

    Returns:
        A list of Brick objects representing the parsed bricks.
    """
    bricks = []
    for i, line in enumerate(lines):
        coords = line.split("~")
        start = Point3(*tuple(map(int, coords[0].split(","))))
        end = Point3(*tuple(map(int, coords[1].split(","))))
        brick_id = i
        bricks.append(Brick(brick_id, start, end))

    return bricks


def settle_bricks(in_bricks) -> dict:
    """
    Once we have all bricks and their cubes, let them fall to their final positions.
    This only needs to be done once.
    """
    bricks = copy.deepcopy(in_bricks)
    bricks.sort(key=lambda b: b.lowest_point())

    for falling in bricks:
        if falling.on_ground():
            continue

        highest_point = 1  # highest z for bricks below

        lower_bricks = [
            lower for lower in bricks if lower.lowest_point() < falling.lowest_point()
        ]

        if not lower_bricks:
            continue

        for lower in lower_bricks:
            if lower.is_under(falling):
                falling.bricks_below.add(lower)
                lower.bricks_above.add(falling)
                highest_point = max(highest_point, lower.highest_point() + 1)

        if falling.lowest_point() > highest_point:
            falling.drop(falling.lowest_point() - highest_point)

    bricks.sort(key=lambda b: b.lowest_point())
    return bricks


def disintegrate(removed_brick):
    """Determines if removing a brick would cause other bricks to fall.

    Checks whether disintegrating the given brick would cause any supported
    bricks to collapse. Returns 0 if the removal would cause a collapse,
    otherwise returns 1.

    Args:
        removed_brick: The Brick object to be potentially disintegrated.

    Returns:
        An integer (0 or 1) indicating whether the brick can be safely removed.
    """

    return next(
        (0 for above in removed_brick.supporting() if len(above.supported_by()) == 1),
        1,
    )


def disintegrate_chain_reaction(removed_brick):
    """Calculates the number of bricks that would fall in a chain reaction
    when a specific brick is removed.

    Simulates the cascading collapse of bricks when a given brick is
    disintegrated, tracking which bricks would fall as a result. Uses a
    breadth-first approach to determine the total number of bricks affected by
    the initial removal.

    Args:
        removed_brick: The Brick object to be initially disintegrated.

    Returns:
        An integer representing the total number of bricks that would fall in
        the chain reaction.
    """

    def can_disintegrate(count, brick):
        return count == len(brick.supported_by())

    q = queue.SimpleQueue()
    q.put(removed_brick)
    disintegrated = {removed_brick.id: True}

    while not q.empty():
        brick = q.get()
        for above in brick.supporting():
            if above.id in disintegrated:
                continue

            supports_disintegrated_count = sum(
                a.id in disintegrated for a in above.supported_by()
            )

            if can_disintegrate(supports_disintegrated_count, above):
                disintegrated[above.id] = True

            q.put(above)

    return len(disintegrated) - 1


def part1(lines: list[str]) -> int:
    """
    Processes a list of lines representing bricks and calculates how many
    bricks can be safely disintegrated.
    This function evaluates the stability of the brick structure and counts
    the number of bricks that can be removed without causing instability.

    Args:
        lines (list[str]): A list of strings where each string represents a
        brick's properties.

    Returns:
        int: The number of bricks that can be safely disintegrated from the
        structure.
    """
    bricks = parse_bricks(lines)
    resting = settle_bricks(bricks)

    return sum(disintegrate(b) for b in resting)


def part2(lines: list[str]) -> int:
    """ """
    bricks = parse_bricks(lines)
    resting = settle_bricks(bricks)

    return sum(disintegrate_chain_reaction(b) for b in resting)


def main():
    loader = LoaderLib(2023)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(22)
    else:
        input_text = dedent(
            """\
                1,0,1~1,2,1
                0,0,2~2,0,2
                0,2,3~2,2,3
                0,0,4~0,2,4
                2,0,5~2,2,5
                0,1,6~2,1,6
                1,1,8~1,1,9
            """
        ).strip("\n")
    # lines = [
    #     (extract_ints(param)) for param in [line for line in lines_to_list(input_text)]
    # ]
    # lines = [lines_to_list(line) for line in input_text.split("\n\n")]
    lines = lines_to_list(input_text)

    loader.print_solution("setup", f"{len(lines)=} ...")
    loader.print_solution(
        1,
        part1(
            lines,
        ),
    )

    # if testing:
    #     input_text = dedent(
    #         """\
    #         """
    #     ).strip("\n")
    #     lines = lines_to_list(input_text)

    loader.print_solution(
        2,
        part2(
            lines,
        ),
    )


if __name__ == "__main__":
    main()
    # --
    # --------------------------------------------------------------------------------
    # LAP -> 0.000865        |        0.000865 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : len(lines)=1232 ...
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 1.509685        |        1.510551 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 430
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 2.286462        |        3.797013 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 2   : 60558
    # --------------------------------------------------------------------------------
