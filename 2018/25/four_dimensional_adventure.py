import networkx as nx


def manhattan(point, point2):
    return sum(abs(i - j) for i, j in zip(point, point2))


def four_dimensional_adventure(inp):
    points = [tuple(map(int, line.split(','))) for line in inp]
    graph = nx.Graph()
    for point in points:
        for point2 in points:
            if manhattan(point, point2) <= 3:
                graph.add_edge(point, point2)

    return nx.number_connected_components(graph)


if __name__ == '__main__':
    with open('input.txt') as map_file:
        map_locations = map_file.read().splitlines(keepends=False)
        print(f'Day 25, part 1: {four_dimensional_adventure(map_locations)}')
        # Day 25, part 1: 350
