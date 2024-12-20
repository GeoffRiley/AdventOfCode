"""
Advent of code 2024
Day 20: Race Condition
"""

from collections import Counter, defaultdict, deque
from enum import Enum
from textwrap import dedent
from typing import Any

from aoc.loader import LoaderLib
from aoc.grid import Grid


class Element(Enum):
    wall = "#"
    empty = "."
    start = "S"
    end = "E"


def bfs(grid, start, end, allow_cheat=False) -> Any | float:
    rows, cols = grid.height(), grid.width()
    queue = deque()
    visited = {}
    # State: (x, y, cheat_remaining)
    queue.append((start[0], start[1], 0, 0))  # x, y, cheat_remaining, time
    visited[(start[0], start[1], 0)] = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while queue:
        x, y, cheat, time = queue.popleft()
        if (x, y) == end:
            return time
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            # Check boundaries
            if 0 <= nx < cols and 0 <= ny < rows:
                cell = grid[nx, ny]
                if cell != Element.wall.value or cheat > 0:
                    next_cheat = max(cheat - 1, 0)
                    # If not currently cheating and cell is wall, can start cheating
                    if cell == Element.wall.value and cheat == 0 and allow_cheat:
                        # Start cheating: allow passing through
                        if (nx, ny, 1) not in visited or visited[
                            (nx, ny, 1)
                        ] > time + 1:
                            visited[(nx, ny, 1)] = time + 1
                            queue.append((nx, ny, 1, time + 1))
                    elif (nx, ny, next_cheat) not in visited or visited[
                        (nx, ny, next_cheat)
                    ] > time + 1:
                        visited[(nx, ny, next_cheat)] = time + 1
                        queue.append((nx, ny, next_cheat, time + 1))
    return float("inf")  # If no path found


def find_all_cheats(grid, start, end, fastest_time) -> defaultdict[Any, int]:
    rows, cols = grid.height(), grid.width()
    cheats = defaultdict(int)
    # Iterate over all possible positions to activate the cheat
    for y in range(rows):
        for x in range(cols):
            if grid[x, y] in (
                Element.empty.value,
                Element.start.value,
                Element.end.value,
            ):
                cheat_start = (x, y)
                # Iterate over all possible positions to end the cheat after 2 moves
                # We'll perform BFS with cheat activated at cheat_start
                # and lasting exactly 2 moves
                queue = deque()
                visited = {}
                queue.append(
                    (start[0], start[1], False, 0, 0)
                )  # x, y, cheated, cheat_moves, time
                visited[(start[0], start[1], False, 0)] = 0
                while queue:
                    cx, cy, cheated, cheat_moves, time = queue.popleft()
                    if (cx, cy) == end:
                        break
                    for nx, ny in grid.neighbors(cx, cy):
                        cell = grid[nx, ny]
                        next_cheated = cheated
                        next_cheat_moves = cheat_moves
                        if next_cheated:
                            if cheat_moves < 2:
                                # Continue cheating
                                next_cheat_moves += 1
                            if cheat_moves == 2:
                                # Cheat ends, must be on normal track
                                if cell == Element.wall:
                                    continue
                                next_cheated = False
                                next_cheat_moves = 0
                        elif (cx, cy) == cheat_start:
                            if cell != Element.wall.value:
                                continue
                            next_cheated = True
                            next_cheat_moves = 1
                        state = (nx, ny, next_cheated, next_cheat_moves)
                        if state not in visited or visited[state] > time + 1:
                            visited[state] = time + 1
                            queue.append(
                                (nx, ny, next_cheated, next_cheat_moves, time + 1)
                            )
                # Calculate time saved
                cheat_time = visited.get((end[0], end[1], False, 0), float("inf"))
                if cheat_time < fastest_time:
                    saved = fastest_time - cheat_time
                    cheats[saved] += 1
    return cheats


def part1(grid: Grid) -> int:
    """ """
    start = end = None
    for y in range(grid.height()):
        for x in range(grid.width()):
            cell = grid[x, y]
            if cell == Element.start.value:
                start = (x, y)
            elif cell == Element.end.value:
                end = (x, y)
    fastest_time = bfs(grid, start, end)
    print(f"Fastest time without cheating: {fastest_time} picoseconds")

    cheats = find_all_cheats(grid, start, end, fastest_time)
    # Count cheats that save at least 100 picoseconds
    counter = Counter(cheats)
    print(f"Cheats that save time: {counter}")
    count = sum(save >= 100 for save in cheats)
    print(f"Number of cheats that save at least 100 picoseconds: {count}")
    return count


def part2(grid: Grid) -> int:
    """ """
    ...


def main():
    loader = LoaderLib(2024)
    testing = True
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
    grid = Grid.from_text(input_text)

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
