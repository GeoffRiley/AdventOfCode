DIRECTIONS = {
    '>': [1, 0],
    '<': [-1, 0],
    '^': [0, 1],
    'v': [0, -1]
}


def houses(delivery_route: str) -> int:
    visited = set()
    pos = [0, 0]
    visited.add(tuple(pos))
    for c in delivery_route:
        pos = [a + b for a, b in zip(pos, DIRECTIONS[c])]
        visited.add(tuple(pos))
    return len(visited)


def robot_santa(delivery_route: str) -> int:
    visited = set()
    pos_a = [0, 0]
    pos_b = [0, 0]
    visited.add(tuple(pos_a))
    for c in delivery_route:
        pos_a = [a + b for a, b in zip(pos_a, DIRECTIONS[c])]
        visited.add(tuple(pos_a))
        pos_a, pos_b = pos_b, pos_a
    return len(visited)


if __name__ == '__main__':
    with open('input') as f:
        route_text = f.read()

    print(f'Part 1: {houses(route_text)}')
    print(f'Part 2: {robot_santa(route_text)}')
