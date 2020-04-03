import operator
import re
from collections import defaultdict
from typing import Dict, Tuple

from z3 import Int, Optimize, If

BOT_LINE = re.compile(r'^pos=<(?P<location>-?\d+,-?\d+,-?\d+)>,\sr=(?P<radius>\d+)$')


def manhatten_distance(point_a, point_b):
    return (
            abs(point_a[0] - point_b[0]) +
            abs(point_a[1] - point_b[1]) +
            abs(point_a[2] - point_b[2])
    )


def zabs(n):
    return If(n >= 0, n, -n)


def experimental_emergency_teleportation(inp, pass1=True):
    points_with_r: Dict[Tuple[int, ...], int] = dict()
    for line in inp:
        match = BOT_LINE.match(line)
        points_with_r[tuple(int(v) for v in match.group('location').split(','))] = int(match.group('radius'))
    if pass1:
        max_p, max_r = max(points_with_r.items(), key=operator.itemgetter(1))
        points = [p for p, r in points_with_r.items() if manhatten_distance(max_p, p) <= max_r]
        return len(points)
    else:
        in_range = defaultdict(int)
        max_r = 0
        max_idx = 0
        for i in range(len(points_with_r)):
            pos, nrange = list(points_with_r.items())[i]
            if nrange > max_r:
                max_r = nrange
                max_idx = i
                for j in range(len(points_with_r)):
                    next_pos, _ = list(points_with_r.items())[i]
                    if manhatten_distance(pos, next_pos) <= max_r:
                        in_range[i] += 1
        (x, y, z) = (Int('x'), Int('y'), Int('z'))
        in_range = [Int(f'in_range_{i}') for i in range(len(points_with_r))]
        range_count = Int('sum')
        o = Optimize()
        for i in range(len(points_with_r)):
            (nx, ny, nz), nrange = list(points_with_r.items())[i]
            o.add(in_range[i] == If(zabs(x - nx) + zabs(y - ny) + zabs(z - nz) <= nrange, 1, 0))
        o.add(range_count == sum(in_range))
        dist_from_origin = Int('dist')
        o.add(dist_from_origin == zabs(x) + zabs(y) + zabs(z))
        h1 = o.maximize(range_count)
        h2 = o.minimize(dist_from_origin)
        print(f'CHECK: {o.check()}')
        print(f'LOW COUNT: {o.lower(h1)}; HIGH COUNT: {o.upper(h1)}')
        print(f'LOW DIST: {o.lower(h2)}; HIGH DIST: {o.upper(h2)}')
        print(f'X: {o.model()[x]}')
        print(f'Y: {o.model()[y]}')
        print(f'Z: {o.model()[z]}')
        return o.lower(h2)


if __name__ == '__main__':
    with open('input.txt') as bot_location_file:
        bot_location_list = bot_location_file.read().splitlines(keepends=False)
        print(f'Day 23, pass 1: {experimental_emergency_teleportation(bot_location_list)}')
        print(f'Day 23, pass 2: {experimental_emergency_teleportation(bot_location_list, False)}')
        # Day 23, pass 1: 399
        # Day 23, pass 2: 81396996
