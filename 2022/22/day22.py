"""
Advent of code 2022
Day 22: Monkey Map
"""
import re
from pathlib import Path
from typing import List, Tuple

from aoc.loader import LoaderLib

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3


def extract_route_path(route_string) -> Tuple[str, ...]:
    return tuple(re.findall(r'[0-9]+|[LR]', route_string))


def turn(facing: int, direction: str = "R", times: int = 1) -> int:
    return (RIGHT, DOWN, LEFT, UP)[(facing + times * (-1, 1)[direction == "R"]) % 4]


def part1(map_tile: List[str], route_path: Tuple[str, ...]) -> int:
    board = {}
    row_ends = {}
    col_ends = {}
    cur = None
    facing = RIGHT

    r = 0
    for inp in map_tile:
        r += 1
        for c, v in enumerate(inp, 1):
            if v != " ":
                board[r, c] = True if v == "." else False
                if board.get((r - 1, c)) is None:
                    col_ends[c] = (r, None)
                else:
                    col_ends[c] = (col_ends[c][0], r)
                if not cur and r == 1:
                    cur = (1, c)
                row_ends[r] = (row_ends.get(r, (c,))[0], c)

    for cmd in route_path:
        if cmd.isdecimal():
            steps = int(cmd)
            dp, di = facing not in (DOWN, UP), (1, -1)[facing in (LEFT, UP)]
            for _ in range(steps):
                new = cur[dp] + di
                ends = (col_ends, row_ends)[dp][cur[~dp]]
                if new < ends[0] or new > ends[1]:
                    new = ends[0] if di == 1 else ends[1]
                if not board[(new_pos := (cur[~dp], new) if dp else (new, cur[~dp]))]:
                    break
                cur = new_pos
        elif cmd == "R":
            facing = (DOWN, LEFT, UP, RIGHT)[facing]
        else:
            facing = (UP, RIGHT, DOWN, LEFT)[facing]

    return 1000 * cur[0] + 4 * cur[1] + facing


def part2(map_tile: List[str], route_path: Tuple[str, ...]) -> int:
    board = {}
    row_ends = {}
    col_ends = {}
    sections = set()
    cur = None
    facing = RIGHT
    side = 50

    r = 0
    for inp in map_tile:
        row_section = r // side + 1
        r += 1
        for c, v in enumerate(inp, 1):
            col_section = (c - 1) // side + 1
            if v != " ":
                sections.add((row_section, col_section))
                board[r, c] = (
                    (True, (row_section, col_section))
                    if v == "."
                    else (False, (row_section, col_section))
                )
                if board.get((r - 1, c)) is None:
                    col_ends[c] = (r, None)
                else:
                    col_ends[c] = (col_ends[c][0], r)
                if not cur and r == 1:
                    cur = (1, c)
                row_ends[r] = (row_ends.get(r, (c,))[0], c)

    for cmd in route_path:
        if cmd.isdecimal():
            steps = int(cmd)
            for _ in range(steps):
                new_facing, new_pos = facing, cur
                dp, di = facing not in (DOWN, UP), (1, -1)[facing in (LEFT, UP)]
                new = cur[dp] + di
                s1, s2 = board.get(cur)[1][:: -1 if dp else 1]
                ends = (col_ends, row_ends)[dp][cur[~dp]]
                if new < ends[0] or new > ends[1]:
                    ch_sec_pos = 1 if di == -1 else side
                    cn_sec_pos = cur[~dp] - side * (s2 - 1)

                    sec_a1 = s1 - 3 * di
                    sec_a2 = s1 + di
                    sec_a3 = s1 - di

                    sec_b1 = s2
                    sec_b2 = s2 + 2 * di
                    sec_b3 = s2 - di
                    sec_b4 = s2 + di
                    sec_b5 = s2 - 3 * di
                    sec_b6 = s2 + 3 * di
                    sec_b7 = s2 - 2 * di

                    val_a1 = facing
                    val_a2 = turn(facing, ("R", "L")[dp])
                    val_a3 = turn(facing, ("L", "R")[dp])
                    val_a4 = turn(facing, times=2)

                    val_b1 = (side + 1) - ch_sec_pos
                    val_b2 = cn_sec_pos
                    val_b3 = (side + 1) - cn_sec_pos
                    val_b4 = ch_sec_pos

                    for sec, value in (
                            ((sec_a1, sec_b1), (val_a1, val_b1, val_b2)),
                            ((sec_a1, sec_b2), (val_a1, val_b1, val_b2)),
                            ((sec_a1, sec_b2), (val_a1, val_b1, val_b2)),
                            ((sec_a2, sec_b3), (val_a2, val_b2, val_b4)),
                            ((sec_a2, sec_b4), (val_a3, val_b3, val_b1)),
                            ((sec_a1, sec_b3), (val_a3, val_b1, val_b3)),
                            ((sec_a1, sec_b4), (val_a2, val_b2, val_b4)),
                            ((sec_a3, sec_b5), (val_a3, val_b1, val_b2)),
                            ((sec_a3, sec_b6), (val_a2, val_b2, val_b4)),
                            ((sec_a3, sec_b2), (val_a4, val_b4, val_b3)),
                            ((sec_a3, sec_b7), (val_a4, val_b4, val_b3)),
                            ((sec_a2, sec_b2), (val_a4, val_b4, val_b3)),
                            ((sec_a2, sec_b7), (val_a4, val_b4, val_b3))
                    ):
                        s = sec[:: -1 if dp else 1]
                        if s in sections:
                            new_facing = value[0]
                            new_pos = (
                                value[1] + side * (sec[0] - 1),
                                value[2] + side * (sec[1] - 1),
                            )
                            new_pos = new_pos[:: -1 if dp else 1]
                            break
                else:
                    new_pos = (cur[~dp], new) if dp else (new, cur[~dp])
                    new_facing = facing
                if not board[new_pos][0]:
                    break
                cur = new_pos
                facing = new_facing
        else:
            facing = turn(facing, cmd)

    return 1000 * cur[0] + 4 * cur[1] + facing


def main():
    loader = LoaderLib(2022)
    testing = True
    if not testing:
        input_text = loader.get_aoc_input(22)
    else:
        input_text = (Path.cwd() / 'testdata.txt').read_text().strip('\n')
        # input_text = dedent('''\
        # ''').strip('\n')

    map_string, route_string = input_text.split('\n\n')

    map_tile = map_string.splitlines()
    route_path = extract_route_path(route_string)

    loader.print_solution('setup', f'{len(map_tile)} {len(route_path)} ...')
    loader.print_solution(1, part1(map_tile, route_path))
    loader.print_solution(2, part2(map_tile, route_path))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.003224        |        0.003224 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 12 13 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.000983        |        0.004208 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 6032
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.000911        |        0.005118 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 8048
    # --------------------------------------------------------------------------------
