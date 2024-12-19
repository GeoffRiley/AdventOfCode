"""
Advent of code 2024
Day 16: Reindeer Maze
"""

from collections import defaultdict
import heapq
import itertools
import sys
from textwrap import dedent

from loader import LoaderLib
from utility import lines_to_list
from grid import Grid


def set_grid_value(grid: Grid, r: int, c: int, value: str):
    if 0 <= r < grid.height() and 0 <= c < grid.width() and grid[r, c] not in "#SE":
        grid[r, c] = value


def dijkstra(maze: Grid, dist: defaultdict, start_s: str, end_s: str) -> int:
    rows = maze.height()
    cols = maze.width()

    # Find start (S) and end (E)
    start = None
    end = None
    for r, c in itertools.product(range(rows), range(cols)):
        if maze[r, c] == start_s:
            start = (r, c)
        if maze[r, c] == end_s:
            end = (r, c)

    # Directions: 0 = North, 1 = East, 2 = South, 3 = West
    # dx, dy for these directions (row, col)
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    start_direction = (
        1 if start_s == "S" else 3
    )  # Facing East initially or West for the return trip
    start_cost = 0

    # Priority queue for Dijkstra’s: (cost, r, c, d)
    pq = []
    heapq.heappush(pq, (start_cost, start[0], start[1], start_direction))

    # Distances dictionary: (r, c, d) -> best known cost
    dist[(start[0], start[1], start_direction)] = start_cost

    while pq:
        cost, r, c, d = heapq.heappop(pq)

        # If this is not the best known cost for this state, skip
        if dist[(r, c, d)] < cost:
            continue

        # Check if we've reached the goal
        if (r, c) == end:
            return cost

        # Try moving forward
        dr, dc = directions[d]
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and maze[nr, nc] != "#":
            new_cost = cost + 1
            new_state = (nr, nc, d)
            if new_cost < dist[new_state]:
                dist[new_state] = new_cost
                set_grid_value(maze, nr, nc, "x")
                heapq.heappush(pq, (new_cost, nr, nc, d))

        # Try turning left
        left_d = (d - 1) % 4
        new_cost = cost + 1000
        new_state = (r, c, left_d)
        if new_cost < dist[new_state]:
            dist[new_state] = new_cost
            # set_grid_value(maze, r, c, "<")
            heapq.heappush(pq, (new_cost, r, c, left_d))

        # Try turning right
        right_d = (d + 1) % 4
        new_cost = cost + 1000
        new_state = (r, c, right_d)
        if new_cost < dist[new_state]:
            dist[new_state] = new_cost
            # set_grid_value(maze, r, c, ">")
            heapq.heappush(pq, (new_cost, r, c, right_d))

        # Try turning around
        rear_d = (d + 2) % 4
        new_cost = cost + 2000  # Two turns
        new_state = (r, c, rear_d)
        if new_cost < dist[new_state]:
            dist[new_state] = new_cost
            # set_grid_value(maze, r, c, "v")
            # heapq.heappush(pq, (new_cost, r, c, rear_d))

    # If we exit the loop without returning, no path was found
    return None


def part1(maze: Grid, dist: defaultdict) -> int:
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
    return dijkstra(maze, dist, "S", "E")


def part2(maze: Grid, dist1: defaultdict, dist2: defaultdict, target_cost: int) -> int:
    print("Before")
    print(maze.transpose())
    # _ = dijkstra(maze, dist1, "S", "E")
    _ = dijkstra(maze, dist2, "E", "S")
    best_path_tiles = set()
    for r, c in itertools.product(range(maze.height()), range(maze.width())):
        if maze[r, c] != "#":
            f_min = min(dist1[(r, c, d)] for d in range(4))
            b_min = min(dist2[(r, c, d)] for d in range(4))
            best_cost = f_min + b_min

            if best_cost == target_cost:
                best_path_tiles.add((r, c))
                set_grid_value(maze, r, c, "O")
            else:
                set_grid_value(maze, r, c, ".")

    print("After")
    print(maze.transpose())
    return len(best_path_tiles)


def main():
    loader = LoaderLib(2024)
    testing = False
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
    grid = Grid().from_text(lines).transpose()
    dist1 = defaultdict(lambda: sys.maxsize)
    dist2 = defaultdict(lambda: sys.maxsize)

    loader.print_solution("setup", f"{len(lines)=} ...")
    loader.print_solution(
        1,
        target_cost := part1(
            grid,
            dist1,
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
            dist1,
            dist2,
            target_cost,
        ),
    )


if __name__ == "__main__":
    main()
    # --
    # --------------------------------------------------------------------------------
    # LAP -> 0.269168        |        0.269168 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : len(lines)=141 ...
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 1201.294138     |     1201.563306 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 94436
    # --------------------------------------------------------------------------------

    # The following is incorrect!!  The correct answer is 481.
    # --------------------------------------------------------------------------------
    # LAP -> 2252.004443     |     3453.567750 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 2   : 367
    # --------------------------------------------------------------------------------
