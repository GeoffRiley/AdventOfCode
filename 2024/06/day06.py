"""
Advent of code 2024
Day 06: Guard Gallivant
"""

from textwrap import dedent
from typing import Tuple

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list
from grid import Grid


# Helper function to determine the next position based on facing direction
def move(position, facing):
    x, y = position
    if facing == "up":
        return x, y - 1
    elif facing == "right":
        return x + 1, y
    elif facing == "down":
        return x, y + 1
    elif facing == "left":
        return x - 1, y


# Rotate the guard's facing direction
def turn_right(facing):
    directions = ["up", "right", "down", "left"]
    return directions[(directions.index(facing) + 1) % 4]


def simulate_patrol_with_history(start_position, start_facing, grid):
    history = []  # Store (position, facing) as guard patrols
    guard_position = start_position
    facing = start_facing

    while True:
        next_position = move(guard_position, facing)

        if next_position not in grid.grid:
            break  # Guard leaves the map

        history.append((guard_position, facing))

        if grid.grid.get(next_position) == "#":
            facing = turn_right(facing)
        else:
            guard_position = next_position

    return history


def get_candidate_obstruction_positions(start_position, start_facing, grid):
    candidate_positions = set()
    guard_position = start_position
    facing = start_facing

    while True:
        next_position = move(guard_position, facing)

        if next_position not in grid.grid:
            break  # Guard leaves the map

        if grid.grid.get(next_position) == "#":
            facing = turn_right(facing)
        else:
            # Forward movement; consider the position in front
            candidate_positions.add(next_position)
            guard_position = next_position

    return candidate_positions


def causes_loop_with_history(history, obstruction_position, grid):
    # Add obstruction temporarily
    grid.grid[obstruction_position] = "#"

    # Follow patrol history up to the obstruction
    visited_positions = set()
    for position, facing in history:
        if position == obstruction_position:
            break  # Obstruction encountered; stop using history
        visited_positions.add((position, facing))

    # Continue simulation from the last position in history
    guard_position, facing = history[len(visited_positions) - 1]
    while True:
        next_position = move(guard_position, facing)

        if next_position not in grid.grid:
            grid.grid[obstruction_position] = "."  # Restore grid
            return False  # Guard leaves the map

        if next_position == obstruction_position:
            facing = turn_right(facing)
        elif grid.grid.get(next_position) == "#":
            facing = turn_right(facing)
        else:
            guard_position = next_position

        if (guard_position, facing) in visited_positions:
            grid.grid[obstruction_position] = "."  # Restore grid
            return True  # Loop detected

        visited_positions.add((guard_position, facing))

    # # Restore the grid before returning
    # grid.grid[obstruction_position] = "."
    # return False


def part1(grid: Grid, guard_position: Tuple[int, int], facing: str) -> int:
    """ """
    # Set to track distinct positions visited
    visited_positions = set()
    visited_positions.add(guard_position)

    # Simulate the guard's patrol
    while True:
        next_position = move(guard_position, facing)

        # Check if the next position is within the map bounds
        if next_position not in grid.grid:
            break  # Guard has left the map

        # If there is an obstacle, turn right
        if grid[next_position] == "#":
            facing = turn_right(facing)
        else:
            # Otherwise, move forward and mark the position as visited
            guard_position = next_position
            visited_positions.add(guard_position)

    # Count the number of distinct positions visited
    return len(visited_positions)


def part2(grid: Grid, guard_position: Tuple[int, int], facing: str) -> int:
    """ """
    # reachable_positions = get_reachable_positions(guard_position, facing, grid)
    candidate_positions = get_candidate_obstruction_positions(
        guard_position, facing, grid
    )

    # Precompute the patrol history without obstructions
    patrol_history = simulate_patrol_with_history(guard_position, facing, grid)

    # Check loop-causing positions incrementally
    loop_causing_positions = [
        pos
        for pos in candidate_positions
        if causes_loop_with_history(patrol_history, pos, grid)
    ]

    return len(loop_causing_positions)


def main() -> None:
    loader = LoaderLib(2024)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(6)
    else:
        input_text = dedent(
            """\
                ....#.....
                .........#
                ..........
                ..#.......
                .......#..
                ..........
                .#..^.....
                ........#.
                #.........
                ......#...
            """
        ).strip("\n")
    lines = [list(param) for param in [line for line in lines_to_list(input_text)]]
    # lines = [lines_to_list(line) for line in input_text.split("\n\n")]
    # lines = lines_to_list(input_text)

    # p = input_text.index('^')
    # starting_pos = divmod(p, len(lines[0])+1)

    grid = Grid.from_text(input_text)

    facing_directions = {"^": "up", ">": "right", "v": "down", "<": "left"}
    guard_position = None
    facing = None

    for pos, value in grid.grid.items():
        if value in facing_directions:
            guard_position = pos
            facing = facing_directions[value]
            grid[pos] = "."  # Clear the starting position marker

    loader.print_solution(
        "setup",
        f"({len(lines)} x {len(lines[0])}) starting at {guard_position} {facing=}...",
    )
    loader.print_solution(
        1,
        part1(
            grid,
            guard_position,
            facing,
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
        part2(grid, guard_position, facing),
    )


if __name__ == "__main__":
    main()
    # --
    # --------------------------------------------------------------------------------
    # LAP -> 0.011391        |        0.011391 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : (130 x 130) starting at (51, 89) facing='up'...
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.002095        |        0.013486 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 5453
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 3.396539        |        3.410025 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 2   : 2188
    # --------------------------------------------------------------------------------
