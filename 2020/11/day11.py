from typing import Dict

FLOOR = '.'
SEAT = 'L'
OCCUPIED = '#'
NEIGHBOURS = (-1 - 1j, -1 + 0j, -1 + 1j, 0 - 1j, 0 + 1j, 1 - 1j, 1 + 0j, 1 + 1j)


def neighbours_type1(grid: Dict[complex, str], pos: complex) -> int:
    return sum(grid.get(pos + n, SEAT) == OCCUPIED for n in NEIGHBOURS)


def neighbours_type2(grid: Dict[complex, str], pos: complex) -> int:
    total = 0
    for n in NEIGHBOURS:
        p = pos
        status = grid.get(p + n, SEAT)
        while status == FLOOR:
            p += n
            status = grid.get(p + n, SEAT)
        total += 1 if status == OCCUPIED else 0
    return total


def generation(grid: Dict[complex, str], gen_type: int = 1) -> Dict[complex, str]:
    neighbours, neighbours_cut = (neighbours_type1, 4) if gen_type == 1 else (neighbours_type2, 5)
    new_grid = dict()
    for pos, old_value in grid.items():
        neighbour_count = neighbours(grid, pos)
        new_grid[pos] = (FLOOR if old_value == FLOOR else
                         OCCUPIED if old_value == SEAT and neighbour_count == 0 else
                         SEAT if old_value == OCCUPIED and neighbour_count >= neighbours_cut else
                         old_value)
    return new_grid


def seat_count(grid: Dict[complex, str]) -> int:
    return sum(1 for value in grid.values() if value == OCCUPIED)


def seating_system_part1(data: str) -> int:
    grid = {(x + y * 1j): ch for y, row in enumerate(data.splitlines(keepends=False)) for x, ch in enumerate(row)}

    done = False
    gen = 0
    last_seat_count = 0
    while not done:
        new_grid = generation(grid)
        gen += 1
        grid = new_grid
        count = seat_count(grid)
        done = last_seat_count == count
        last_seat_count = count
    return seat_count(grid)


def seating_system_part2(data: str) -> int:
    grid = {(x + y * 1j): ch for y, row in enumerate(data.splitlines(keepends=False)) for x, ch in enumerate(row)}

    done = False
    last_seat_count = 0
    while not done:
        new_grid = generation(grid, 2)
        grid = new_grid
        count = seat_count(grid)
        done = last_seat_count == count
        last_seat_count = count
    return seat_count(grid)


if __name__ == '__main__':
    test_text = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""
    assert seating_system_part1(test_text) == 37
    assert seating_system_part2(test_text) == 26

    with open('input.txt') as in_file:
        in_text = in_file.read()
        part1 = seating_system_part1(in_text)
        print(f'Part1: {part1}')
        part2 = seating_system_part2(in_text)
        print(f'Part2: {part2}')

    # Part1: 2263
    # Part2: 2002
