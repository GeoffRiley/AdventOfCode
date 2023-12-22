"""
Advent of code 2023
Day 21: Step Counter
"""
from collections import deque
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


def walk(grid, steps, start):
    """
    Slightly modified BFS.
    """
    x, y = start
    v = {(x, y): 0}
    dist = 0
    q = deque()
    q.append((x, y))
    result = []
    while dist < max(steps):
        dist += 1
        q2 = deque()
        while q:
            x, y = q.popleft()
            for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                nx, ny = dx + x, dy + y
                tx, ty = nx % len(grid[0]), ny % len(grid)
                if grid[ty][tx] != "#" and (nx, ny) not in v:
                    v[(nx, ny)] = dist
                    q2.append((nx, ny))
        q = q2
        if dist in steps:
            result.append(len([x for x in v.values() if x % 2 == dist % 2]))
    return result


def part1(grid: list[str], target) -> int:
    """
    'grid' represents a grid of garden plots, '.', and rocks, '#'.
    Each line is a row of the garden.
    'S' is the starting position. We can move left or right, up or down.
    We can only move to a plot that is a garden plot, '.'.
    Our task us to find how many garden plots we can reach in 'target' moves.
    """
    for y, l in enumerate(grid):
        for x, c in enumerate(l):
            if c == "S":
                break
        if c == "S":
            break
    s = walk(grid, (target,), (x, y))[0]
    return s


def part2(grid: list[str]) -> int:
    """
    Now we have an infinite grid: the given grid is the center of the grid,
    and the grid is repeated in all directions.
    """
    for y, l in enumerate(grid):
        for x, c in enumerate(l):
            if c == "S":
                break
        if c == "S":
            break
    SIDE = len(grid)
    HALF = x

    f0, f1, f2 = walk(grid, (HALF, HALF + SIDE, HALF + 2 * SIDE), (x, y))

    c = f0
    a = (f2 - 2 * f1 + f0) // 2
    b = f1 - f0 - a
    # Now we have our polynomial!

    def f(n):
        return a * n**2 + b * n + c

    N = (26501365 - HALF) // SIDE
    return f(N)


def main():
    loader = LoaderLib(2023)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(21)
        target1 = 64
    else:
        input_text = dedent(
            """\
            ...........
            .....###.#.
            .###.##..#.
            ..#.#...#..
            ....#.#....
            .##..S####.
            .##..#...#.
            .......##..
            .##.#.####.
            .##..##.##.
            ...........
            """
        ).strip("\n")
        target1 = 6
    # lines = [
    #     (pat, to_list_int(param))
    #     for pat, param in [line.split()
    #         for line in lines_to_list(input_text)]
    # ]
    # lines = [lines_to_list(line) for line in input_text.split("\n\n")]
    lines = lines_to_list(input_text)

    loader.print_solution("setup", f"{len(lines)=} ...")
    loader.print_solution(
        1,
        part1(
            lines,
            target1,
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
    # LAP -> 0.000144        |        0.000144 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : len(lines)=131 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    # LAP -> 0.004438        |        0.004582 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 3632
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    # LAP -> 0.131945        |        0.136527 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 2   : 600336060511101
    # --------------------------------------------------------------------------------
