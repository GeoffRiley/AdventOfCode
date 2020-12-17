from collections import defaultdict
from itertools import product
from typing import Tuple, Iterator


def neighbors(point: Tuple) -> Iterator[Tuple]:
    for delta in product(range(-1, 2), repeat=len(point)):
        if set(delta) == {0}:
            continue
        yield tuple(c + delta[i] for i, c in enumerate(point))


def do_simulation(grid):
    for generation in range(6):
        new_grid = defaultdict(int)
        check_cells = []
        for point, state in grid.items():
            if state:
                check_cells.extend(list(neighbors(point)))
        for point in check_cells:
            c = sum(grid.get(pos, 0) for pos in neighbors(point))
            if (grid.get(point, 0) and c in (2, 3)) or (not grid.get(point, 0) and c == 3):
                new_grid[point] = 1
        grid = new_grid
    return grid


def conway_cubes_part1(data: str) -> int:
    z = 0
    grid = defaultdict(int)
    grid.update(
        {(x, y, z): int(cell == '#')
         for y, row in enumerate(data.splitlines(keepends=False))
         for x, cell in enumerate(row)})
    grid = do_simulation(grid)
    return sum(grid.values())


def conway_cubes_part2(data: str) -> int:
    z = 0
    w = 0
    grid = defaultdict(int)
    grid.update(
        {(x, y, z, w): int(cell == '#')
         for y, row in enumerate(data.splitlines(keepends=False))
         for x, cell in enumerate(row)})
    grid = do_simulation(grid)
    return sum(grid.values())


if __name__ == '__main__':
    test_text = """.#.
..#
###"""
    assert conway_cubes_part1(test_text) == 112
    assert conway_cubes_part2(test_text) == 848

    with open('input.txt') as in_file:
        in_text = in_file.read()
        part1 = conway_cubes_part1(in_text)
        print(f'Part1: {part1}')
        part2 = conway_cubes_part2(in_text)
        print(f'Part2: {part2}')

    # Part1: 388
    # Part2: 2280
