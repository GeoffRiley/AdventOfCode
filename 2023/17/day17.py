"""
Advent of code 2023
Day 17: Clumsy Crucible
"""
from heapq import heappop, heappush
from textwrap import dedent
from typing import Any

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


def complex_to_tuple(c) -> tuple[int, int]:
    return int(c.real), int(c.imag)


def tuple_to_complex(t) -> complex:
    return complex(*t)


def dijkstra(grid, dest) -> Any:
    priority_queue = []
    visited = {}
    start = 0
    startcost = 0
    for startd in [1, 1j, -1, -1j]:
        heappush(
            priority_queue,
            (startcost, complex_to_tuple(start), complex_to_tuple(startd)),
        )
    while priority_queue:
        cost, prev_t, dist_t = heappop(priority_queue)
        prev = tuple_to_complex(prev_t)
        dist = tuple_to_complex(dist_t)
        if (prev, dist) in visited and visited[(prev, dist)] <= cost:
            continue
        if prev == dest:
            return cost
        visited[(prev, dist)] = cost
        for turn in (1j, -1j):
            newd = dist * turn
            newp = prev
            newcost = cost
            for _ in range(3):
                newp += newd
                if newp not in grid:
                    break
                newcost += grid[newp]
                heappush(
                    priority_queue,
                    (newcost, complex_to_tuple(newp), complex_to_tuple(newd)),
                )
    raise ValueError("No solution found")


def ultra_dijkstra(grid, dest) -> Any:
    priority_queue = []
    visited = {}
    start = 0
    startcost = 0
    for startd in [1, 1j, -1, -1j]:
        heappush(
            priority_queue,
            (startcost, complex_to_tuple(start), complex_to_tuple(startd)),
        )
    while priority_queue:
        cost, prev_t, dist_t = heappop(priority_queue)
        prev = tuple_to_complex(prev_t)
        dist = tuple_to_complex(dist_t)
        if (prev, dist) in visited and visited[(prev, dist)] <= cost:
            continue
        if prev == dest:
            return cost
        visited[(prev, dist)] = cost
        for turn in (1j, -1j):
            newd = dist * turn
            newp = prev
            newcost = cost
            for i in range(1, 11):
                newp += newd
                if newp not in grid:
                    break
                newcost += grid[newp]
                if i > 3:
                    heappush(
                        priority_queue,
                        (newcost, complex_to_tuple(newp), complex_to_tuple(newd)),
                    )
    raise ValueError("No solution found")


def part1(lines: list[str]) -> int:
    """
    We're in charge of a nice big crucible full of lava, and we need to
    get it from the top left city block to the bottom right city block.
    The crucible losed heat at the rate determined by the number given
    in each block. We can only move forwards, left or right—and we can
    only move a maximum of three city blocks in a straight line before
    we have to turn. We can't move diagonally.

    What is the minimum amount of heat loss that we can achieve?

    Okay, after a lot of fiddling around with fancy classes and stuff,
    I've decided to just go with a simple dictionary of complex numbers
    to heat loss values. I'll use Dijkstra's algorithm to find the
    shortest path through the city, and that should be that. !?!?!?!?!?
    """
    grid = {}
    for y, line in enumerate(lines):
        for x, heat in enumerate(line):
            grid[complex(x, y)] = int(heat)

    return dijkstra(grid, complex(len(lines[0]) - 1, len(lines) - 1))


def part2(lines: list[str]) -> int:
    """ """
    grid = {}
    for y, line in enumerate(lines):
        for x, heat in enumerate(line):
            grid[complex(x, y)] = int(heat)

    return ultra_dijkstra(grid, complex(len(lines[0]) - 1, len(lines) - 1))


def main():
    loader = LoaderLib(2023)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(17)
    else:
        input_text = dedent(
            """\
            2413432311323
            3215453535623
            3255245654254
            3446585845452
            4546657867536
            1438598798454
            4457876987766
            3637877979653
            4654967986887
            4564679986453
            1224686865563
            2546548887735
            4322674655533
            """
        ).strip("\n")
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
    # LAP -> 0.000135        |        0.000135 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : len(lines)=141 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    # LAP -> 0.757551        |        0.757686 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 814
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    # LAP -> 2.149850        |        2.907536 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 2   : 974
    # --------------------------------------------------------------------------------
