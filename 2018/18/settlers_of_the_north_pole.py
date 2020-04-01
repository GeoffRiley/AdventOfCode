from collections import defaultdict
from typing import List, DefaultDict

SURROUND = (-1 - 1j, -1j, 1 - 1j, -1, 1, -1 + 1j, 1j, 1 + 1j)


def settlers_of_the_north_pole(inp: List[str], timeframe: int = 10) -> int:
    grid = defaultdict(lambda: '.')
    for y, row in enumerate(inp):
        for x, c in enumerate(row):
            grid[x + y * 1j] = c
    ymax = len(inp)
    xmax = len(inp[0])
    history = {}
    state = ''
    for minute in range(timeframe):
        grid = one_generation(grid, xmax, ymax)
        state = str(grid)
        if state in history:
            result = (timeframe - history[state] - 1) % (minute - history[state])
            rept = history[state]
            state = [k for k, v in history.items() if v == result + rept][0]
            break
        history[state] = minute
    return state.count('#') * state.count('|')


def one_generation(grid: DefaultDict[complex, str], xmax: int, ymax: int) -> DefaultDict[complex, str]:
    new_grid = defaultdict(lambda: '.')
    for y in range(ymax):
        for x in range(xmax):
            position = x + y * 1j
            if grid[position] == '.':
                new_grid[position] = '|' if sum(1 for c in SURROUND if grid[position + c] == '|') >= 3 else '.'
            elif grid[position] == '|':
                new_grid[position] = '#' if sum(1 for c in SURROUND if grid[position + c] == '#') >= 3 else grid[
                    position]
            elif grid[position] == '#':
                new_grid[position] = '#' if sum(1 for c in SURROUND if grid[position + c] == '|') >= 1 and sum(
                    1 for c in SURROUND if grid[position + c] == '#') >= 1 else '.'
    return new_grid


if __name__ == '__main__':
    with open('input.txt') as map_file:
        map_strings = map_file.read().splitlines(keepends=False)
        print(f'Day 18, part 1: {settlers_of_the_north_pole(map_strings)}')
        print(f'Day 18, part 2: {settlers_of_the_north_pole(map_strings, 1_000_000_000)}')
        # Day 18, part 1: 535522
        # Day 18, part 2: 210160
