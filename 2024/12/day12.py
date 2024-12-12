"""
Advent of code 2024
Day 12: Garden Groups
"""

from collections import defaultdict, deque
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list
from grid import Grid


def part1(grid: Grid) -> int:
    rows = grid.height()
    cols = grid.width()

    def bfs(x, y, plant_type):
        area = 0
        perimeter = 0
        queue = deque([(x, y)])
        visited.add((x, y))

        while queue:
            cx, cy = queue.popleft()
            area += 1

            for nx, ny in grid.neighbors(cx, cy, diagonals=False):
                if grid[nx, ny] == plant_type and (nx, ny) not in visited:
                    queue.append((nx, ny))
                    visited.add((nx, ny))
                elif grid[nx, ny] != plant_type:
                    perimeter += 1

        return area, perimeter

    visited = set()
    total_price = 0

    for i in range(rows):
        for j in range(cols):
            if (i, j) not in visited:
                area, perimeter = bfs(i, j, grid[i, j])
                total_price += area * perimeter

    return total_price


def part2(grid: Grid) -> int:
    rows = grid.height()
    cols = grid.width()

    def bfs(x, y, plant_type):
        area = 0
        boundary_edges = set()
        visited_region = set()
        queue = deque([(x, y)])
        visited_region.add((x, y))

        while queue:
            cx, cy = queue.popleft()
            area += 1

            for nx, ny in grid.neighbors(cx, cy, diagonals=False, valid_only=False):
                edge = ((cx, cy), (nx, ny))
                if grid.is_valid(nx, ny) and grid[nx, ny] == plant_type:
                    if (nx, ny) not in visited_region:
                        queue.append((nx, ny))
                        visited_region.add((nx, ny))
                else:
                    boundary_edges.add(edge)

        return area, visited_region, boundary_edges

    def combine_edges(edges):
        """
        Combine edges that are adjacent to each other.
        """
        unique_edges = defaultdict(set)
        result = set()
        for edge in edges:
            a, b1, b2 = edge
            for i in range(b1, b2+1):
                unique_edges[a].add(i)
        # Combine adjacent edges
        for edge in unique_edges:
            b1, b2 = min(unique_edges[edge]), max(unique_edges[edge])
            # check for breaks in the boundary and add them to the result
            for i in range(b1, b2+1):
                if i not in unique_edges[edge]:
                    result.add((edge, b1, i-1))
                    b1 = i
            result.add((edge, b1, b2))
        return result

    def optimize_edges(boundary_edges):
        """
        Reduce boundary edges by identifying unique external edges.
        """
        horizontal_edges = set()
        vertical_edges = set()

        for edge in boundary_edges:
            (x1, y1), (x2, y2) = edge

            if (x2, y2) < (x1, y1):
                edge = ((x2, y2), (x1, y1))  # Normalize edge
                (x1, y1), (x2, y2) = edge
            if x1 == x2:
                vertical_edges.add((x1, y1, y2))  # Vertical edge
                vertical_edges = combine_edges(vertical_edges)
            else:
                horizontal_edges.add((y1, x1, x2))  # Horizontal edge
                horizontal_edges = combine_edges(horizontal_edges)

        unique_edges = vertical_edges.union(horizontal_edges)

        # Total sides are the count of unique external edges
        return len(unique_edges)

    visited = set()
    total_price = 0

    for i in range(rows):
        for j in range(cols):
            if (i, j) not in visited:
                plant_type = grid[i, j]
                area, region_visited, boundary_edges = bfs(i, j, plant_type)
                visited.update(region_visited)
                sides = optimize_edges(boundary_edges)
                print(
                    f"Region with plant type '{plant_type}' - Area: {area}, Sides: {sides}"
                )
                total_price += area * sides

    return total_price


def main():
    loader = LoaderLib(2024)
    testing = True
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
            grid,
        ),
    )


if __name__ == "__main__":
    main()
    # --
    # -
