"""
Advent of code 2023
Day 22: Sand Slabs
"""

import itertools
from collections import defaultdict
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import extract_ints, lines_to_list, to_list_int


def parse_bricks(lines):
    bricks = {}
    for i, line in enumerate(lines):
        coords = line.split("~")
        start = tuple(map(int, coords[0].split(",")))
        end = tuple(map(int, coords[1].split(",")))
        brick_id = chr(65 + i)

        brick_cubes = set()
        for x, y in itertools.product(
            range(min(start[0], end[0]), max(start[0], end[0]) + 1),
            range(min(start[1], end[1]), max(start[1], end[1]) + 1),
        ):
            for z in range(min(start[2], end[2]), max(start[2], end[2]) + 1):
                brick_cubes.add((x, y, z))
        bricks[brick_id] = brick_cubes
    return bricks


def settle_bricks(bricks):
    occupied = set()
    settled_positions = {}

    for brick_id, cubes in sorted(
        bricks.items(), key=lambda x: min(c[2] for c in x[1])
    ):
        while True:
            new_cubes = {(x, y, z - 1) for x, y, z in cubes}
            if any(c[2] == 0 for c in new_cubes) or not new_cubes.isdisjoint(occupied):
                break
            cubes = new_cubes
        settled_positions[brick_id] = cubes
        occupied.update(cubes)

    return settled_positions


def build_support_graph(bricks):
    support_graph = defaultdict(set)
    for brick_id, cubes in bricks.items():
        for x, y, z in cubes:
            if (x, y, z - 1) in bricks[brick_id]:
                continue
            for below_id, below_cubes in bricks.items():
                if below_id != brick_id and (x, y, z - 1) in below_cubes:
                    support_graph[brick_id].add(below_id)
    return support_graph


def can_disintegrate(brick_id, bricks, support_graph):
    temp_bricks = {k: v for k, v in bricks.items() if k != brick_id}
    
    # Recompute the support graph without the selected brick
    temp_graph = build_support_graph(temp_bricks)

    # Perform a topological sort to check for instability
    unstable = set()
    visited = set()
    stack = [k for k in temp_bricks if not temp_graph[k]]

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        for nbr in temp_graph[node]:
            if nbr not in visited:
                stack.append(nbr)

    return len(visited) == len(temp_bricks)


def part1(lines: list[str]) -> int:
    """ """
    bricks = parse_bricks(lines)
    settled = settle_bricks(bricks)
    support_graph = build_support_graph(settled)

    safe_count = 0
    for brick_id in bricks.keys():
        if can_disintegrate(brick_id, settled, support_graph):
            safe_count += 1

    return safe_count


def part2(lines: list[str]) -> int:
    """ """
    ...


def main():
    loader = LoaderLib(2024)
    testing = True
    if not testing:
        input_text = loader.get_aoc_input(22)
    else:
        input_text = dedent(
            """\
                1,0,1~1,2,1
                0,0,2~2,0,2
                0,2,3~2,2,3
                0,0,4~0,2,4
                2,0,5~2,2,5
                0,1,6~2,1,6
                1,1,8~1,1,9
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
    # -
