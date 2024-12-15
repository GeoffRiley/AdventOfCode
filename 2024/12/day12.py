"""
Advent of code 2024
Day 12: Garden Groups
"""

from collections import deque
from textwrap import dedent
from typing import Any

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list
from grid import Grid


def part1(grid: Grid) -> int:
    """
    This is a graph traversal problem. We can use a breadth-first search to find
    the regions of each plant type. We can then calculate the area and perimeter
    for each region and sum the area * perimeter for each region.

    :param grid: Grid
    :return: int
    """
    rows = grid.height()
    cols = grid.width()

    def bfs(x, y, plant_type) -> tuple[int, int]:
        """
        Breadth-first search to find the regions of each plant type.
        :param x: int representing the x-coordinate
        :param y: int representing the y-coordinate
        :param plant_type: str representing the plant type
        :return: tuple of ints
        """
        area = 0
        perimeter = 0
        queue = deque([(x, y)])
        visited.add((x, y))

        while queue:
            cx, cy = queue.popleft()
            area += 1

            # Check the neighbors of the current cell
            for nx, ny in grid.neighbors(cx, cy, diagonals=False):
                # If the neighbor is the same plant type and not visited, add it to the queue
                # and visited set. If the neighbor is not the same plant type, increment the
                # perimeter.
                if grid[nx, ny] == plant_type and (nx, ny) not in visited:
                    queue.append((nx, ny))
                    visited.add((nx, ny))
                elif grid[nx, ny] != plant_type:
                    perimeter += 1

        # Calculate the perimeter
        return area, perimeter

    visited = set()
    total_price = 0

    # Iterate through the grid and find the regions of each plant type
    # and calculate the area and perimeter.
    for i in range(rows):
        for j in range(cols):
            if (i, j) not in visited:
                area, perimeter = bfs(i, j, grid[i, j])
                total_price += area * perimeter

    return total_price


def part2(lines: str) -> int:
    """
    This is a graph traversal problem. We can use a depth-first search to find
    the regions of each plant type. We can then calculate the area, perimeter,
    and sides of each region and sum the area * sides for each region.

    :param lines: list of strings
    :return: int
    """
    graph = {
        (i) + (j) * 1j: e for i, row in enumerate(lines) for j, e in enumerate(row)
    }
    cardinal_directions, visited = (1, -1, 1j, -1j), set()

    def dfs(
        position, plant_type, region, fence, direction=None
    ) -> None | Any | tuple[int, int, int]:
        """
        Depth-first search to find the regions of each plant type.
        :param position: complex number representing the current position
        :param plant_type: str representing the plant type
        :param region: set of complex numbers representing the region
        :param fence: set of tuples representing the fence
        :param direction: complex number representing the direction
        :return: None or tuple of ints
        """
        # Base cases
        # If the position is in visited and the plant type is the same as the current plant type
        # then return None
        if position in visited and graph.get(position) == plant_type:
            return
        # If the position is in visited and the plant type is not the same as the current plant type
        # then add the position and direction to the fence
        if graph.get(position) != plant_type:
            return fence.add((position, direction))
        # If the position is not in visited then add the position to visited and region
        visited.add(position), region.add(position)
        for direction in cardinal_directions:
            dfs(position + direction, plant_type, region, fence, direction)

        # Calculate the area, perimeter, and sides of the region
        neighbors = {(p + dr * 1j, dr) for p, dr in fence}
        return len(region), len(fence), len(fence - neighbors)

    regions = [dfs(p, e, set(), set()) for p, e in graph.items() if p not in visited]

    # part1 = sum(area * perim for area, perim, _ in regions)
    part2 = sum(area * sides for area, _, sides in regions)

    return part2


def main():
    loader = LoaderLib(2024)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(12)
    else:
        input_text = dedent(
            """\
                RRRRIICCFF
                RRRRIICCCF
                VVRRRCCFFF
                VVRCCCJFFF
                VVVVCJJCFE
                VVIVCCJJEE
                VVIIICJJEE
                MIIIIIJJEE
                MIIISIJEEE
                MMMISSJEEE
            """
        ).strip("\n")
    # lines = [
    #     (extract_ints(param)) for param in [line for line in lines_to_list(input_text)]
    # ]
    # lines = [lines_to_list(line) for line in input_text.split("\n\n")]
    lines = lines_to_list(input_text)
    grid = Grid().from_text(input_text)

    loader.print_solution("setup", f"{grid.width()=} {grid.height()=} ...")
    loader.print_solution(
        1,
        part1(
            grid,
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
    # LAP -> 0.004954        |        0.004954 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : grid.width()=140 grid.height()=140 ...
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.025579        |        0.030533 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 1533024
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.136817        |        0.167350 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 2   : 910066
    # --------------------------------------------------------------------------------
