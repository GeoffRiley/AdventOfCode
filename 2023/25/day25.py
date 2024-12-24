"""
Advent of code 2023
Day 25: Snowverload
"""

from collections import Counter
from functools import lru_cache
from itertools import combinations
import random
from textwrap import dedent
import networkx as nx

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list, pairwise


def part1(lines: list[str]) -> int:
    """ """

    @lru_cache(maxsize=None)
    def d1(node):
        return nx.descendants_at_distance(graph, node, 1)

    components = []
    for line in lines:
        node, children = line.split(": ")
        components.append((node, children.split()))
    graph = nx.Graph()
    for node, children in components:
        for child in children:
            graph.add_edge(node, child)
    nodes = list(graph.nodes)
    cut_candidates = {
        frozenset((a, b))
        for (a, b) in combinations(graph, 2)
        if b in d1(a) and not (d1(a) & d1(b))
    }
    c = Counter()
    for _ in range(1000):
        for edge in pairwise(nx.shortest_path(graph, *random.choices(nodes, k=2))):
            edgefs = frozenset(edge)
            if edgefs in cut_candidates:
                c[edgefs] += 1
    graph1 = graph.copy()
    graph1.remove_edges_from(tuple(edgefs) for (edgefs, count) in c.most_common(3))
    cc = list(nx.connected_components(graph1))
    if len(cc) == 2:
        return len(cc[0]) * len(cc[1])
    raise ValueError("nope")


def part2(lines: list[str]) -> int:
    """ """
    ...


def main():
    loader = LoaderLib(2023)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(25)
    else:
        input_text = dedent(
            """\
                jqt: rhn xhk nvd
                rsh: frs pzl lsr
                xhk: hfx
                cmg: qnr nvd lhk bvb
                rhn: xhk bvb hfx
                bvb: xhk hfx
                pzl: lsr hfx nvd
                qnr: nvd
                ntq: jqt hfx bvb xhk
                nvd: lhk
                lsr: lhk
                rzs: qnr cmg lsr rsh
                frs: qnr lhk lsr
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
    # --------------------------------------------------------------------------------
    # LAP -> 0.000481        |        0.000481 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : len(lines)=1211 ...
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.167869        |        0.168350 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 552695
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.000053        |        0.168403 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 2   : None
    # --------------------------------------------------------------------------------
