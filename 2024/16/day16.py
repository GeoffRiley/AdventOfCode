"""
Advent of code 2024
Day 16: Reindeer Maze
"""

from collections import Counter, deque
import heapq
from textwrap import dedent

from loader import LoaderLib
from utility import lines_to_list
from grid import Grid


def part1(maze: Grid) -> int:
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
    rows = maze.height()
    cols = maze.width()

    # Find start (S) and end (E)
    start = None
    end = None
    for r in range(rows):
        for c in range(cols):
            if maze[r, c] == "S":
                start = (r, c)
            if maze[r, c] == "E":
                end = (r, c)

    # Directions: 0 = North, 1 = East, 2 = South, 3 = West
    # dx, dy for these directions (row, col)
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    # Heuristic function: Manhattan distance
    def heuristic(r, c):
        # Simple Manhattan distance from current to end
        return abs(r - end[0]) + abs(c - end[1])

    # Priority queue for A*: entries are (f_score, cost, r, c, d)
    # f_score = cost + heuristic
    # cost is the g_score (actual cost so far)

    # Initialize
    start_direction = 1  # facing East initially
    start_cost = 0

    pq = []
    heapq.heappush(
        pq,
        (
            heuristic(start[0], start[1]),
            start_cost,
            start[0],
            start[1],
            start_direction,
        ),
    )

    # Distances dictionary: (r, c, d) -> best cost found
    dist = {(start[0], start[1], start_direction): start_cost}

    cheapest_cost = float("inf")

    while pq:
        f, cost, r, c, d = heapq.heappop(pq)

        # Early termination - if f_score is already worse than best solution
        if f >= cheapest_cost:
            continue

        # If this is not the best known cost for this state, skip
        if dist.get((r, c, d), float("inf")) < cost:
            continue

        # Check goal
        if (r, c) == end:
            # return cost  # We've reached the goal with minimal cost
            cheapest_cost = min(cheapest_cost, cost)

        # Try moving forward
        dr, dc = directions[d]
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and maze[nr, nc] != "#":
            new_cost = cost + 1  # moving forward cost
            new_state = (nr, nc, d)
            if new_cost < dist.get(new_state, float("inf")):
                dist[new_state] = new_cost
                heapq.heappush(pq, (new_cost + heuristic(nr, nc), new_cost, nr, nc, d))

        # Try turning left and right
        # Turning left: (d - 1) mod 4
        left_d = (d - 1) % 4
        new_cost = cost + 1000
        new_state = (r, c, left_d)
        if new_cost < dist.get(new_state, float("inf")):
            dist[new_state] = new_cost
            heapq.heappush(pq, (new_cost + heuristic(r, c), new_cost, r, c, left_d))

        # Turning right: (d + 1) mod 4
        right_d = (d + 1) % 4
        new_cost = cost + 1000
        new_state = (r, c, right_d)
        if new_cost < dist.get(new_state, float("inf")):
            dist[new_state] = new_cost
            heapq.heappush(pq, (new_cost + heuristic(r, c), new_cost, r, c, right_d))

    return cheapest_cost


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
