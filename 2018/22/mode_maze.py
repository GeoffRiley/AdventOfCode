from heapq import heapify, heappop, heappush


def erosion(pos, target, depth):
    if pos in erosion.table:
        return erosion.table[pos]
    result = int((geological_index(pos, target, depth) + depth) % 20183)
    erosion.table[pos] = result
    return result


erosion.table = dict()


def geological_index(pos, target, depth):
    if pos in geological_index.table:
        return geological_index.table[pos]
    if pos in [0, target]:
        result = 0
    elif pos.imag == 0:
        result = int(pos.real) * 16807
    elif pos.real == 0:
        result = int(pos.imag) * 48271
    else:
        result = erosion(pos - 1, target, depth) * erosion(pos - 1j, target, depth)
    geological_index.table[pos] = result
    return result


geological_index.table = dict()


def show_grid(target, depth):
    xmax, ymax = int(target.real) + 10, int(target.imag) + 10
    for y in range(ymax + 1):
        line = ''
        for x in range(xmax + 1):
            pos = x + y * 1j
            if pos == 0:
                line += 'M'
            elif pos == target:
                line += 'T'
            else:
                line += {0: '.', 1: '=', 2: '|'}[erosion(pos, target, depth) % 3]
        print(line)


def risk_level(target, depth):
    return sum(int(erosion(x + y * 1j, target, depth)) % 3 for y in range(int(target.imag) + 1) for x in
               range(int(target.real) + 1))


NEITHER = 0
TORCH = 1
CLIMBING = 2


def calculate_quickest_route(target, depth):
    queue = [(0, 0, 0, TORCH)]
    heapify(queue)
    visited = {(0 + 0j, TORCH): 0}
    time = 0

    while True:
        time, x, y, equip = heappop(queue)
        pos = x + y * 1j
        if (pos, equip) == (target, TORCH):
            break
        time += 1
        scan_adjacent_positions(depth, equip, pos, queue, target, time, visited)
        time += 6
        equip = 3 - equip - (erosion(pos, target, depth) % 3)
        if (pos, equip) == (target, TORCH):
            break
        time += 1
        scan_adjacent_positions(depth, equip, pos, queue, target, time, visited)

    return time


def scan_adjacent_positions(depth, equip, pos, queue, target, time, visited):
    for next_pos in [pos + 1, pos - 1, pos + 1j, pos - 1j]:
        if next_pos.real < 0 or next_pos.imag < 0:
            continue
        if erosion(next_pos, target, depth) % 3 == equip:
            continue
        if (next_pos, equip) in visited and visited[(next_pos, equip)] <= time:
            continue
        visited[(next_pos, equip)] = time
        heappush(queue, (time, int(next_pos.real), int(next_pos.imag), equip))


def mode_maze(inp, pass1=True):
    depth = target = 0
    for line in inp:
        if line.startswith('depth: '):
            depth = int(line.split()[1])
        elif line.startswith('target: '):
            target = list(int(i) for i in line.split()[1].split(','))
        else:
            print(f'Unrecognised line "{line}"')
    target = target[0] + target[1] * 1j
    if pass1:
        return risk_level(target, depth)
    else:
        return calculate_quickest_route(target, depth)


if __name__ == '__main__':
    with open('input.txt') as maze_param_file:
        maze_params = maze_param_file.read().splitlines(keepends=False)
        print(f'Day 22, part 1: {mode_maze(maze_params)}')
        print(f'Day 22, part 2: {mode_maze(maze_params, False)}')
        # Day 22, part 1: 9940
        # Day 22, part 2: 944
