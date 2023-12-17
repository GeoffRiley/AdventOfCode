"""
Advent of code 2023
Day 16: The Floor Will Be Lava
"""
from textwrap import dedent
from typing import Any, Generator

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


def shoot_beam(
        lines: list[str], starting_vector: tuple[int, int, int, int]
        ) -> int:
    """
    Project a beam of light, travelling along the given vector, into the grid,
    and follow it as it moves through the grid. It may encounter a mirror or a
    splitter.
    If the beam encounters a mirror, (i.e. / or \\), it will change direction
    though 90 degrees, and continue. If the beam encounters a splitter,
    (i.e. | or -), that is along the path of the beam, then the beam will
    continue unaffected. If the beam encounters a splitter that is not
    along the path of the beam, then the beam will split in two, and
    continue along both paths. The beam will continue until it reaches the
    edge of the grid, at which point it will stop.
    """
    # We'll maintain a stack of the current beam and sub beams
    # Initialise the stack with the starting vector
    stack = [starting_vector]
    # We'll maintain a set of all the points that have been seen
    seen = set()
    # We'll maintain a set of all the points that have been energized
    energized = set()

    while stack:
        x, y, dx, dy = stack.pop()

        while 0 <= x < len(lines[0]) and 0 <= y < len(lines):
            if (x, y, dx, dy) in seen:
                break

            seen.add((x, y, dx, dy))
            energized.add((x, y))

            this_char = lines[y][x]

            if this_char == ".":
                x += dx
                y += dy
                continue

            if this_char == "-":
                if dx:
                    x += dx
                    continue

                stack.append((x - 1, y, -1, 0))
                stack.append((x + 1, y, 1, 0))
                break

            if this_char == "|":
                if dy:
                    y += dy
                    continue

                stack.append((x, y - 1, 0, -1))
                stack.append((x, y + 1, 0, 1))
                break

            if this_char == "/":
                if dy == 1:
                    dx, dy = -1, 0
                    x += dx
                elif dy == -1:
                    dx, dy = 1, 0
                    x += dx
                elif dx == 1:
                    dx, dy = 0, -1
                    y += dy
                elif dx == -1:
                    dx, dy = 0, 1
                    y += dy
                continue

            if this_char == "\\":
                if dy == 1:
                    dx, dy = 1, 0
                    x += dx
                elif dy == -1:
                    dx, dy = -1, 0
                    x += dx
                elif dx == 1:
                    dx, dy = 0, 1
                    y += dy
                elif dx == -1:
                    dx, dy = 0, -1
                    y += dy

    return len(energized)


def beam_feeder(
    width: int, height: int
) -> Generator[tuple[int, int, int, int], Any, None]:
    """
    Generator that yields the starting vectors for the beam
    entering along each possible path on the grid.
    """
    # left side and the beam going right
    for y in range(height):
        yield (0, y, 1, 0)
    # top side and the beam going down
    for x in range(width):
        yield (x, 0, 0, 1)
    # right side and the beam going left
    for y in range(height):
        yield (width - 1, y, -1, 0)
    # bottom side and the beam going up
    for x in range(width):
        yield (x, height - 1, 0, -1)


def part1(lines: list[str]) -> int:
    """
    Project a beam of light, travelling right, into the top left of the grid,
    and follow it as it moves through the grid.
    """
    # We need to define a starting vector for the beam
    # top left corner and the beam going right
    starting_vector = (0, 0, 1, 0)

    return shoot_beam(lines, starting_vector)


def part2(lines: list[str]) -> int:
    """
    Now we try shooting beams from all positions on all four edges of the grid.
    We are looking for the position that gives the most energized points.
    """
    # We need to define a starting vectors for the beam
    width = len(lines[0])
    height = len(lines)

    return max(
        shoot_beam(lines, starting_vector)
        for starting_vector in beam_feeder(width, height)
    )


def main():
    loader = LoaderLib(2023)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(16)
    else:
        input_text = dedent(
            """\
            .|...\\....
            |.-.\\.....
            .....|-...
            ........|.
            ..........
            .........\\
            ..../.\\\\..
            .-.-/..|..
            .|....-|.\\
            ..//.|....
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
    #  LAP -> 0.000124        |        0.000124 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : len(lines)=110 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.004501        |        0.004625 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 8112
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 1.094059        |        1.098684 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 8314
    # --------------------------------------------------------------------------------
