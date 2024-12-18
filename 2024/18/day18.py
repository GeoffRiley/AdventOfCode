"""
Advent of code 2024
Day 18: RAM Run
"""

from collections import defaultdict
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list, to_list_int
from geometry import Size
from search import astar


def print_grid(grid: defaultdict, size: Size):
    mappy = {0: ".", 1: "#"}
    for y in range(size.cy):
        for x in range(size.cx):
            print(mappy[grid[x + y * 1j]], end="")
        print()


def find_path(start_pos, end_pos, grid, size):
    def is_valid(pos):
        x, y = pos.real, pos.imag
        return 0 <= x < size.cx and 0 <= y < size.cy

    def get_neighbors(pos):
        return [
            nx
            for dx in [(1 + 0j), (-1 + 0j), (0 + 1j), (0 - 1j)]
            if (nx := pos + dx) and is_valid(nx) and grid[nx] == 0
        ]

    def is_end(pos):
        return pos == end_pos

    def heuristic(pos):
        x, y = pos.real, pos.imag
        ex, ey = end_pos.real, end_pos.imag
        return abs(ex - x) + abs(ey - y)

    return astar(start_pos, is_end, get_neighbors, heuristic)


def part1(grid: defaultdict, size: Size) -> int:
    """ """
    start_pos = 0 + 0 * 1j
    end_pos = size.cx - 1 + (size.cy - 1) * 1j
    # print(f"{start_pos=} {end_pos=}")
    # print_grid(grid, size)

    path = find_path(start_pos, end_pos, grid, size)

    p = path
    i = 0
    while p:
        p = p.parent
        i += 1
    return i - 1


def part2(grid: defaultdict, size: Size, more_rocks: list[str]) -> int:
    start_pos = 0 + 0 * 1j
    end_pos = size.cx - 1 + (size.cy - 1) * 1j
    # print(f"{start_pos=} {end_pos=}")
    # print_grid(grid, size)

    def path_to_set(path):
        p = path
        s = set()
        while p:
            s.add(p.state)
            p = p.parent
        return s

    path = find_path(start_pos, end_pos, grid, size)
    last_rock = 0j
    for next_rock in more_rocks:
        x, y = to_list_int(next_rock)
        grid[x + y * 1j] = 1
        last_rock = x + y * 1j
        if last_rock in path_to_set(path):
            path = find_path(start_pos, end_pos, grid, size)
            if not path:
                break

    # print()
    # print(f"{last_rock=}")
    # print_grid(grid, size)
    return f"{int(last_rock.real)},{int(last_rock.imag)}"


def main():
    loader = LoaderLib(2024)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(18)
        size = Size(71, 71)
        rock_falls = 1024
    else:
        input_text = dedent(
            """\
                5,4
                4,2
                4,5
                3,0
                2,1
                6,3
                2,4
                1,5
                0,6
                3,3
                2,6
                5,1
                1,2
                5,5
                2,5
                6,5
                1,4
                0,4
                6,4
                1,1
                6,1
                1,0
                0,5
                1,6
                2,0
            """
        ).strip("\n")
        size = Size(7, 7)
        rock_falls = 12
    # lines = [
    #     (extract_ints(param)) for param in [line for line in lines_to_list(input_text)]
    # ]
    # lines = [lines_to_list(line) for line in input_text.split("\n\n")]
    lines = lines_to_list(input_text)

    # setup grid using complex numbers for coordinates up to `size`
    grid = defaultdict(int)
    for y in range(size.cy):
        for x in range(size.cx):
            grid[x + y * 1j] = 0

    # now fill the grid with the input data, representing the coordinates as complex numbers again
    for line in lines[:rock_falls]:
        x, y = to_list_int(line)
        grid[x + y * 1j] = 1

    loader.print_solution("setup", f"{len(lines)=} ...")
    loader.print_solution(
        1,
        part1(
            grid,
            size,
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
            size,
            lines[rock_falls:],
        ),
    )


if __name__ == "__main__":
    main()
    # --
    # --------------------------------------------------------------------------------
    # LAP -> 0.001741        |        0.001741 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : len(lines)=3450 ...
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.010326        |        0.012068 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 272
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.156167        |        0.168235 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 2   : 16,44
    # --------------------------------------------------------------------------------
