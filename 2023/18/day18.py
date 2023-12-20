"""
Advent of code 2023
Day 18: Lavaduct Lagoon

Amagumation of examples and solutions from the AoC reddit
Megathread: https://www.reddit.com/r/adventofcode/comments/5jvbzt/2016_day_18_solutions/
"""
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


dir_map = {
    "U": (0, 1),
    "D": (0, -1),
    "L": (-1, 0),
    "R": (1, 0),
    "3": (0, 1),
    "1": (0, -1),
    "2": (-1, 0),
    "0": (1, 0),
}


def shoelace(vertices):
    shoelace = 0
    for i in range(len(vertices) - 1):
        shoelace += (
            vertices[i][0] * vertices[i + 1][1] - vertices[i + 1][0] * vertices[i][1]
        )
    return abs(shoelace) // 2


def calcarea(pgen, instructions):
    vertices = [(0, 0)]
    perimeter = 0
    for dx, dy, steps in pgen(instructions):
        vertices.append((vertices[-1][0] + dx * steps, vertices[-1][1] + dy * steps))
        perimeter += steps

    return shoelace(vertices) + perimeter // 2 + 1


def part1generator(instructions):
    yield 0, 0, 0
    for uplr, steps, _ in instructions:
        yield (*dir_map[uplr], int(steps))


def part2generator(instructions):
    yield 0, 0, 0
    for _, _, code in instructions:
        yield (*dir_map[code[-1]], int(code[:-1], 16))


def part1(lines: list[str]) -> int:
    """ """
    intructions = [(line.split()) for line in lines]
    return calcarea(part1generator, intructions)


def part2(lines: list[str]) -> int:
    """ """
    intructions = [(line.replace("(#", "").replace(")", "").split()) for line in lines]
    return calcarea(part2generator, intructions)


def main():
    loader = LoaderLib(2023)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(18)
    else:
        input_text = dedent(
            """\
            R 6 (#70c710)
            D 5 (#0dc571)
            L 2 (#5713f0)
            D 2 (#d2c081)
            R 2 (#59c680)
            D 2 (#411b91)
            L 5 (#8ceee2)
            U 2 (#caa173)
            L 1 (#1b58a2)
            U 2 (#caa171)
            R 2 (#7807d2)
            U 3 (#a77fa3)
            L 2 (#015232)
            U 2 (#7a21e3)
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
    # -
