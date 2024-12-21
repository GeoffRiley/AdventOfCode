"""
Advent of code 2024
Day 20: Race Condition
"""

from textwrap import dedent
from typing import Any, Generator

from aoc.loader import LoaderLib


EMPTY = ord(" ")
WALL = ord("#")

Grid = list[list[int]]
Cord = tuple[int, int]  # x, y
Size = tuple[int, int]  # width, height
DijkstraCosts = dict[Cord, int]
DijkstraNodes = dict[Cord, list[Cord]]


def parse_grid(input_text: str) -> tuple[Grid, Cord, Cord, Size]:
    grid = []
    start = (-1, -1)
    end = (-1, -1)
    for y, line in enumerate(input_text.split("\n")):
        row = []
        for x, c in enumerate(line):
            if c == ".":
                row.append(EMPTY)
            elif c == "#":
                row.append(WALL)
            elif c == "S":
                row.append(EMPTY)
                start = (x, y)
            elif c == "E":
                row.append(EMPTY)
                end = (x, y)
            else:
                raise ValueError(f"Invalid character {c}")
        grid.append(row)
    size = len(grid[0]), len(grid)
    return grid, start, end, size


def dijkstra(
    grid: Grid, start: Cord, /, size: Size = None
) -> tuple[DijkstraNodes, DijkstraCosts]:
    previous: DijkstraNodes = {}
    w, h = size or (len(grid[0]), len(grid))

    work: list[tuple[int, int, int]] = [(0, *start)]
    costs: DijkstraCosts = {start: 0}
    while work:
        prev_cost, cx, cy = work.pop(0)
        prev_node = cx, cy
        for x, y in ((cx + 1, cy), (cx, cy + 1), (cx - 1, cy), (cx, cy - 1)):
            if not 0 <= x < w or not 0 <= y < h:
                continue

            if grid[y][x] == WALL:
                continue

            cost = prev_cost + 1
            node: Cord = (x, y)

            if node not in costs or cost < costs[node]:
                costs[node] = cost
                previous[node] = [prev_node]
                work.append((cost, x, y))
            elif cost == costs[node]:
                previous[node].append(prev_node)

    return previous, costs


def iter_cross(
    n: int,
) -> Generator[tuple[int, Literal[0]] | tuple[int, int], Any, None]:
    """
    Only scan in this pattern (where x is)
    ...o...
    ..oop..
    .ooooo.
    oooCxxx
    .xxxxx.
    ..xxx..
    ...x...
    """

    # y is 0
    for x in range(1, n + 1):
        yield x, 0

    # Other cases:
    for y in range(1, n + 1):
        # when n = 3:
        # y  x
        # 1  [-2, 2]
        # 2  [-1, 1]
        # 3  [0]
        for x in range(y - n, n - y + 1):
            yield x, y


def calc_steps_saved(steps: int, cost_start: int, cost_end: int) -> int:
    """
    Always go from low cost point to high cost point
    """
    if cost_start > cost_end:
        return cost_start - (cost_end + steps)
    else:
        return cost_end - (cost_start + steps)


def solve_ex(
    grid: Grid, costs: DijkstraCosts, /, verbose: bool, threshold: int, time: int
) -> int:
    # print(f"solve for {time=} {threshold=}")
    good = 0

    search_window = set(iter_cross(time))
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == WALL:
                continue

            # Find 2 free space within the search window
            cost_start = costs[x, y]
            for dx, dy in search_window:
                if (cost_exit := costs.get((x + dx, y + dy), None)) is not None:
                    steps = abs(dx) + abs(dy)

                    # Check if we actually make some "good" savings
                    steps_saved = calc_steps_saved(steps, cost_start, cost_exit)
                    if steps_saved >= threshold:
                        good += 1

    return good


def part1(
    grid: Grid, costs: DijkstraCosts, verbose=False, threshold=100, time=2
) -> int:
    """ """
    return solve_ex(grid, costs, verbose=verbose, threshold=threshold, time=time)


def part2(
    grid: Grid, costs: DijkstraCosts, verbose=False, threshold=100, time=20
) -> int:
    """ """
    return solve_ex(grid, costs, verbose=verbose, threshold=threshold, time=20)


def main():
    loader = LoaderLib(2024)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(20)
    else:
        input_text = dedent(
            """\
                ###############
                #...#...#.....#
                #.#.#.#.#.###.#
                #S#...#.#.#...#
                #######.#.#.###
                #######.#.#...#
                #######.#.###.#
                ###..E#...#...#
                ###.#######.###
                #...###...#...#
                #.#####.#.###.#
                #.#...#.#.#...#
                #.#.#.#.#.#.###
                #...#...#...###
                ###############
            """
        ).strip("\n")
    # lines = [
    #     (extract_ints(param)) for param in [line for line in lines_to_list(input_text)]
    # ]
    # lines = [lines_to_list(line) for line in input_text.split("\n\n")]
    # lines = lines_to_list(input_text)
    # grid = Grid.from_text(input_text)

    grid, start, end, size = parse_grid(input_text)
    _, costs = dijkstra(grid, start, size=size)
    assert end in costs, f"Can't reach end {end}"

    loader.print_solution("setup", f"{len(grid[0])=} {len(grid)=} ...")
    loader.print_solution(
        1,
        part1(
            grid,
            costs,
            False,
            100,
            2,
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
            costs,
            False,
            100,
            20,
        ),
    )


if __name__ == "__main__":
    main()
    # --
    # --------------------------------------------------------------------------------
    # LAP -> 0.008396        |        0.008396 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : len(grid[0])=141 len(grid)=141 ...
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.007532        |        0.015928 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 1490
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.502153        |        0.518081 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 2   : 1011325
    # --------------------------------------------------------------------------------
