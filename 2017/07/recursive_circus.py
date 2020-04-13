from collections import Counter

import networkx as nx


def recursive_circus(inp, part1=True):
    graph = nx.DiGraph()
    for line in inp:
        under, *over = line.split(' -> ')
        under, mass = under.split()
        graph.add_node(under, mass=int(mass[1:-1]))
        if over:
            over = over[0].split(', ')
            for o in over:
                graph.add_edge(under, o)
    ordered = list(nx.topological_sort(graph))
    if part1:
        return ordered[0]
    else:
        mass = dict()
        bad_child = None
        for node in ordered[::-1]:
            total = graph.nodes[node]['mass']
            child_mass = Counter(mass[child] for child in graph[node])
            good_mass = None
            for child in graph[node]:
                if len(child_mass) > 1 and child_mass[mass[child]] == 1:
                    bad_child = child
                else:
                    good_mass = mass[child]
                total += mass[child]
            if bad_child is not None:
                return graph.nodes[bad_child]['mass'] - (mass[bad_child] - good_mass)
            mass[node] = total


if __name__ == '__main__':
    with open('input.txt') as proc_file:
        process_list = proc_file.read().splitlines(keepends=False)
        print(f'Day 7, part 1: {recursive_circus(process_list)}')
        print(f'Day 7, part 2: {recursive_circus(process_list, False)}')
        # Day 7, part 1: dgoocsw
        # Day 7, part 2: 1275
