"""
Advent of code 2023
Day 23: A Long Walk
"""

import sys
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


# Directions for normal movement
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Mapping for slope tiles
SLOPE_DIR = {
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1),
}


def part1(lines):
    # Read the input map from stdin
    grid = [list(line.rstrip("\n")) for line in lines if line.strip() != ""]
    rows = len(grid)
    cols = len(grid[0])

    # Find the start (top row '.') and end (bottom row '.') positions
    start = None
    end = None
    for c in range(cols):
        if grid[0][c] == ".":
            start = (0, c)
            break
    for c in range(cols):
        if grid[rows - 1][c] == ".":
            end = (rows - 1, c)
            break

    # A recursive DFS to find the longest path
    # state:
    #   r, c: current position
    #   visited: set of visited coordinates
    #   slope_forced: whether we must move in a forced slope direction and what that direction is.
    # returns the length of the longest path starting from this position under current conditions.
    sys.setrecursionlimit(10**7)

    best_path_length = 0

    def dfs(r, c, visited, forced_dir=None):
        nonlocal best_path_length
        # If we've reached the end tile, update best path
        if (r, c) == end:
            path_length = len(visited)
            if path_length > best_path_length:
                best_path_length = path_length
            return

        current_tile = grid[r][c]

        # Determine next possible moves
        if current_tile in SLOPE_DIR:
            # If on a slope tile, the next move is forced
            next_moves = []
            dr, dc = SLOPE_DIR[current_tile]
            nr, nc = r + dr, c + dc
            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and ((nr, nc) not in visited and grid[nr][nc] != "#")
            ):
                next_moves.append((nr, nc))
        else:
            # On a normal path tile, if we came from a slope tile, we must follow forced_dir
            if forced_dir is not None:
                # Forced direction movement
                dr, dc = forced_dir
                nr, nc = r + dr, c + dc
                next_moves = []
                if (
                    0 <= nr < rows
                    and 0 <= nc < cols
                    and ((nr, nc) not in visited and grid[nr][nc] != "#")
                ):
                    next_moves.append((nr, nc))
            else:
                # No forced direction, can move in any of the four directions
                next_moves = []
                for dr, dc in DIRECTIONS:
                    nr, nc = r + dr, c + dc
                    if (
                        0 <= nr < rows
                        and 0 <= nc < cols
                        and ((nr, nc) not in visited and grid[nr][nc] != "#")
                    ):
                        next_moves.append((nr, nc))

        # For each next move, figure out if the next step is forced or not
        for nr, nc in next_moves:
            next_tile = grid[nr][nc]
            # If next_tile is a slope, the step after that must follow its direction
            # So after moving onto a slope tile, the next move is forced by that slope
            # If next_tile is not a slope, no forced direction after that move.
            next_forced = None
            if current_tile in SLOPE_DIR:
                # We've just come from a slope tile, direction was forced, but we made the move already
                next_forced = None
            elif forced_dir is not None:
                # We are currently forced by a previous slope. We took that forced step,
                # so after this, no forced direction unless the next tile is also a slope.
                next_forced = None
            # If we land on a slope tile now, the next step after this will be forced:
            if next_tile in SLOPE_DIR:
                next_forced = SLOPE_DIR[next_tile]

            visited.add((nr, nc))
            dfs(nr, nc, visited, next_forced)
            visited.remove((nr, nc))

    # Start DFS from the start
    visited = set()
    visited.add(start)
    dfs(start[0], start[1], visited, None)

    # return the best path length found
    return best_path_length - 1


def part2(lines: list[str]) -> int:
    # Read the input map from stdin
    grid = [list(line.rstrip("\n")) for line in lines if line.strip() != ""]
    rows = len(grid)
    cols = len(grid[0])

    # Identify start and end
    start = None
    end = None
    for c in range(cols):
        if grid[0][c] == ".":
            start = (0, c)
            break
        # If slopes appear in the top row, treat them as paths too
        if grid[0][c] in "^v<>":
            start = (0, c)
            break
    for c in range(cols):
        if grid[rows - 1][c] == ".":
            end = (rows - 1, c)
            break
        # If slopes appear in the bottom row, treat them as paths too
        if grid[rows - 1][c] in "^v<>":
            end = (rows - 1, c)
            break

    # Convert slope tiles to '.' for simpler logic (or just check them as passable)
    def is_passable(tile):
        return tile != "#"  # Everything except '#' is now treated as passable

    sys.setrecursionlimit(10**7)

    best_path_length = 0

    def dfs(r, c, visited):
        nonlocal best_path_length
        # If we've reached the end tile, update best path
        if (r, c) == end:
            path_length = len(visited)
            if path_length > best_path_length:
                best_path_length = path_length
            return

        # Explore all four directions
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and ((nr, nc) not in visited and is_passable(grid[nr][nc]))
            ):
                visited.add((nr, nc))
                dfs(nr, nc, visited)
                visited.remove((nr, nc))

    visited = set()
    visited.add(start)
    dfs(start[0], start[1], visited)

    return best_path_length - 1


def main():
    loader = LoaderLib(2023)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(23)
    else:
        input_text = dedent(
            """\
                #.#####################
                #.......#########...###
                #######.#########.#.###
                ###.....#.>.>.###.#.###
                ###v#####.#v#.###.#.###
                ###.>...#.#.#.....#...#
                ###v###.#.#.#########.#
                ###...#.#.#.......#...#
                #####.#.#.#######.#.###
                #.....#.#.#.......#...#
                #.#####.#.#.#########v#
                #.#...#...#...###...>.#
                #.#.#v#######v###.###v#
                #...#.>.#...>.>.#.###.#
                #####v#.#.###v#.#.###.#
                #.....#...#...#.#.#...#
                #.#########.###.#.#.###
                #...###...#...#...#.###
                ###.###.#.###v#####v###
                #...#...#.#.>.>.#.>.###
                #.###.###.#.###.#.#v###
                #.....###...###...#...#
                #####################.#
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
    # --------------------------------------------------------------------------------
    # LAP -> 0.007537        |        0.007537 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : len(lines)=141 ...
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.178063        |        0.185600 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 2278
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 10944.434319    |    10944.619919 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 2   : 6734
    # --------------------------------------------------------------------------------
