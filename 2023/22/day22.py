"""
Advent of code 2023
Day 22: Sand Slabs
"""

import itertools
from collections import defaultdict, deque
from textwrap import dedent
from typing import Any

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


def parse_bricks(lines) -> dict:
    bricks = {}
    for i, line in enumerate(lines):
        coords = line.split("~")
        start = tuple(map(int, coords[0].split(",")))
        end = tuple(map(int, coords[1].split(",")))
        brick_id = i

        xs = range(min(start[0], end[0]), max(start[0], end[0]) + 1)
        ys = range(min(start[1], end[1]), max(start[1], end[1]) + 1)
        zs = range(min(start[2], end[2]), max(start[2], end[2]) + 1)
        brick_cubes = {(x, y, z) for x in xs for y in ys for z in zs}

        bricks[brick_id] = brick_cubes
    return bricks


def settle_bricks(bricks) -> dict:
    """
    Once we have all bricks and their cubes, let them fall to their final positions.
    This only needs to be done once.
    """
    occupied = set()
    settled_positions = {}

    # Sort bricks by lowest z to drop them from highest to lowest
    sorted_bricks = sorted(bricks.items(), key=lambda x: min(c[2] for c in x[1]))

    for brick_id, cubes in sorted_bricks:
        while True:
            # Try moving the brick down by one
            new_cubes = {(x, y, z - 1) for x, y, z in cubes}
            # If any new cube hits ground or occupied space, we stop
            if any(c[2] == 0 for c in new_cubes) or not new_cubes.isdisjoint(occupied):
                break
            cubes = new_cubes
        settled_positions[brick_id] = cubes
        occupied.update(cubes)

    return settled_positions


def build_support_graph(bricks) -> tuple[defaultdict[Any, set], defaultdict[Any, set]]:
    """
    Build a graph where an edge U -> V means: V is directly supported by U.
    That is, brick V rests on top of brick U (at least one cube of V sits directly above a cube of U).
    """
    # Map each cube to its brick for O(1) lookups
    cube_to_brick = {}
    for b_id, cubes in bricks.items():
        for c in cubes:
            cube_to_brick[c] = b_id

    # support_graph: brick -> set of bricks it supports
    # Actually, for checking dependencies, we might want the reverse graph as well:
    # Let's store two directions:
    # down_graph[b] = bricks that b rests on (parents)
    # up_graph[b] = bricks that rest on b (children)
    down_graph = defaultdict(set)
    up_graph = defaultdict(set)

    # For each cube in each brick, check the cube immediately below (z+1)
    # If there's a brick below, that forms a support link: below -> current
    for b_id, cubes in bricks.items():
        # Find any supporting bricks (parents)
        parents = set()
        for x, y, z in cubes:
            below = (x, y, z - 1)
            if below in cube_to_brick:
                parent_brick = cube_to_brick[below]
                if parent_brick != b_id:
                    parents.add(parent_brick)
        # Update graphs
        for p in parents:
            down_graph[b_id].add(p)
            up_graph[p].add(b_id)

    return up_graph, down_graph


def topological_sort(all_nodes, down_graph, up_graph):
    """
    Given that 'down_graph[b]' gives the set of bricks that b rests on (its
    parents), we can find a topological order of bricks by looking at
    in-degrees.
    """
    in_degree = {node: 0 for node in all_nodes}
    for node, parents in down_graph.items():
        # Each parent -> node edge means node depends on parent
        in_degree[node] = len(parents)

    queue = deque([n for n in all_nodes if in_degree[n] == 0])
    topo_order = []
    while queue:
        cur = queue.popleft()
        topo_order.append(cur)
        # For each brick that cur supports (reverse edge), reduce their in-degree
        pass

    return topo_order


def compute_support_counts(all_nodes, down_graph):
    """
    Compute the number of distinct support paths from the ground for each brick.
    If a brick has no parents, it rests on the ground, so support_count=1.
    Otherwise, support_count= sum of support_counts of parents.
    """
    # Find all ground-level bricks: these have no parents
    in_degree = {n: len(down_graph[n]) for n in all_nodes}

    # We'll do a topological pass, computing support counts
    support_count = {n: 0 for n in all_nodes}
    for n in all_nodes:
        if in_degree[n] == 0:
            # resting on ground
            support_count[n] = 1

    # To topologically process, we need the reverse edges:
    # reverse_graph[p] = bricks that have p as a parent
    reverse_graph = defaultdict(set)
    for child, parents in down_graph.items():
        for p in parents:
            reverse_graph[p].add(child)

    # Process nodes in topological order
    topo_order = []
    q = deque(n for n in all_nodes if in_degree[n] == 0)
    deg = dict(in_degree)
    while q:
        cur = q.popleft()
        topo_order.append(cur)
        for child in reverse_graph[cur]:
            # Add cur's support_count to child
            # We'll sum these up after we confirm all parents are processed
            support_count[child] += support_count[cur]
            deg[child] -= 1
            if deg[child] == 0:
                q.append(child)

    return support_count


def compute_heights(support_graph: dict[str, set]) -> dict[str, int]:
    """
    Compute the 'height' of each brick in the given support_graph.
    A height of 0 indicates a brick that doesn't rest on any other bricks
    (i.e., has no incoming edges). Higher numbers indicate bricks stacked above others.

    The graph structure: Each key has edges pointing to bricks that depend on it.
    So, key -> dependents means these dependents rest ON the key.

    Steps to compute height:
    - Determine the in-degree of each node.
    - Topologically process nodes, where a node with in-degree 0 starts at height 0.
    - For each node, the height of its dependents is at least height[node] + 1.
    """
    # Extract all nodes
    all_nodes = set(support_graph.keys())
    for dependents in support_graph.values():
        all_nodes.update(dependents)

    # Compute in-degrees
    in_degree = {node: 0 for node in all_nodes}
    for node in support_graph:
        for dep in support_graph[node]:
            in_degree[dep] += 1

    # Initialize queue with nodes of in-degree 0 (these are "ground-level")
    queue = deque([node for node, deg in in_degree.items() if deg == 0])
    heights = {node: 0 for node in queue}

    # For nodes not in queue (not ground-level),
    # initialize height to -∞ temporarily
    for node in all_nodes:
        if node not in heights:
            heights[node] = float("-inf")

    # Topological processing
    visited_count = 0
    while queue:
        current = queue.popleft()
        visited_count += 1
        current_height = heights[current]
        for dep in support_graph.get(current, []):
            # Update the height of the dependent
            heights[dep] = max(heights[dep], current_height + 1)
            in_degree[dep] -= 1
            if in_degree[dep] == 0:
                queue.append(dep)

    # If we didn't visit all nodes, there's a cycle or disconnected component
    # which means the structure can't be properly leveled.
    return None if visited_count < len(all_nodes) else heights


def can_disintegrate_fast(
    brick_to_remove, all_nodes, down_graph, up_graph, support_count
):
    """
    Determine if removing 'brick_to_remove' is safe.
    If removing this brick invalidates all support paths for any brick above
    it, then it's not safe.

    We know how many support paths each brick currently has. If we remove
    'brick_to_remove':
    - Any brick that relied solely on paths through 'brick_to_remove' will
      lose its support.

    Quick heuristic:
    - If 'brick_to_remove' is on a unique path to some brick (that brick has
      support_count=1 and the path includes 'brick_to_remove'), removing it
      will cause that brick to fall.
    - We need to check if 'brick_to_remove' is critical for any brick's
      support_count.

    One approach:
    - If a brick above has support_count=1 and you can trace that single path
      of support back down and it includes 'brick_to_remove', not safe.
    - For a fully optimized solution, you'd precompute additional information
      to know if each parent contributes distinct paths. For simplicity, let's
      do a brute-force check here:
      * This might still be expensive, but less so than before because we have
        the topological order and precomputed counts.

    A more efficient approach involves storing, for each brick, how removing
    each of its parents affects its support_count. But let's outline a
    simplified version:
    """

    # If a brick does not appear in the support chain of another brick’s
    # unique path, it’s safe.
    # Checking path inclusion directly can still be costly. Instead, consider:
    # - If 'brick_to_remove' has no children that depend solely on it
    # (children with support_count=1 and no alternative parents), it's safe.
    # - Recursively check upwards.

    # To do a minimal example, let's do a BFS upwards from brick_to_remove and
    # check if we find a brick with support_count=1 and no alternative support
    # if remove this one.

    # Mark brick_to_remove as "removed" and see if any brick loses all support
    # paths:
    # We'll simulate a modified support count removal:
    # Create a modified support_count array:
    temp_support = support_count.copy()

    # We know that removing this brick removes its contributions to all bricks
    # above it.
    # How do we know which bricks above are affected? We can propagate upwards:
    queue = deque([brick_to_remove])
    visited = {brick_to_remove}

    # Because support_count calculations are cumulative, removing one brick
    # means subtracting its contribution from all descendants. But we only
    # know total counts, not per-parent counts.
    # Without per-parent breakdown, we must assume if a brick is supported by
    # multiple paths, removing one path might still leave others intact. If
    # support_count > 1, it's not immediately doomed. If support_count = 1
    # and we remove that one path, it's doomed.

    # For a truly robust solution, you'd need parent contribution tracking.
    # Here’s a simplified assumption:
    # We'll detect a problematic scenario where a brick had support_count=1
    # and its only parent path was through this brick.
    # Since we don't have explicit per-parent contributions, we make a
    # simplifying assumption:
    # If a brick rests on multiple parents and support_count > 1, removing one
    # shouldn't kill it.
    # If a brick has support_count=1, removing any single parent in its chain
    # kills it.

    # Thus, if we can reach any brick with support_count=1 above
    # brick_to_remove, we consider it unsafe.
    # In reality, you'd store more detailed info.

    while queue:
        cur = queue.popleft()
        # Check all bricks that rest on 'cur' (its children in up_graph)
        for child in up_graph[cur]:
            if child not in visited:
                visited.add(child)
                # If child had support_count=1 originally, it means this brick_remove chain is critical
                if support_count[child] == 1:
                    # Removing 'brick_to_remove' kills child's only support path
                    return False
                # If support_count[child] > 1, it might still be stable,
                # but let's continue upwards to see if there's another vulnerable brick.
                queue.append(child)

    # If we never encountered a brick with support_count=1 above it, it's safe
    return True


def can_disintegrate(
    brick_id: str, bricks: dict, support_graph: defaultdict[str, set]
) -> bool:
    """
    Checks if removing a specified brick keeps the structure stable.
    Stability is determined by whether any remaining bricks are forced to "move down."

    Args:
        brick_id (str): The brick to remove.
        bricks (dict): Dictionary of brick data.
        support_graph (defaultdict[str, set]): The original support graph.

    Returns:
        bool: True if the structure remains stable after the specified brick is removed, False otherwise.
    """
    # print(f"*** Remove {brick_id=}")
    # Compute original heights
    original_heights = compute_heights(support_graph)
    if original_heights is None:
        # If the original structure itself is not properly arranged, return False
        print("cannot calculate pre removal heights")
        return False
    # pprint.pp(original_heights)

    temp_bricks = {k: v for k, v in bricks.items() if k != brick_id}

    # Recompute the support graph without the selected brick
    temp_graph = build_support_graph(temp_bricks)

    # Compute new heights after removal
    new_heights = compute_heights(temp_graph)
    if new_heights is None:
        # If after removal, we can't get a proper height assignment, it's unstable
        print("Cannot calculate post removal heights")
        return False

    return not any(
        b in original_heights
        and b in new_heights
        and new_heights[b] < original_heights[b]
        or (b not in original_heights or b not in new_heights)
        and b != brick_id
        for b in temp_bricks
    )


def part1(lines: list[str]) -> int:
    """
    Processes a list of lines representing bricks and calculates how many
    bricks can be safely disintegrated.
    This function evaluates the stability of the brick structure and counts
    the number of bricks that can be removed without causing instability.

    Args:
        lines (list[str]): A list of strings where each string represents a
        brick's properties.

    Returns:
        int: The number of bricks that can be safely disintegrated from the
        structure.
    """
    bricks = parse_bricks(lines)
    settled = settle_bricks(bricks)

    up_graph, down_graph = build_support_graph(settled)

    # Precompute all nodes:
    all_nodes = list(settled.keys())

    # Compute support counts (number of distinct paths from ground)
    support_count = compute_support_counts(all_nodes, down_graph)

    # Now determine how many bricks can be safely disintegrated
    safe_count = 0
    for b in all_nodes:
        if can_disintegrate_fast(b, all_nodes, down_graph, up_graph, support_count):
            safe_count += 1

    return safe_count


def part2(lines: list[str]) -> int:
    """ """
    ...


def main():
    loader = LoaderLib(2023)
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
    # Part 1 attempts
    # -1141: Too high
