"""
Advent of code 2023
Day 10: Pipe Maze
"""
from enum import Enum
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


# Pipe Maze elements:
#  | is a vertical pipe connecting north and south.
#  - is a horizontal pipe connecting east and west.
#  L is a 90-degree bend connecting north and east.
#  J is a 90-degree bend connecting north and west.
#  7 is a 90-degree bend connecting south and west.
#  F is a 90-degree bend connecting south and east.
#  . is ground; there is no pipe in this tile.
#  S is the starting position of the animal;
#    there is a pipe on this tile, but your sketch
#    doesn't show what shape the pipe has.
NORTH = (0, 1)
SOUTH = (0, -1)
EAST = (1, 0)
WEST = (-1, 0)


class PipeDirection(Enum):
    north_south = (NORTH, SOUTH)
    east_west = (EAST, WEST)
    north_east = (NORTH, EAST)
    north_west = (NORTH, WEST)
    south_east = (SOUTH, EAST)
    south_west = (SOUTH, WEST)
    no_direction = ()
    all_directions = (NORTH, SOUTH, EAST, WEST)

    def inverse(self):
        return PipeDirection(*[d * -1 for d in self.value])


class Pipe:
    def __init__(
        self,
        pipe_character,
    ):
        self.pipe_character = pipe_character
        self.directions = self.tranlate_character_to_directions(
            pipe_character
            ).value

    def tranlate_character_to_directions(self, pipe_character):
        if pipe_character == "|":
            return PipeDirection.north_south
        elif pipe_character == "-":
            return PipeDirection.east_west
        elif pipe_character == "L":
            return PipeDirection.north_east
        elif pipe_character == "J":
            return PipeDirection.north_west
        elif pipe_character == "7":
            return PipeDirection.south_west
        elif pipe_character == "F":
            return PipeDirection.south_east
        elif pipe_character == ".":
            return PipeDirection.no_direction
        elif pipe_character == "S":
            return PipeDirection.all_directions
        else:
            raise ValueError(f"Unknown pipe character: {pipe_character}")

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.pipe_character}"

    def __str__(self):
        return self.pipe_character


def print_grid(grid):
    # print the grid
    xlate = {
        "|": "│",
        "-": "─",
        "L": "└",
        "J": "┘",
        "7": "┐",
        "F": "┌",
        ".": "░",
        "S": "┼",
    }
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] in xlate:
                print(xlate[grid[row][col]], end="")
            else:
                print(grid[row][col], end="")
        print()


def pad_grid(grid):
    # Pad out the grid with an empty border for easier parsing
    for i in range(len(grid)):
        grid[i].append(".")
        grid[i].insert(0, ".")

    empty_row = list("." * len(grid[0]))
    grid.append(empty_row)
    grid.insert(0, empty_row)

    return grid


def generate_grid(lines):
    grid = [list(line.strip("\n")) for line in lines]

    grid = pad_grid(grid)

    # the directions NESW are represented by 0, 1, 2, and 3
    tiles = [".", "-", "|", "7", "J", "L", "F"]
    tile_outputs = [
        [-1, -1, 0, 3, -1, -1, 1],
        [-1, 1, -1, 2, 0, -1, -1],
        [-1, -1, 2, -1, 3, 1, -1],
        [-1, 3, -1, -1, -1, 0, 2],
    ]
    return grid, tiles, tile_outputs


def find_starting_position(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "S":
                return [j, i]


def find_starting_direction(grid, tiles, tile_outputs, animal_position):
    if tile_outputs[0][tiles.index(grid[animal_position[1] - 1][animal_position[0]])] != -1:
        direction = 0
    elif tile_outputs[1][tiles.index(grid[animal_position[1]][animal_position[0] + 1])] != -1:
        direction = 1
    else:
        direction = 2

    return direction


def part1(lines) -> int:
    """
    Right, our animal is starting at the S tile.
    We need to follow the pipes until we reach the
    point furthest away from the animal---in number
    of steps.
    Since the connected pipes are in a ring, we can
    see that the furthest distance is half the number
    of pipes in the ring. However, there are pipes
    present in the ring that are not connected to
    the animal's starting position. We need to
    determine the number of pipes in the ring that
    are connected to the starting position.
    """
    grid, tiles, tile_outputs = generate_grid(lines)
    animal_position = find_starting_position(grid)
    direction = find_starting_direction(grid, tiles, tile_outputs, animal_position)

    tile_count = 0
    while True:
        match direction:
            case 0:
                animal_position = [animal_position[0], animal_position[1] - 1]
            case 1:
                animal_position = [animal_position[0] + 1, animal_position[1]]
            case 2:
                animal_position = [animal_position[0], animal_position[1] + 1]
            case 3:
                animal_position = [animal_position[0] - 1, animal_position[1]]

        if grid[animal_position[1]][animal_position[0]] == "S":
            break

        direction = tile_outputs[direction][tiles.index(grid[animal_position[1]][animal_position[0]])]
        tile_count += 1

    return tile_count // 2 + 1


def make_pipe(grid, animal_position):
    """
    We need to determine the shape of the pipe
    at the animal's current position. We can do
    this by looking at the directions of the
    adjacent pipes.
    """
    if grid[animal_position[1] - 1][animal_position[0]] in "|LJ":
        if grid[animal_position[1]][animal_position[0] + 1] in "-FJ":
            return "L"
        elif grid[animal_position[1]][animal_position[0] - 1] in "-7F":
            return "J"
        else:
            return "|"
    elif grid[animal_position[1] + 1][animal_position[0]] in "|7F":
        if grid[animal_position[1]][animal_position[0] + 1] in "-FJ":
            return "7"
        elif grid[animal_position[1]][animal_position[0] - 1] in "-7F":
            return "F"
        else:
            return "|"
    elif grid[animal_position[1]][animal_position[0] + 1] in "-FJ":
        return "-"
    elif grid[animal_position[1]][animal_position[0] - 1] in "-7F":
        return "-"
    else:
        raise ValueError("Unknown pipe shape")


def part2(lines) -> int:
    """
    We need to find the number of spaces enclosed by
    the pipes. The enclosed spaces are the ones that
    are not connected to the animal's starting position.
    We can do this by counting the spaces that are inside
    the ring, using the winding number algorithm.

    See: https://en.wikipedia.org/wiki/Nonzero-rule
    """
    grid, tiles, tile_outputs = generate_grid(lines)
    animal_position = find_starting_position(grid)
    direction = find_starting_direction(grid, tiles, tile_outputs, animal_position)

    # Gather the border tiles
    tile_border = set(tuple(animal_position))
    while True:
        match direction:
            case 0:
                animal_position = [animal_position[0], animal_position[1] - 1]
            case 1:
                animal_position = [animal_position[0] + 1, animal_position[1]]
            case 2:
                animal_position = [animal_position[0], animal_position[1] + 1]
            case 3:
                animal_position = [animal_position[0] - 1, animal_position[1]]

        if grid[animal_position[1]][animal_position[0]] == "S":
            grid[animal_position[1]][animal_position[0]] = make_pipe(grid, animal_position)
            break

        direction = tile_outputs[direction][tiles.index(grid[animal_position[1]][animal_position[0]])]
        tile_border.add(tuple(animal_position))

    # Count the inner tiles
    inner_tile_count = 0

    for row in range(len(grid)):
        parity = 0
        for col in range(len(grid[row])):
            if (col, row) not in tile_border:
                if parity % 2 == 1:
                    inner_tile_count += 1
                    grid[row][col] = "X"
                else:
                    grid[row][col] = "."
                continue
            # Parity changes when we encounter a border tile, the vertical
            # pipes are the easiest to check for parity; but we also need
            # to check the corners on the horizontal pipes. The horizontal
            # pipes are ignored because they always follow a corner.
            if grid[row][col] in "|LJ":
                parity += 1

    # print_grid(grid)
    return inner_tile_count - 1


def main():
    loader = LoaderLib(2023)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(10)
    else:
        input_text = dedent(
            """\
            7-F7-
            .FJ|7
            SJLL7
            |F--J
            LJ.LJ
            """
        ).strip("\n")
    lines = lines_to_list(input_text)

    loader.print_solution("setup", f"{len(lines)=} ...")
    loader.print_solution(
        1,
        part1(
            lines,
        ),
    )
    if testing:
        input_text = dedent(
            """\
            FF7FSF7F7F7F7F7F---7
            L|LJ||||||||||||F--J
            FL-7LJLJ||||||LJL-77
            F--JF--7||LJLJ7F7FJ-
            L---JF-JLJ.||-FJLJJ7
            |F|F-JF---7F7-L7L|7|
            |FFJF7L7F-JF7|JL---7
            7-L-JL7||F7|L7F-7F7|
            L.L7LFJ|||||FJL7||LJ
            L7JLJL-JLJLJL--JLJ.L
            """
        ).strip("\n")
        lines = lines_to_list(input_text)
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
    # LAP -> 0.000699        |        0.000699 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : len(lines)=140 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    # LAP -> 0.010636        |        0.011335 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 6968
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    # LAP -> 0.027671        |        0.039005 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 2   : 413
    # --------------------------------------------------------------------------------
