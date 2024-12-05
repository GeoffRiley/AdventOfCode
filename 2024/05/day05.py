"""
Advent of code 2024
Day 05: Print Queue
"""

from collections import defaultdict
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import extract_ints, lines_to_list


def is_valid_update(update, graph):
    # Create a reverse mapping of page -> index for quick lookup
    page_to_index = {page: i for i, page in enumerate(update)}

    for x in graph:
        for y in graph[x]:
            # Check if both x and y are in the update and that x appears before y
            if x in page_to_index and y in page_to_index:
                if page_to_index[x] > page_to_index[y]:
                    return False
    return True


def middle_num(arr: list[int]) -> int:
    l = len(arr)
    return arr[l // 2]


def topological_sort(update, graph):
    # Restrict graph to only nodes in the update
    restricted_graph = {node: set(edges) & set(update)
                        for node, edges in graph.items() if node in update}
    indegree = {node: 0 for node in update}

    for node, edges in restricted_graph.items():
        for edge in edges:
            indegree[edge] += 1

    # Nodes with no incoming edges
    queue = [node for node in update if indegree[node] == 0]
    sorted_order = []

    while queue:
        current = queue.pop(0)
        sorted_order.append(current)
        for neighbor in restricted_graph.get(current, []):
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    return sorted_order


def part1(updates: list[int], graph: dict) -> int:
    """ """
    middle_pages = []
    for update in updates:
        middle_pages.append(middle_num(update))

    return sum(middle_pages)


def part2(updates: list[int], graph: dict) -> int:
    """ """
    middle_pages = []
    for update in updates:
        fixed_update = topological_sort(update, graph)
        middle_pages.append(middle_num(fixed_update))

    return sum(middle_pages)


def main():
    loader = LoaderLib(2024)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(5)
    else:
        input_text = dedent(
            """\
                47|53
                97|13
                97|61
                97|47
                75|29
                61|13
                75|53
                29|13
                97|29
                53|29
                61|53
                97|53
                61|29
                47|13
                75|47
                97|75
                47|61
                75|61
                47|29
                75|13
                53|13

                75,47,61,53,29
                97,61,53,29,13
                75,29,13
                75,97,47,61,53
                61,13,29
                97,13,75,29,47
            """
        ).strip("\n")
    # lines = [
    #     (extract_ints(param)) for param in [line for line in lines_to_list(input_text)]
    # ]
    lines = [lines_to_list(line) for line in input_text.split("\n\n")]
    # lines = lines_to_list(input_text)

    # Sort out the valid and invalid rules here to pass to the individual
    # routines doing the final analysis. 
    rules, updates = lines
    graph = defaultdict(set)
    for rule in rules:
        x, y = map(int, rule.split("|"))
        graph[x].add(y)
    updates = [extract_ints(u) for u in updates]
    valid_updates = []
    invalid_updates = []
    for update in updates:
        if is_valid_update(update, graph):
            valid_updates.append(update)
        else:
            invalid_updates.append(update)

    loader.print_solution(
        "setup", f"{len(graph)=} {len(valid_updates)=} {len(invalid_updates)=} ...")
    loader.print_solution(
        1,
        part1(
            valid_updates,
            graph,
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
            invalid_updates,
            graph,
        ),
    )


if __name__ == "__main__":
    main()
    # --
    # --------------------------------------------------------------------------------
    # LAP -> 0.007422        |        0.007422 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : len(graph)=49 len(valid_updates)=127 len(invalid_updates)=74 ...
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.000106        |        0.007528 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 7198
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.002536        |        0.010064 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 2   : 4230
    # --------------------------------------------------------------------------------

