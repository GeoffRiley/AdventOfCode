"""
Advent of code 2025
Day 08: Playground
"""

import heapq
from itertools import combinations
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import extract_ints


class UnionFind:
    """Implements the Union-Find (Disjoint Set Union) data structure.

    Maintains a collection of disjoint sets and supports efficient union and find operations. This class is useful for tracking connected components in a set of elements.

    Args:
        n (int): The number of elements to initialize in the structure.

    Attributes:
        parent (list): The parent of each element.
        size (list): The size of each set.
        num_components (int): The current number of disjoint sets.
    """
    __slots__ = ("parent", "size", "num_components")

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n
        self.num_components = n

    def find(self, x: int) -> int:
        """Finds the representative (root) of the set containing x.

        Returns the root of the set that contains the element x, applying path compression for efficiency.

        Args:
            x (int): The element to find the set representative for.

        Returns:
            int: The root of the set containing x.
        """
        path = []
        root = x
        while root != self.parent[root]:
            path.append(root)
            root = self.parent[root]
        for node in path:
            self.parent[node] = root
        return root

    def union(self, x: int, y: int) -> bool:
        """Unites the sets containing x and y, if they are disjoint.

        Merges the sets containing the two elements if they are not already in the same set. Returns True if a union was performed, otherwise returns False.

        Args:
            x (int): The first element.
            y (int): The second element.

        Returns:
            bool: True if the sets were merged, False if they were already in the same set.
        """
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            return self._extracted_from_union_5(root_x, root_y)
        return False

    def _extracted_from_union_5(self, root_x, root_y):
        """Helper method to merge two sets by their roots.

        Combines the sets rooted at root_x and root_y, updating parent and size information. Ensures the larger set remains the root for efficiency.

        Args:
            root_x (int): The root of the first set.
            root_y (int): The root of the second set.

        Returns:
            bool: True after the sets have been merged.
        """
        if self.size[root_x] < self.size[root_y]:
            root_x, root_y = root_y, root_x
        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]
        self.size[root_y] = 0
        self.num_components -= 1
        return True


def get_edges_generator(points):
    """Generates all possible edges between points with their squared Euclidean distances.

    Iterates over all unique pairs of points and yields a tuple containing the squared distance and the indices of the two points. This is useful for constructing edge lists for graph algorithms.

    Args:
        points (list): A list of points, where each point is a tuple of coordinates.

    Yields:
        tuple: A tuple (distance_squared, index1, index2) for each unique pair of points.
    """
    for (u, p1), (v, p2) in combinations(enumerate(points), 2):
        # Squared Euclidean distance avoids sqrt and is faster
        d2 = (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2
        yield d2, u, v


def part1(lines: list[list[int]]) -> int:
    """Solves part 1 of the puzzle by connecting points and calculating the product of the largest parts.

    Connects points using the smallest distances and forms disjoint sets, then computes the product of the sizes of the three largest parts. Returns the resulting product as the solution.

    Args:
        lines (list[list[int]]): A list of points, each represented as a list of integers.

    Returns:
        int: The product of the sizes of the three largest connected parts.
    """
    points = [tuple(l) for l in lines]
    connections_to_make = 1000 if len(lines) > 100 else 10

    # Use nsmallest to avoid sorting O(N^2) edges when we only need the top K.
    edges = heapq.nsmallest(connections_to_make, get_edges_generator(points))

    uf = UnionFind(len(points))
    for _, u, v in edges:
        uf.union(u, v)

    largest_sizes = sorted(uf.size, reverse=True)[:3]
    return largest_sizes[0] * largest_sizes[1] * largest_sizes[2]


def part2(lines: list[list[int]]) -> int:
    """Solves part 2 of the puzzle by connecting all points into a single part.

    Iteratively connects points using the smallest available edges until all points are in one connected part. Returns the product of the first coordinates of the last two points connected.

    Args:
        lines (list[list[int]]): A list of points, each represented as a list of integers.

    Returns:
        int: The product of the first coordinates of the last two points connected.
    """
    points = [tuple(l) for l in lines]

    edges = sorted(get_edges_generator(points))
    uf = UnionFind(len(points))
    last_u, last_v = -1, -1

    for _, u, v in edges:
        if uf.union(u, v):
            last_u, last_v = u, v
            if uf.num_components == 1:
                break

    return points[last_u][0] * points[last_v][0]


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

    # Efficient parsing using extract_ints
    lines = [extract_ints(line) for line in input_text.splitlines()]

    loader.print_solution("setup", f"{len(lines)=} ...")
    loader.print_solution(
        1,
        part1(
            lines,
        ),
    )

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
    #  LAP -> 0.002526        |        0.002526 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : len(lines)=1000 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.267398        |        0.269924 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 80446
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.908722        |        1.178646 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 51294528
    # --------------------------------------------------------------------------------
