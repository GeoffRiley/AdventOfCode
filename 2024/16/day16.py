"""
Advent of code 2024
Day 16: Reindeer Maze
"""

from collections import Counter, deque
from textwrap import dedent

from loader import LoaderLib
from utility import lines_to_list
from grid import Grid


def left(direction: str) -> str:
    if direction == "N":
        return "W"
    if direction == "W":
        return "S"
    if direction == "S":
        return "E"
    if direction == "E":
        return "N"


def right(direction: str) -> str:
    if direction == "N":
        return "E"
    if direction == "E":
        return "S"
    if direction == "S":
        return "W"
    if direction == "W":
        return "N"


def part1(grid: Grid) -> int:
    """
    The reindeer is in a maze. He starts facing east at the start of the maze,
    marked by the letter S.
    The maze is a grid of cells, each of which is either empty (.) or a wall (#).
    The reindeer cannot move into a wall.
    The reindeer can only move forward or turn to the left or right.
    Movement has a cost of 1, and turning has a cost of 1000.
    The reindeer must get to the end of the maze, which is marked by the letter E,
    by the cheapest route possible.
    """
    directions = {
        "N": (-1, 0),
        "E": (0, 1),
        "S": (1, 0),
        "W": (0, -1),
    }
    # find the start and end
    start = end = None

    for row in range(grid.height()):
        for col in range(grid.width()):
            char = grid[row, col]
            if char == "S":
                start = (row, col)
            if char == "E":
                end = (row, col)

    # find the path
    path = ""
    visited = set()
    current = (start, "E")
    total_cost = 0
    queue = deque([(path, current, visited, total_cost)])
    completed_paths = []
    while queue:
        path, current, visited, total_cost = queue.popleft()
        if tuple(current) in visited:
            continue
        visited.add(tuple(current))
        if current[0] == end:
            completed_paths.append([path, total_cost])
            continue
        for dir in [left(current[1]), current[1], right(current[1])]:
            new_pos = (
                current[0][0] + directions[dir][0],
                current[0][1] + directions[dir][1],
            )
            if grid[new_pos[0], new_pos[1]] == "#":
                continue
            if dir == current[1]:
                new_cost = total_cost + 1
                queue.append([path + dir, (new_pos, dir), visited, new_cost])
            else:
                new_cost = total_cost + 1000
                queue.append([path + dir, (current[0], dir), visited, new_cost])
    return min((path for path in completed_paths), key=lambda x: x[1])


def part2(lines: list[str]) -> int:
    """ """
    ...


def main():
    loader = LoaderLib(2024)
    testing = True
    if not testing:
        input_text = loader.get_aoc_input(16)
    else:
        input_text = dedent(
            """\
                #################
                #...#...#...#..E#
                #.#.#.#.#.#.#.#.#
                #.#.#.#...#...#.#
                #.#.#.#.###.#.#.#
                #...#.#.#.....#.#
                #.#.#.#.#.#####.#
                #.#...#.#.#.....#
                #.#.#####.#.###.#
                #.#.#.......#...#
                #.#.###.#####.###
                #.#.#...#.....#.#
                #.#.#.#####.###.#
                #.#.#.........#.#
                #.#.#.#########.#
                #S#.............#
                #################
            """
        ).strip("\n")
    # lines = [
    #     (extract_ints(param)) for param in [line for line in lines_to_list(input_text)]
    # ]
    # lines = [lines_to_list(line) for line in input_text.split("\n\n")]
    lines = lines_to_list(input_text)
    grid = Grid().from_text(lines)

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
            lines,
        ),
    )


if __name__ == "__main__":
    main()
    # --
    # -
