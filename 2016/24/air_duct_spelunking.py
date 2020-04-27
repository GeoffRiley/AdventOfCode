from collections import defaultdict
from itertools import permutations

import networkx as nx


def air_duct_spelunking(inp, part1=True):
    max_y = len(inp)
    max_x = max(len(line) for line in inp)
    grid = defaultdict(lambda: '#')
    numbers = defaultdict(lambda: '')
    route_list = defaultdict(lambda: 0)
    graph = nx.Graph()
    for y, row in enumerate(inp):
        yo = 1j * y
        for x, ch in enumerate(row):
            grid[x + yo] = ch
    for y in range(max_y):
        yo = 1j * y
        for x in range(max_x):
            if grid[x + yo] == '#':
                continue
            ch = grid[x + yo]
            node_address = str(x + yo)
            if ch.isdigit():
                graph.add_node(node_address, num=int(ch))
                numbers[ch] = node_address
            else:
                graph.add_node(node_address)
            for offset in [1j, 1, -1j, -1]:
                if grid[x + yo + offset] != '#':
                    graph.add_edge(node_address, str(x + yo + offset))
    # find shortest path
    short_route = 1e9
    for route in permutations([n for n in numbers.keys() if n > '0']):
        path = 0
        if part1:
            r = ['0'] + list(route)
        else:
            r = ['0'] + list(route) + ['0']
        for u, v in zip(r[:-1], r[1:]):
            if route_list[(u, v)] == 0:
                route_list[(u, v)] = nx.shortest_path_length(graph, numbers[u], numbers[v])
            path += route_list[(u, v)]
        if short_route > path:
            short_route = path
    return short_route


if __name__ == '__main__':
    with open('input.txt') as cave_file:
        cave_lines = cave_file.read().splitlines(keepends=False)
        print(f'Day 24, part 1: {air_duct_spelunking(cave_lines)}')
        print(f'Day 24, part 2: {air_duct_spelunking(cave_lines, False)}')
        # Day 24, part 1: 518
        # Day 24, part 2: 716
