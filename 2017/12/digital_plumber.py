import networkx as nx


def digital_plumber(inp):
    graph = nx.Graph()
    for line in inp:
        left, right = line.split(' <-> ')
        left = int(left)
        for r in map(int, right.split(', ')):
            graph.add_edge(left, r)
    return len(nx.components.node_connected_component(graph, 0)), len(list(nx.connected_components(graph)))


if __name__ == '__main__':
    with open('input.txt') as com_link_file:
        com_links = com_link_file.read().splitlines(keepends=False)
        plumber = digital_plumber(com_links)
        print(f'Day 12, pass 1: {plumber[0]}')
        print(f'Day 12, pass 2: {plumber[1]}')
        # Day 12, pass 1: 130
        # Day 12, pass 2: 189
