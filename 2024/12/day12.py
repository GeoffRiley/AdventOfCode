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

PERIMETER = object()

def part2(grid: Grid) -> int:
    """
    This is a depth first search solution, but it's not working.

    The idea is to find the area of a plant type and then calculate the perimeter
    area and sides by counting the number of sides that are not the same plant type.

    The area is the number of nodes visited, the perimeter is the number of nodes
    that are not the same plant type and the sides is the number of sides that are
    not the same plant type.

    The total price is the area times the sides and the total perimeter price is
    the area times the perimeter.

    The problem is that the total prices are not coming out as expected.

    I'm going to leave this here for now and come back to it later.
    """
    rows = grid.height()
    cols = grid.width()
    # Going back to one of my favourite indexing methods, complex numbers. :)
    # Create a graph using complex numbers to represent one dimension of the
    # grid as the real part and the other as the imaginary part.
    # This makes it easy to move in all directions as the whole grid is
    # represented as a single one dimensional array.
    graph = {i + j * 1j: grid[i, j] for i in range(rows) for j in range(cols)}

    # Add a surround of "#" to the grid to stop bleed?
    for i in range(-1, rows + 1):
        graph[i - 1 * 1j] = graph[i + cols * 1j] = PERIMETER  # Top and bottom
    for j in range(-1, cols + 1):
        graph[-1 + j * 1j] = graph[rows + j * 1j] = PERIMETER  # Left and right

    # Create a set of visited nodes
    visited = set()

    def dfs(visited, node, plant_type, dir):
        """
        Depth first search to find the region of a plant type.
        """
        if node in visited:
            return 0, 0, 0
        visited.add(node)
        if graph[node] != plant_type:
            if (
                graph[node + dir * 1j] != plant_type
                or graph[node - dir + dir * 1j] != plant_type
            ):
                return 0, 1, 1
            return 0, 1, 0
        area, perimeter, sides = 1, 0, 0
        for d in [1, 1j, -1, -1j]:
            a, p, s = dfs(visited, node + d, plant_type, d)
            area += a
            perimeter += p
            sides += s
        return area, perimeter, sides

    total_price = 0
    total_perimeter_price = 0

    for node in graph:
        if node not in visited and graph[node] != PERIMETER:
            area, perimeter, sides = dfs(visited, node, graph[node], 1)
            print(f"Plant type = {graph[node]} {area=} {perimeter=} {sides=}")
        total_price += area * sides
        total_perimeter_price += area * perimeter
        
    # This really should be the result for both part 1 and 2 here,
    # but there's something going adrift in the calculation.
    return total_perimeter_price, total_price


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
    # lines = lines_to_list(input_text)
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
