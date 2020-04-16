import sys
from collections import defaultdict

sys.path.insert(0, '../10')
from knot_hash import knot_hash_str

BIT_COUNT = {
    '0': 0,  # 0000
    '1': 1,  # 0001
    '2': 1,  # 0010
    '3': 2,  # 0011
    '4': 1,  # 0100
    '5': 2,  # 0101
    '6': 2,  # 0110
    '7': 3,  # 0111
    '8': 1,  # 1000
    '9': 2,  # 1001
    'a': 2,  # 1010
    'b': 3,  # 1011
    'c': 2,  # 1100
    'd': 3,  # 1101
    'e': 3,  # 1110
    'f': 4,  # 1111
}
BINARY_SEQ = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'a': '1010',
    'b': '1011',
    'c': '1100',
    'd': '1101',
    'e': '1110',
    'f': '1111',
}

knots = dict()


def get_knot(key: str) -> str:
    if key not in knots:
        knots[key] = knot_hash_str(key)
    return knots[key]


def bit_counter(hex_str: str) -> int:
    res = 0
    for digit in hex_str:
        res += BIT_COUNT[digit]
    return res


def disk_defragmentation(inp, pass1=True):
    res = 0
    if pass1:
        for c in range(128):
            res += bit_counter(get_knot(f'{inp}-{c}'))
        return res
    else:
        grid = defaultdict(lambda: 0)
        for c in range(128):
            y = c * 1j
            knot = get_knot(f'{inp}-{c}')
            for x, ch in enumerate(knot):
                nibble_start = x * 4 + y
                b = BINARY_SEQ[ch]
                for bit in range(4):
                    grid[nibble_start + bit] = int(b[bit])
        assert sum(grid.values()) == 8074
        # print_grid(grid)
        res = region_count(grid)
        return res


def print_grid(grid):
    for c in range(128):
        y = c * 1j
        s = ''
        for x in range(128):
            s += '#' if grid[x + y] == 1 else '.'
        print(s)


def region_count(grid):
    res = 0
    for c in range(128):
        y = c * 1j
        for x in range(128):
            pos = x + y
            if grid[pos] == 1:
                clear_region(grid, pos)
                res += 1
    return res


def clear_region(grid, pos):
    if grid[pos] == 1:
        grid[pos] = 0
        clear_region(grid, pos - 1j)
        clear_region(grid, pos - 1)
        clear_region(grid, pos + 1j)
        clear_region(grid, pos + 1)


if __name__ == '__main__':
    input_value = 'jzgqcdpd'
    print(f'Day 14, part 1: {disk_defragmentation(input_value)}')
    print(f'Day 14, part 2: {disk_defragmentation(input_value, False)}')
    # Day 14, part 1: 8074
    # Day 14, part 2: 1212
