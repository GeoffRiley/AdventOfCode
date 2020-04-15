"""

  \ n  /
nw +--+ ne
  /    \
-+      +-
  \    /
sw +--+ se
  / s  \

Turn directions into vectors, single unit and:
"""
DIRECTIONS = {
    'nw': (-1, 0),
    'n': (0, -1),
    'ne': (1, -1),
    'se': (1, 0),
    's': (0, 1),
    'sw': (-1, 1)
}


def hex_ed(inp, pass1=True):
    pos = (0, 0)
    far_away = 0
    for d in inp:
        pos = tuple(i + j for i, j in zip(pos, DIRECTIONS[d]))
        ds = distance_away(pos)
        if ds > far_away:
            far_away = ds
    if pass1:
        return distance_away(pos)
    else:
        return far_away


def distance_away(pos):
    return max(abs(pos[0]), abs(pos[1]), abs(pos[0] + pos[1]))


if __name__ == '__main__':
    with open('input.txt') as directions_file:
        directions_list = directions_file.read().strip().split(',')
        print(f'Day 11, part 1: {hex_ed(directions_list)}')
        print(f'Day 11, part 2: {hex_ed(directions_list, False)}')
        # Day 11, part 1: 747
        # Day 11, part 2: 1544
