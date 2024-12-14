"""
Advent of code 2024
Day 14: Restroom Redoubt
"""

from collections import defaultdict
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import extract_ints, lines_to_list
from aoc.geometry import Point, Rectangle


class Robot:
    def __init__(self, position: tuple[int, int], velocity: tuple[int, int]):
        self.position = Point(*position)
        self.velocity = Point(*velocity)

    def move(self):
        self.position = self.position + self.velocity

    def __repr__(self):
        return f"Robot({self.position=}, {self.velocity=})"


def wrap_in_bounds(robot: Robot, bounds: Rectangle):
    if robot.position.x < bounds.left:
        robot.position.x = bounds.right - (bounds.left - robot.position.x)
    if robot.position.x >= bounds.right:
        robot.position.x = bounds.left + (robot.position.x - bounds.right)
    if robot.position.y < bounds.top:
        robot.position.y = bounds.bottom - (bounds.top - robot.position.y)
    if robot.position.y >= bounds.bottom:
        robot.position.y = bounds.top + (robot.position.y - bounds.bottom)


def print_grid(robots: list[Robot], work_area: Rectangle, cycle: int):
    """
    Print the grid with the robots on it
    A dot indicates an empty space, a number indicates the number of robots
    occupying that space
    """
    grid = [[0 for _ in range(work_area.width())] for _ in range(work_area.height())]
    for robot in robots:
        grid[robot.position.y][robot.position.x] += 1

    print(f"Cycle {cycle}:")
    for row in grid:
        print("".join([str(cell) for cell in row]))


def part1(lines: list[str], work_area: Rectangle) -> int:
    """
    Data is line by line a list of robots with their position and velocity
    p=<x,y> v=<x,y>
    Origin is top left, x increases to the right, y increases down

    The robots move in a straight line at a constant velocity, they will never
    collide with each other: multiple robots can occupy the same position at
    the same time. Upon reaching the edge of the grid, a robot wraps around to
    the opposite edge. The robots move simultaneously, one step per second.

    To determine the safest area, count the number of robots in each quadrant
    after 100 seconds. Robots that are exactly in the middle (horizontally or
    vertically) don't count as being in any quadrant.
    """
    # Parse the input
    robots = []
    for line in lines:
        p_x, p_y, v_x, v_y = extract_ints(line, negative=True)
        position = (p_x, p_y)
        velocity = (v_x, v_y)
        robots.append(Robot(position, velocity))

    # Move the robots
    for cycle in range(100):
        for robot in robots:
            robot.move()
            wrap_in_bounds(robot, work_area)
        # print_grid(robots, work_area, cycle)

    # Count the robots in each quadrant
    quadrants = defaultdict(int)
    for robot in robots:
        centre = work_area.center_point()
        if robot.position.x < centre.x:
            if robot.position.y < centre.y:
                quadrants["NW"] += 1
            elif robot.position.y > centre.y:
                quadrants["SW"] += 1
        elif robot.position.x > centre.x:
            if robot.position.y < centre.y:
                quadrants["NE"] += 1
            elif robot.position.y > centre.y:
                quadrants["SE"] += 1

    return quadrants["NW"] * quadrants["NE"] * quadrants["SW"] * quadrants["SE"]


def part2(lines: list[str], work_area: Rectangle) -> int:
    """
    This time we want to know how long it takes for the 'easter egg' to appear
    The easter egg occurs when the robots draw together to form the image
    of a Christmas tree. The easter egg will appear when the robots are
    all standing on independent points in the grid, no two robots are on the
    same point.
    """
    # Parse the input
    robots = []
    for line in lines:
        p_x, p_y, v_x, v_y = extract_ints(line, negative=True)
        position = (p_x, p_y)
        velocity = (v_x, v_y)
        robots.append(Robot(position, velocity))

    # Move the robots
    cycle = 0
    while True:
        # Move the robots, wrap them around, and check if any are on the same
        # position. If they are all on different positions, we have the easter
        # egg and can return the cycle number.
        cycle += 1
        for robot in robots:
            robot.move()
            wrap_in_bounds(robot, work_area)
        positions = [tuple(robot.position) for robot in robots]
        if len(set(positions)) == len(positions):
            return cycle


def main():
    loader = LoaderLib(2024)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(14)
        work_area = Rectangle(0, 0, 101, 103)
    else:
        input_text = dedent(
            """\
                p=0,4 v=3,-3
                p=6,3 v=-1,-3
                p=10,3 v=-1,2
                p=2,0 v=2,-1
                p=0,0 v=1,3
                p=3,0 v=-2,-2
                p=7,6 v=-1,-3
                p=3,0 v=-1,-2
                p=9,3 v=2,3
                p=7,3 v=-1,2
                p=2,4 v=2,-3
                p=9,5 v=-3,-3
            """
        ).strip("\n")
        work_area = Rectangle(0, 0, 11, 7)
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
            work_area,
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
            work_area,
        ),
    )


if __name__ == "__main__":
    main()
    # --
    # --------------------------------------------------------------------------------
    # LAP -> 0.001016        |        0.001016 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : len(lines)=500 ...
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.014509        |        0.015525 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 233709840
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 1.332868        |        1.348393 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 2   : 6620
    # --------------------------------------------------------------------------------
