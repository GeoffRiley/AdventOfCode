"""
Advent of code 2023
Day 24: Never Tell Me The Odds
"""

from collections import Counter
from itertools import combinations, product
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import (
    extract_ints,
    lines_to_list,
    to_list_int,
    batched,
    grouped,
    lines_to_list_int,
    pairwise,
    sequence_to_int,
    tee,
    to_list,
)
from aoc.binary_feeder import BinaryFeeder
from aoc.geometry import Point, Rectangle, Size
from aoc.edge import Edge
from aoc.grid import Grid
from aoc.maths import (
    factorial,
    fibonacci,
    manhattan_distance,
    sign,
)
from aoc.search import (
    astar,
    bfs,
    dfs,
    binary_contains,
    linear_contains,
    Comparable,
    Node,
    PriorityQueue,
    Queue,
    node_to_path,
    Stack,
)


def part1(vectors: list[str], test_area_min: int, test_area_max: int) -> int:
    """
    Vectors are pairs of tuples (position, velocity)
    where position is in a 3D space and velocity is a 3D vector
    both in the form of (x, y, z). Velocity is given in distamce
    per nanosecond.

    Each vector represents a hailstone, a small object that moves
    in a straight line at a constant velocity. The hailstones are
    all moving in different directions and at different speeds.

    Disregarding the z-axis, the hailstones are moving in a 2D plane.
    The hailstones may cross paths, if they do so at the same time
    and place, they will collide.

    Our task is to find how many hailstone paths cross within the
    test area of (test_area_min, test_area_min) to
    (test_area_,max, test_area_max) units.
    """
    paths_crossed = 0
    for vec1, vec2 in combinations(vectors, 2):
        pos1, vel1 = vec1
        pos2, vel2 = vec2
        # Ignore the z-axis
        px1, py1, _ = pos1
        px2, py2, _ = pos2
        vx1, vy1, _ = vel1
        vx2, vy2, _ = vel2

        # If the hailstones are moving in the same direction
        # they will never cross paths.
        if (vx1, vy1) == (vx2, vy2):
            continue

        # If the hailstones are moving in parallel lines
        # they will never cross paths.
        if (vx1 * vy2) == (vx2 * vy1):
            continue

        # Calculate the point of intersection
        # regardless of time
        # y = m1 * x + b1
        # y = m2 * x + b2
        # m1 * x + b1 = m2 * x + b2
        # m1 * x - m2 * x = b2 - b1
        # x * (m1 - m2) = b2 - b1
        # x = (b2 - b1) / (m1 - m2)

        # Calculate the intersection point
        denominator_x = vx1 - vx2
        denominator_y = vy1 - vy2
        if denominator_x == 0 or denominator_y == 0:
            continue

        x = ((py2 - py1) * (vx1 - vx2) - (px2 - px1) * (vy1 - vy2)) / denominator_x
        y = ((py2 - py1) * (vy1 - vy2) - (px2 - px1) * (vx1 - vx2)) / denominator_y

        # Check if the intersection point is within the test area
        if test_area_min <= x <= test_area_max and test_area_min <= y <= test_area_max:
            paths_crossed += 1

    return paths_crossed


def part2(vectors: list[str], test_area_min: int, test_area_max: int) -> int:
    """ """
    ...


def main():
    loader = LoaderLib(2023)
    testing = True
    if not testing:
        input_text = loader.get_aoc_input(24)
        test_area_min = 200_000_000_000_000
        test_area_max = 400_000_000_000_000
    else:
        input_text = dedent(
            """\
                19, 13, 30 @ -2,  1, -2
                18, 19, 22 @ -1, -1, -2
                20, 25, 34 @ -2, -2, -4
                12, 31, 28 @ -1, -2, -1
                20, 19, 15 @  1, -5, -3
            """
        ).strip("\n")
        test_area_min = 7
        test_area_max = 27

    # input_text format: (x, y, z) position @ (x, y, z) velocity
    pos_vel = [line.split(" @ ") for line in input_text.split("\n")]
    vectors = []
    for pos, vel in pos_vel:
        pos_coords = tuple(map(int, pos.split(", ")))
        vel_coords = tuple(map(int, vel.split(", ")))
        vectors.append((pos_coords, vel_coords))
    # lines = [
    #     (extract_ints(param)) for param in [line for line in lines_to_list(input_text)]
    # ]
    # lines = [lines_to_list(line) for line in input_text.split("\n\n")]
    # lines = lines_to_list(input_text)

    loader.print_solution("setup", f"{len(vectors)=} ...")
    loader.print_solution(
        1,
        part1(vectors, test_area_min, test_area_max),
    )

    # if testing:
    #     input_text = dedent(
    #         """\
    #         """
    #     ).strip("\n")
    #     lines = lines_to_list(input_text)

    loader.print_solution(
        2,
        part2(vectors, test_area_min, test_area_max),
    )


if __name__ == "__main__":
    main()
    # --
    # -
