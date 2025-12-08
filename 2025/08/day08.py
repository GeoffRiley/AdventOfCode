"""
Advent of code 2025
Day 08: Playground
"""

from collections import Counter
import math
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import (
    extract_ints,
    lines_to_list,
    to_list_int,
    batched,
    grouped,
    lines_to_list_int,
    pairwise,
    sequence_to_int,
    tee,
    to_list,
)
from aoc.binary_feeder import BinaryFeeder
from aoc.geometry import Point, Point3, Rectangle, Size
from aoc.edge import Edge
from aoc.grid import Grid
from aoc.maths import (
    factorial,
    fibonacci,
    manhattan_distance,
    sign,
)
from aoc.search import (
    astar,
    bfs,
    dfs,
    binary_contains,
    linear_contains,
    Comparable,
    Node,
    PriorityQueue,
    Queue,
    node_to_path,
    Stack,
)


def part1(lines: list[str]) -> int:
    """ """

    connections_to_make = 1000 if len(lines) > 100 else 10
    points = [Point3(x, y, z) for x, y, z in lines]

    def manhattan_3d(p1: Point3, p2: Point3) -> int:
        return abs(p1.x - p2.x) + abs(p1.y - p2.y) + abs(p1.z - p2.z)

    edges = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dist = math.dist(points[i], points[j])
            # dist = manhattan_3d(points[i], points[j])
            edges.append((dist, i, j))
    edges.sort()

    parent = list(range(len(points)))
    size = [1] * len(points)

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: int, y: int) -> None:
        rootX = find(x)
        rootY = find(y)
        if rootX != rootY:
            if size[rootX] < size[rootY]:
                rootX, rootY = rootY, rootX
            parent[rootY] = rootX
            size[rootX] += size[rootY]
            size[rootY] = 0

    for i, (dist, u, v) in enumerate(edges):
        if i == connections_to_make:
            break
        if find(u) != find(v):
            union(u, v)

    largest_sizes = sorted(size)[:-4:-1]
    result = largest_sizes[0] * largest_sizes[1] * largest_sizes[2]
    return result


def part2(lines: list[str]) -> int:
    """ """

    points = [Point3(x, y, z) for x, y, z in lines]

    def manhattan_3d(p1: Point3, p2: Point3) -> int:
        return abs(p1.x - p2.x) + abs(p1.y - p2.y) + abs(p1.z - p2.z)

    edges = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dist = math.dist(points[i], points[j])
            # dist = manhattan_3d(points[i], points[j])
            edges.append((dist, i, j))
    edges.sort()

    parent = list(range(len(points)))
    size = [1] * len(points)

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: int, y: int) -> None:
        rootX = find(x)
        rootY = find(y)
        if rootX != rootY:
            if size[rootX] < size[rootY]:
                rootX, rootY = rootY, rootX
            parent[rootY] = rootX
            size[rootX] += size[rootY]
            size[rootY] = 0

    connections = 0
    for i, (dist, u, v) in enumerate(edges):
        if find(u) != find(v):
            connections += 1
            if connections == len(edges) - 1:
                break
            union(u, v)

    result = points[u].x * points[v].x
    return result


def main():
    loader = LoaderLib(2025)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(8)
    else:
        input_text = dedent(
            """\
                162,817,812
                57,618,57
                906,360,560
                592,479,940
                352,342,300
                466,668,158
                542,29,236
                431,825,988
                739,650,466
                52,470,668
                216,146,977
                819,987,18
                117,168,530
                805,96,715
                346,949,466
                970,615,88
                941,993,340
                862,61,35
                984,92,344
                425,690,689
            """
        ).strip("\n")
    # lines = [extract_ints(param) for param in lines_to_list(input_text)]
    # lines = [lines_to_list(line) for line in input_text.split("\n\n")]
    # lines = lines_to_list(input_text)

    lines = list(map(eval, input_text.splitlines()))

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
