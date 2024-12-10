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
        # for dx, dy in directions:
        #     nx, ny = x + dx, y + dy
        #     if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited:
        #         if map[nx][ny] == current_height + 1:
        #             queue.append((nx, ny, current_height + 1))

    return trail_count


def part1(lines: list[str]) -> int:
    """ """
    grid = Grid().from_text(lines)
    for x in range(grid.width()):
        for y in range(grid.height()):
            grid[x, y] = int(grid[x, y])
    trailheads = find_trailheads(grid)
    return sum(bfs_count_trails(grid, trailhead) for trailhead in trailheads)


def part2(lines: list[str]) -> int:
    """ """
    ...


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
    # -
