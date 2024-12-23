"""
Advent of code 2024
Day 23: LAN Party
"""

from textwrap import dedent
from numpy import sort

import networkx as nx

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


def part1(graph: nx.Graph) -> int:
    """ """
    triangles = [
        clique for clique in nx.enumerate_all_cliques(graph) if len(clique) == 3
    ]
    triples = [
        tuple(sorted(clique))
        for clique in triangles
        if any(node.startswith("t") for node in clique)
    ]
    good_triples = list(set(triples))
    return len(good_triples)


def part2(graph: nx.Graph) -> int:
    """ """
    big_cliques = [
        (len(clique), clique)
        for clique in nx.enumerate_all_cliques(graph)
        if len(clique) > 3
    ]
    max_clique = max(big_cliques)
    return ",".join(sort(max_clique[1]))


def main():
    loader = LoaderLib(2024)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(23)
    else:
        input_text = dedent(
            """\
                kh-tc
                qp-kh
                de-cg
                ka-co
                yn-aq
                qp-ub
                cg-tb
                vc-aq
                tb-ka
                wh-tc
                yn-cg
                kh-ub
                ta-co
                de-co
                tc-td
                tb-wq
                wh-td
                ta-ka
                td-qp
                aq-cg
                wq-ub
                ub-vc
                de-ta
                wq-aq
                wq-vc
                wh-yn
                ka-de
                kh-ta
                co-tc
                wh-qp
                tb-vc
                td-yn
            """
        ).strip("\n")
    # lines = [
    #     (extract_ints(param)) for param in [line for line in lines_to_list(input_text)]
    # ]
    # lines = [lines_to_list(line) for line in input_text.split("\n\n")]
    lines = lines_to_list(input_text)
    graph = nx.Graph()
    for line in lines:
        a, b = line.split("-")
        graph.add_edge(a, b)

    loader.print_solution("setup", f"{len(lines)=} ...")
    loader.print_solution(
        1,
        part1(
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
            graph,
        ),
    )


if __name__ == "__main__":
    main()
    # --
    # --------------------------------------------------------------------------------
    # LAP -> 0.002563        |        0.002563 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : len(lines)=3380 ...
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.418463        |        0.421025 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 1046
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.626610        |        1.047636 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 2   : de,id,ke,ls,po,sn,tf,tl,tm,uj,un,xw,yz
    # --------------------------------------------------------------------------------
