"""
Advent of code 2024
Day 10  Hoof It
"""

from collections import deque
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list
from grid import Grid


def find_trailheads(grid: Grid):
    trailheads = []
    for i in range(grid.width()):
        trailheads.extend((i, j) for j in range(grid.height()) if grid[i, j] == 0)
    return trailheads


def bfs_count_trails(map: Grid, start: tuple[int, int]):
    # rows, cols = map.height, map.width
    # directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    visited = set()
    queue = deque([(start[0], start[1], 0)])  # (row, col, current_height)
    trail_count = 0

    while queue:
        x, y, current_height = queue.popleft()
        if (x, y) in visited:
            continue
        visited.add((x, y))

        if map[x, y] == 9:
            trail_count += 1
            continue

        for nx, ny in map.neighbors(x, y, valid_only=True):
            if map[nx, ny] == current_height + 1:
                queue.append((nx, ny, current_height + 1))

    return trail_count


def bfs_count_distinct_paths(map: Grid, start: tuple[int, int]):
    # rows, cols = len(map), len(map[0])
    # directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    paths_count = {}
    queue = deque(
        [(start[0], start[1], 0, frozenset())]
    )  # (row, col, current_height, path)

    while queue:
        x, y, current_height, path = queue.popleft()
        path = path | {(x, y)}  # Add the current position to the path

        if map[x, y] == 9:
            paths_count[path] = 1
            continue

        for nx, ny in map.neighbors(x, y, valid_only=True):
            if map[nx, ny] == current_height + 1:
                queue.append((nx, ny, current_height + 1, path))

    return len(paths_count)


def part1(grid: Grid) -> int:
    """ """
    trailheads = find_trailheads(grid)
    return sum(bfs_count_trails(grid, trailhead) for trailhead in trailheads)


def part2(grid: Grid) -> int:
    """ """
    trailheads = find_trailheads(grid)
    return sum(bfs_count_distinct_paths(grid, trailhead) for trailhead in trailheads)


def main():
    loader = LoaderLib(2024)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(10)
    else:
        input_text = dedent(
            """\
                89010123
                78121874
                87430965
                96549874
                45678903
                32019012
                01329801
                10456732
            """
        ).strip("\n")
    # lines = [
    #     (extract_ints(param)) for param in [line for line in lines_to_list(input_text)]
    # ]
    # lines = [lines_to_list(line) for line in input_text.split("\n\n")]
    lines = lines_to_list(input_text)

    grid = Grid().from_text(lines)
    for x in range(grid.width()):
        for y in range(grid.height()):
            grid[x, y] = int(grid[x, y])

    loader.print_solution("setup", f"{len(lines)=} ...")
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
    # --------------------------------------------------------------------------------
    # LAP -> 0.008575        |        0.008575 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : len(lines)=58 ...
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.006137        |        0.014712 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 760
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.010780        |        0.025493 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 2   : 1764
    # --------------------------------------------------------------------------------
