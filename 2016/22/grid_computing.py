from collections import defaultdict

# No man stands in the same river twice, because it's not the same river and he's not the same man.
from itertools import permutations


def size_to_int(size: str) -> int:
    if size[-1] != 'T':
        raise SyntaxError(f'Bad size descriptor: {size}')
    return int(size[:-1])


def grid_computing(inp):
    grid = defaultdict(lambda: (0, 0))
    for line in inp:
        if line.startswith('/dev'):
            device, _, used, avail, _ = line.split()
            pth, x, y = device.split('-')
            pos = int(x[1:]) + int(y[1:]) * 1j
            grid[pos] = (size_to_int(used), size_to_int(avail))
    viable_count = 0
    for a, b in permutations(grid, 2):
        if grid[a][0] == 0:
            continue
        if grid[a][0] < grid[b][1]:
            viable_count += 1
    return viable_count, grid


if __name__ == '__main__':
    with open('input.txt') as df_file:
        df_list = df_file.read().splitlines(keepends=False)
        viable, grid = grid_computing(df_list)
        print(f'Day 22, part 1: {viable}')
        print('Day 22, part 2: Hand calculated from grid...')
        home = 0j
        target = 0j + 31
        for y in range(31):
            y0 = 1j * y
            line = ''
            for x in range(32):
                pos = x + y0
                c = grid[pos]
                if pos == home:
                    line += 'S '
                elif pos == target:
                    line += 'G '
                elif c[0] == 0:
                    line += '_ '
                elif c[0] > 99:
                    line += '# '
                else:
                    line += '. '
            print(line)
        # Day 22, part 1: 985
        # Day 22, part 2: Hand calculated from grid...
        # S . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . G
        # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # . . . . . . . . . . . . . . . . . . . . . . . . . . # # # # # #
        # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # . . . . . . . . . . . . . . . . . . . . . . . . . . . . _ . . . 3l + 20u + 6r + (5*30)l
        # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . = 29 + 150
        # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . = 179
        # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # Day 22, part 2: 179
