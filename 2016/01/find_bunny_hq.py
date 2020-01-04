import operator

DIR = {0: (0, 1), 1: (1, 0), 2: (0, -1), 3: (-1, 0)}


class direction(object):
    def __init__(self):
        self._direction = 0

    def left(self):
        self._direction = (self._direction + 3) % 4

    def right(self):
        self._direction = (self._direction + 1) % 4

    @property
    def move(self):
        return DIR[self._direction]


def how_far_to_bunny(route, part2=False):
    path_history = set()
    path = [v.strip() for v in route.split(',')]
    pos = (0, 0)
    dir = direction()
    for p in path:
        t, d = p[0], int(p[1:])
        if t == 'L':
            dir.left()
        elif t == 'R':
            dir.right()
        else:
            raise ValueError(f'Unrecognised turn command: {t}')
        for _ in range(d):
            if part2 and pos in path_history:
                return abs(pos[0]) + abs(pos[1])
            path_history.add(pos)
            pos = tuple(map(operator.add, pos, dir.move))
    return abs(pos[0]) + abs(pos[1])


if __name__ == '__main__':
    with open('input') as f:
        the_route = f.read()
    print(f'Part 1: {how_far_to_bunny(the_route)}')
    # Part 1: 209
    print(f'Part 2: {how_far_to_bunny(the_route, True)}')
    # Part 2: 136
