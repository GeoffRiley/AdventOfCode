from collections import defaultdict

TURNS = {
    1j: (-1, 1),
    -1j: (1, -1),
    1: (-1j, 1j),
    -1: (1j, -1j)
}


def a_series_of_tubes(inp, part1=True):
    steps = 1
    start = inp[0].index('|') + 0j
    grid = defaultdict(lambda: ' ')
    for y, row in enumerate(inp):
        for x, c in enumerate(row):
            grid[x + y * 1j] = c
    result = ''
    pos = start
    fwd = 1j
    while grid[pos + fwd] != ' ' or grid[pos + TURNS[fwd][0]] != ' ' or grid[pos + TURNS[fwd][1]] != ' ':
        if grid[pos + fwd] != ' ':
            pass
        elif grid[pos + TURNS[fwd][0]] != ' ':
            fwd = TURNS[fwd][0]
        else:
            fwd = TURNS[fwd][1]
        pos += fwd
        steps += 1
        if grid[pos].isalpha():
            result += grid[pos]
    return result, steps


if __name__ == '__main__':
    with open('input.txt') as maze_file:
        maze_grid = maze_file.read().splitlines(keepends=False)
        word, step_count = a_series_of_tubes(maze_grid)
        print(f'Day 19, part 1: {word}')
        print(f'Day 19, part 2: {step_count}')
        # Day 19, part 1: LIWQYKMRP
        # Day 19, part 2: 16764
