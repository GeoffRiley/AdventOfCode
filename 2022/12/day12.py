"""
Advent of code 2022
Day 12: Hill Climbing Algorithm
"""
from textwrap import dedent
from typing import List, Dict, Tuple

from aoc.loader import LoaderLib
from aoc.search import node_to_path, bfs
from aoc.utility import lines_to_list


def create_grid(lines: List[str]) -> Tuple[Dict[complex, str], int, int, complex, complex]:
    grid = {}
    max_imag = len(lines)
    max_real = len(lines[0])
    for y, line in enumerate(lines):
        complex_offset = 1j * y
        grid.update({x + complex_offset: ch for x, ch in enumerate(line)})
    s_start = [x for x, ch in grid.items() if ch == 'S'][0]
    grid[s_start] = 'a'
    s_end = [x for x, ch in grid.items() if ch == 'E'][0]
    grid[s_end] = 'z'
    return grid, max_real, max_imag, s_start, s_end


def test_end(entry: complex, s_end: complex) -> bool:
    return entry == s_end


def find_successors(entry: complex, grid: Dict[complex, str], max_real: int, max_imag: int) -> List[complex]:
    results = []
    target_value = chr(ord(grid[entry]) + 1)
    if 0 < entry.real and grid[entry - 1] <= target_value:
        results.append(entry - 1)
    if entry.real < max_real - 1 and grid[entry + 1] <= target_value:
        results.append(entry + 1)
    if 0 < entry.imag and grid[entry - 1j] <= target_value:
        results.append(entry - 1j)
    if entry.imag < max_imag - 1 and grid[entry + 1j] <= target_value:
        results.append(entry + 1j)
    return results


def part1(lines: List[str]) -> int:
    """
    """
    grid, max_real, max_imag, s_start, s_end = create_grid(lines)

    short_route = bfs(
        s_start,
        lambda x: test_end(x, s_end),
        lambda x: find_successors(x, grid, max_real, max_imag)
    )

    return len(node_to_path(short_route)) - 1


def part2(lines: List[str]) -> int:
    """
    """
    grid, max_real, max_imag, _, s_end = create_grid(lines)

    all_starts = [x for x, ch in grid.items() if ch == 'a']
    best_routes = []
    for a_route in all_starts:
        short_route = bfs(
            a_route,
            lambda x: test_end(x, s_end),
            lambda x: find_successors(x, grid, max_real, max_imag)
        )
        if short_route is not None:
            best_routes.append(len(node_to_path(short_route)) - 1)

    return min(best_routes)


def main():
    loader = LoaderLib(2022)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(12)
    else:
        # input_text = (Path.cwd() / 'testdata.txt').read_text().strip('\n')
        input_text = dedent('''\
            Sabqponm
            abcryxxl
            accszExk
            acctuvwj
            abdefghi
        ''').strip('\n')

    lines = lines_to_list(input_text)

    loader.print_solution('setup', f'{len(lines)} ...')
    loader.print_solution(1, part1(lines))
    loader.print_solution(2, part2(lines))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.006598        |        0.006598 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 41 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.138794        |        0.145392 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 370
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 110.413874      |      110.559266 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 363
    # --------------------------------------------------------------------------------
