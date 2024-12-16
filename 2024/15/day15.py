"""
Advent of code 2024
Day 15: Warehouse Woes
"""

from collections import Counter, deque
from textwrap import dedent
from typing import Any

from aoc.geometry import Point, Rectangle, Size
from aoc.grid import Grid
from aoc.loader import LoaderLib
from aoc.utility import extract_ints, lines_to_list, to_list_int


def parse_map_and_scale(input_map) -> tuple[list, set, tuple[int, int] | None]:
    # Scale the map and maintain coupled box representation
    scaled_map = []
    box_positions = set()  # Track upper (`[`) and lower (`]`) pairs
    robot_position = None

    for r, row in enumerate(input_map):
        scaled_row = []
        for c, cell in enumerate(row):
            if cell == "#":
                scaled_row.extend("##")
            elif cell == ".":
                scaled_row.extend("..")
            elif cell == "@":
                scaled_row.extend("@.")
                robot_position = (r, c * 2)  # Track robot's starting position
            elif cell == "O":
                scaled_row.extend("[]")
                box_positions.add((r, c * 2))  # Add `[` position
                box_positions.add((r, c * 2 + 1))  # Add `]` position
        scaled_map.append("".join(scaled_row))

    return scaled_map, box_positions, robot_position


def move_robot(
    scaled_map, box_positions, robot_position, moves
) -> tuple[Any, Any | tuple]:
    # Simulate robot movement
    directions = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}
    for move in moves:
        dr, dc = directions[move]
        r, c = robot_position
        target = (r + dr, c + dc)

        if is_free_space(scaled_map, target):
            # Move robot
            scaled_map[r] = f"{scaled_map[r][:c]}.{scaled_map[r][c + 1:]}"
            scaled_map[r + dr] = (
                f"{scaled_map[r + dr][:c+dc]}@{scaled_map[r + dr][c+dc + 1:]}"
            )
            robot_position = target
        elif is_box(scaled_map, target, box_positions):
            # Attempt to push
            if can_push_box(scaled_map, target, dr, dc, box_positions):
                push_box(scaled_map, target, dr, dc, box_positions)
                robot_position = target
    return scaled_map, robot_position


def is_free_space(scaled_map, target) -> Any:
    r, c = target
    return scaled_map[r][c] == "."


def is_box(scaled_map, target, box_positions) -> bool:
    return target in box_positions


def is_wall(scaled_map, target) -> bool:
    r, c = target
    return scaled_map[r][c] == "#"


def is_within_bounds(scaled_map, r, c):
    """
    Check if a position is within the bounds of the map.
    """
    return 0 <= r < len(scaled_map) and 0 <= c < len(scaled_map[0])


def can_push_box(scaled_map, target, dr, dc, box_positions):
    """
    Determine if a chain of connected boxes can be pushed.
    """
    # Find all connected boxes starting from the target
    connected_boxes = get_connected_boxes(target, box_positions)

    # Check that all connected boxes can move in the direction (dr, dc)
    for box in connected_boxes:
        new_r, new_c = box[0] + dr, box[1] + dc

        # If any part of the chain is blocked, return False
        if not is_within_bounds(scaled_map, new_r, new_c) or is_wall(
            scaled_map, (new_r, new_c)
        ):
            return False

    return True


def push_box(scaled_map, target, dr, dc, box_positions):
    """
    Push the entire chain of connected boxes.
    """
    # Get all connected boxes
    connected_boxes = get_connected_boxes(target, box_positions)

    # Sort boxes in reverse order of the push direction
    # This ensures we move the farthest box first
    connected_boxes = sorted(
        connected_boxes, key=lambda box: (box[0] * dr + box[1] * dc), reverse=True
    )

    for box in connected_boxes:
        r, c = box
        new_r, new_c = r + dr, c + dc

        # Move the box on the map
        scaled_map[r] = f"{scaled_map[r][:c]}..{scaled_map[r][c + 2:]}"
        scaled_map[new_r] = (
            f"{scaled_map[new_r][:new_c]}[]{scaled_map[new_r][new_c + 2:]}"
        )

        # Update the box position
        box_positions.remove(box)
        box_positions.add((new_r, new_c))


def get_connected_boxes(start, box_positions) -> set:
    # Find all connected boxes (horizontally and vertically)
    connected = set()
    queue = [start]
    while queue:
        current = queue.pop()
        if current in box_positions and current not in connected:
            connected.add(current)
            for dr, dc in [(-1, 0), (1, 0), (0, -2), (0, 2)]:
                neighbor = (current[0] + dr, current[1] + dc)
                if neighbor in box_positions:
                    queue.append(neighbor)
    return connected


def from_direction(direction: str) -> Point:
    """Simplified direction mapping using a dictionary."""
    directions = {
        "^": Point(0, -1),
        "v": Point(0, 1),
        "<": Point(-1, 0),
        ">": Point(1, 0),
    }
    return directions.get(direction, ValueError(f"Invalid direction: {direction}"))


def part1(lines: list[str]) -> int:
    """
    The warehouse is a grid of rooms, each of which may contain a wall (#), an open space (.), or a box(O).
    The robot (@) can move up, down, left, or right, but cannot move through walls.
    The robot can push a box, but cannot pull one.
    The robot can push a box into a space, but cannot push a box into a wall.
    The robot can push a line of boxes in a row, but cannot push a line of boxes that includes a wall.
    The robot can push a line of boxes into a space, but cannot push a line of boxes into a wall.
    The robot can push a box into a space that already contains a box if that box is pushed into a space that is empty.
    No two boxes, walls, or the robot can occupy the same space.
    """
    # create a grid of the warehouse
    grid = Grid.from_text(lines[0])
    movements = lines[1]

    # find the robot and the boxes
    robot = None
    boxes = []
    for y in range(grid.height()):
        for x in range(grid.width()):
            if grid[x, y] == "@":
                robot = Point(x, y)
            elif grid[x, y] == "O":
                boxes.append(Point(x, y))
    print("Initial grid:")
    print(grid)
    # move the robot
    for move in movements:
        new_robot = robot + from_direction(move)
        # check if the robot can move
        if grid[new_robot] == ".":
            grid[robot] = "."
            grid[new_robot] = "@"
            robot = new_robot
        # check if the robot can push a line of boxes
        elif grid[new_robot] == "O":
            new_box = new_robot + from_direction(move)
            while grid[new_box] == "O":
                new_box = new_box + from_direction(move)
            if grid[new_box] == ".":
                grid[robot] = "."
                grid[new_robot] = "@"
                grid[new_box] = "O"
                robot = new_robot
                boxes.remove(new_robot)
                boxes.append(new_box)
        # print(f"{move=}")
        # print(grid)

    return sum((y * 100 + x) for x, y in boxes)


def part2(lines: list[str]) -> int:
    """
    Everything in the wearhouse is the same as part 1, except that all elenebts are now twice as wide other than the robot.
    The input is the same as part 1, but the following changes are made:
    - The robot (@) is now represented by a character followed by a 'open space character': @.
    - The walls (#) are now represented by double characters: ##
    - The open spaces (.) are now represented by double characters: ..
    - The boxes (O) are now represented by two characters: []
    The robot can still move up, down, left, or right, but cannot move through walls.
    The robot can push a box, but cannot pull one.
    The robot can push a box into a space, but cannot push a box into a wall.
    The robot can push a line of boxes in a row, but cannot push a line of boxes that includes a wall.
    The robot can push a line of boxes into a space, but cannot push a line of boxes into a wall.
    The robot can push a box into a space that already contains a box if that box is pushed into a space that is empty.
    No two boxes, walls, or the robot can occupy the same space.
    When pushing up or down, the robot can push on either half of the box.
    When pushing up or down, if the robot pushes a box into a a second box on either side, the second box will move.
    When pushing up or down, a wall will stop the box from moving if it meets on either side.
    """

    scaled_map, box_positions, robot_position = parse_map_and_scale(lines[0])

    scaled_map, robot_position = move_robot(
        scaled_map, box_positions, robot_position, lines[1]
    )

    return sum((y * 100 + x) for x, y in box_positions)


def main():
    loader = LoaderLib(2024)
    testing, tester = True, 2  # 1 or 2
    if not testing:
        input_text = loader.get_aoc_input(15)
    else:
        input_text1 = dedent(
            """\
                ########
                #..O.O.#
                ##@.O..#
                #...O..#
                #.#.O..#
                #...O..#
                #......#
                ########

                <^^>>>vv<v>>v<<
            """
        ).strip("\n")
        input_text2 = dedent(
            """\
                ##########
                #..O..O.O#
                #......O.#
                #.OO..O.O#
                #..O@..O.#
                #O#..O...#
                #O..O..O.#
                #.OO.O.OO#
                #....O...#
                ##########

                <vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
                vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
                ><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
                <<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
                ^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
                ^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
                >^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
                <><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
                ^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
                v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
            """
        ).strip("\n")
        input_text = input_text1 if tester == 1 else input_text2
    # lines = [(extract_ints(param)) for param in list(lines_to_list(input_text))]
    lines = [lines_to_list(line) for line in input_text.split("\n\n")]
    # movements are in the second list and need to be joined into a single string
    lines[1] = "".join(lines[1])
    # lines = lines_to_list(input_text)

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
    # -
