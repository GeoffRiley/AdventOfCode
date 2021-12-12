"""
Advent of code 2021
Day 12: Passage Pathing
"""

import networkx as nx

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


def walk_graph(graph: nx.Graph, node: str, visited: set) -> int:
    if node == 'end':
        return 1
    if node.islower() and node in visited:
        return 0
    new_visited = visited.copy()
    if node.islower():
        new_visited.add(node)
    return sum(walk_graph(graph, n, new_visited) for n in graph[node])


def walk_graph2(graph: nx.Graph, node: str, visited: set, revisited: bool) -> int:
    if node == 'end':
        return 1
    if node.islower() and node in visited:
        if revisited or node == 'start':
            return 0
        revisited = True
    new_visited = visited.copy()
    if node.islower():
        new_visited.add(node)
    return sum(walk_graph2(graph, n, new_visited, revisited) for n in graph[node])


def part1(g: nx.Graph):
    """
    """
    return walk_graph(g, 'start', set())


def part2(g: nx.Graph):
    """
    """
    return walk_graph2(g, 'start', set(), False)


def main():
    loader = LoaderLib(2021)
    input_text = loader.get_aoc_input(12)

    #     input_text = """dc-end
    # HN-start
    # start-kj
    # dc-start
    # dc-HN
    # LN-dc
    # HN-end
    # kj-sa
    # kj-HN
    # kj-dc"""

    lines = [tuple(line.split('-')) for line in lines_to_list(input_text)]
    g = nx.Graph(lines)

    loader.print_solution('setup', f'{len(lines)} -> graph len({len(g)})...')
    loader.print_solution(1, part1(g))
    loader.print_solution(2, part2(g))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 2.303420        |        2.303420 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 24 -> graph len(12)...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.154901        |        2.458321 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 5212
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 3.797804        |        6.256125 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 134862
    # --------------------------------------------------------------------------------
