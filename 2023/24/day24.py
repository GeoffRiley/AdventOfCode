"""
Advent of code 2023
Day 24: Never Tell Me The Odds
"""

from itertools import combinations
from textwrap import dedent
from typing import Literal

import sympy as sp
from aoc.loader import LoaderLib


def zero_determinant(vx1, vy1, px1, py1, px2, py2, delta_x, delta_y) -> bool:
    """
    Determines if two hailstone trajectories are parallel and distinct.

    Checks whether two hailstone paths are parallel and do not intersect, considering special cases
    like stationary hailstones and non-zero velocity vectors.

    Args:
        vx1 (float): X-velocity of the first hailstone.
        vy1 (float): Y-velocity of the first hailstone.
        px1 (float): X-position of the first hailstone.
        py1 (float): Y-position of the first hailstone.
        px2 (float): X-position of the second hailstone.
        py2 (float): Y-position of the second hailstone.
        delta_x (float): Difference in X-positions between hailstones.
        delta_y (float): Difference in Y-positions between hailstones.

    Returns:
        bool: True if hailstones are parallel and distinct, False otherwise.
    """
    if vx1 == 0 and vy1 == 0:
        # Hailstone 1 is stationary
        if px1 != px2 or py1 != py2:
            # Parallel and distinct
            return True
    else:
        # Check if (delta_x, delta_y) is a scalar multiple of (vx1, vy1)
        ratio_x = delta_x / vx1 if vx1 != 0 else None
        ratio_y = delta_y / vy1 if vy1 != 0 else None
        if ratio_x is None or ratio_y is None or abs(ratio_x - ratio_y) >= 1e-9:
            # Lines are parallel and distinct
            return True
    return False


def nonzero_determinant(
    vx1,
    vy1,
    vx2,
    vy2,
    px1,
    py1,
    delta_x,
    delta_y,
    determminant,
    test_area_min,
    test_area_max,
) -> Literal[0] | Literal[1]:
    """
    Determines if two hailstone trajectories intersect within a specified test area.

    Calculates the intersection point of two hailstone paths and checks if it occurs in the future and within the given test area boundaries.

    Args:
        vx1 (float): X-velocity of the first hailstone.
        vy1 (float): Y-velocity of the first hailstone.
        vx2 (float): X-velocity of the second hailstone.
        vy2 (float): Y-velocity of the second hailstone.
        px1 (float): X-position of the first hailstone.
        py1 (float): Y-position of the first hailstone.
        delta_x (float): Difference in X-positions between hailstones.
        delta_y (float): Difference in Y-positions between hailstones.
        determminant (float): Calculated determinant for intersection calculation.
        test_area_min (float): Minimum boundary of the test area.
        test_area_max (float): Maximum boundary of the test area.

    Returns:
        int: 1 if intersection is in the future and within the test area, 0 otherwise.
    """
    t1 = (delta_x * vy2 - delta_y * vx2) / determminant
    t2 = (delta_x * vy1 - delta_y * vx1) / determminant

    if t1 < 0 or t2 < 0:
        # Intersection point is behind the starting point
        return 0

    # Calculate intersection point
    x_intersect = px1 + vx1 * t1
    y_intersect = py1 + vy1 * t1

    # Check if the intersection point is within the test area
    if (
        test_area_min <= x_intersect <= test_area_max
        and test_area_min <= y_intersect <= test_area_max
    ):
        return 1
    return 0


def part1(
    vectors: list[tuple[tuple[int, int, int], tuple[int, int, int]]],
    test_area_min: int,
    test_area_max: int,
) -> int:
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
    intersections = 0
    for (pos1, vel1), (pos2, vel2) in combinations(vectors, 2):
        # Ignore the z-axis
        px1, py1, _ = pos1
        px2, py2, _ = pos2
        vx1, vy1, _ = vel1
        vx2, vy2, _ = vel2

        # Compute the determinant
        determminant = vx1 * vy2 - vx2 * vy1

        # Lines are parallel (could be coincident)
        # Check if they are coincident
        # To do this, check if (P2 - P1) is parallel to V1
        delta_x = px2 - px1
        delta_y = py2 - py1
        if determminant == 0:
            if zero_determinant(
                vx1,
                vy1,
                px1,
                py1,
                px2,
                py2,
                delta_x,
                delta_y,
            ):
                continue
        else:
            intersections += nonzero_determinant(
                vx1,
                vy1,
                vx2,
                vy2,
                px1,
                py1,
                delta_x,
                delta_y,
                determminant,
                test_area_min,
                test_area_max,
            )

    return intersections


def part2(
    vectors: list[tuple[tuple[int, int, int], tuple[int, int, int]]],
    test_area_min: int,
    test_area_max: int,
) -> int:
    """
    Determines the exact initial position and velocity of the rock so that it collides with all hailstones.
    Returns the sum of the X, Y, and Z coordinates of the rock's initial position.

    Args:
        vectors: A list of tuples, each containing position and velocity tuples.
                 Position is (x, y, z) and velocity is (vx, vy, vz).

    Returns:
        The sum x0 + y0 + z0 of the rock's initial position.
    """
    # Here we go, trying sympy to solve the equations
    # Try working with the first three hailstones to start.
    hailstones = vectors[:3]
    unknowns = sp.symbols("x y z dx dy dz t1 t2 t3")
    x, y, z, dx, dy, dz, *time = unknowns

    equations = []  # build system of 9 equations with 9 unknowns
    for t, h in zip(time, hailstones):
        equations.extend(
            (
                sp.Eq(x + t * dx, h[0][0] + t * h[1][0]),
                sp.Eq(y + t * dy, h[0][1] + t * h[1][1]),
                sp.Eq(z + t * dz, h[0][2] + t * h[1][2]),
            )
        )
    solution = sp.solve(equations, unknowns).pop()
    return sum(solution[:3])


def main():
    loader = LoaderLib(2023)
    testing = False
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
    # --------------------------------------------------------------------------------
    # LAP -> 0.001033        |        0.001033 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : len(vectors)=300 ...
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.023334        |        0.024368 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 12783
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.146741        |        0.171109 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 2   : 948485822969419
    # --------------------------------------------------------------------------------
