import networkx

DIRECTIONS = {'N': 1,
              'S': -1,
              'W': -1j,
              'E': 1j}


def a_regular_map(inp, part2=False):
    maze = networkx.Graph()
    positions = {0}
    stack = []
    start_loc = {0}
    end_loc = set()

    for character in inp:

        if character in 'NSEW':
            direction = DIRECTIONS[character]
            maze.add_edges_from((p, p + direction) for p in positions)
            positions = {p + direction for p in positions}

        elif character == '|':
            end_loc.update(positions)
            positions = start_loc

        elif character == '(':
            stack.append((start_loc, end_loc))
            start_loc, end_loc = positions, set()

        elif character == ')':
            positions.update(end_loc)
            start_loc, end_loc = stack.pop()

    lengths = networkx.algorithms.shortest_path_length(maze, 0)

    if part2:
        return sum(1 for length in lengths.values() if length >= 1000)
    else:
        return max(lengths.values())


if __name__ == '__main__':
    with open('input.txt') as map_file:
        map_string = map_file.read().splitlines(keepends=False)[0]
        print(f'Day 20, part 1: {a_regular_map(map_string)}')
        print(f'Day 20, part 2: {a_regular_map(map_string, True)}')
        # Day 20, part 1: 4018
        # Day 20, part 2: 8581
