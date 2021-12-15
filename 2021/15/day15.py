"""
Advent of code 2021
Day 15: Chiton
"""
from typing import List

from aoc.grid import Grid
from aoc.loader import LoaderLib
from aoc.utility import lines_to_list
from aoc.utility import sequence_to_int


def perform_seek(grid):
    lim_x = grid.width()
    lim_y = grid.height()
    queue = [(0, 0, 0)]
    seen = {(0, 0)}
    best = None
    while queue:
        queue.sort()
        cost, x, y = queue.pop(0)
        if best is None or cost < best:
            for dx, dy in grid.neighbors(x, y, valid_only=True):
                if dx == lim_x - 1 and dy == lim_y - 1:
                    cost += grid[dx, dy]
                    if best is None or cost < best:
                        best = cost
                if (dx, dy) not in seen:
                    seen.add((dx, dy))
                    queue.append((cost + grid[dx, dy], dx, dy))
    return best


def part1(lines: List[List[int]]):
    """
    """
    grid = Grid.from_text(lines)
    best = perform_seek(grid)
    return best
    # 595


def part2(lines: List[List[int]]):
    """
    """
    grid = Grid.from_text(lines)
    lim_x = grid.width()
    lim_y = grid.height()
    for by in range(5):
        for bx in range(5):
            if bx == by == 0:
                continue
            for dy in range(lim_y):
                for dx in range(lim_x):
                    grid[bx * lim_x + dx, by * lim_y + dy] = ((lines[dy][dx] + bx + by - 1) % 9) + 1

    best = perform_seek(grid)
    return best
    # 2914


def main():
    loader = LoaderLib(2021)
    input_text = loader.get_aoc_input(15)

    #     input_text = """1163751742
    # 1381373672
    # 2136511328
    # 3694931569
    # 7463417111
    # 1319128137
    # 1359912421
    # 3125421639
    # 1293138521
    # 2311944581"""

    lines: List[List[int]] = [sequence_to_int(line) for line in lines_to_list(input_text)]

    # assert len(lines) == len(...)
    loader.print_solution('setup', f'{len(lines)} ...')
    loader.print_solution(1, part1(lines))
    loader.print_solution(2, part2(lines))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.005848        |        0.005848 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 100 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.415174        |        0.421022 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 595
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 22.537658       |       22.958680 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 2914
    # --------------------------------------------------------------------------------
