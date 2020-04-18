from collections import defaultdict, namedtuple

Turn = namedtuple('Turn', 'left, right, forward, back')

NORTH = -1j
EAST = +1
SOUTH = +1j
WEST = -1

TURNS = {
    NORTH: Turn(WEST, EAST, NORTH, SOUTH),
    EAST: Turn(NORTH, SOUTH, EAST, WEST),
    SOUTH: Turn(EAST, WEST, SOUTH, NORTH),
    WEST: Turn(SOUTH, NORTH, WEST, EAST)
}

INFECTED = 1
CLEAN = 0
WEAKENED = 2
FLAGGED = 3

FLIP = {
    CLEAN: INFECTED,
    INFECTED: CLEAN,
}

FLIP2 = {
    CLEAN: WEAKENED,
    WEAKENED: INFECTED,
    INFECTED: FLAGGED,
    FLAGGED: CLEAN
}


def sporifica_virus(inp, part1=True):
    grid = generate_grid(inp)
    current_pos = 0 + 0j
    current_direction = NORTH
    infections = 0
    if part1:
        for _ in range(10_000):
            turn = TURNS[current_direction]
            current_direction = turn.right if grid[current_pos] == INFECTED else turn.left
            grid[current_pos] = FLIP[grid[current_pos]]
            infections += grid[current_pos]
            current_pos += current_direction
    else:
        for _ in range(10_000_000):
            turn = TURNS[current_direction]
            here = grid[current_pos]
            current_direction = turn.right if here == INFECTED else turn.left if here == CLEAN else turn.forward if here == WEAKENED else turn.back
            grid[current_pos] = FLIP2[here]
            infections += 1 if grid[current_pos] == INFECTED else 0
            current_pos += current_direction
    return infections


def generate_grid(inp):
    grid = defaultdict(lambda: 0)
    y_offset = len(inp) // 2
    x_offset = len(inp[0]) // 2
    origin_offset = x_offset + y_offset * 1j
    for y, row in enumerate(inp):
        yo = y * 1j - origin_offset
        for x, cell in enumerate(row):
            grid[x + yo] = 1 if cell == '#' else 0
    return grid


if __name__ == '__main__':
    with open('input.txt') as map_file:
        map_area = map_file.read().splitlines(keepends=False)
        print(f'Day 22, part 1: {sporifica_virus(map_area)}')
        print(f'Day 22, part 2: {sporifica_virus(map_area, False)}')
        # Day 22, part 1: 5570
        # Day 22, part 2: 2512022
