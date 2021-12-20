"""
Advent of code 2021
Day 20: Trench Map
"""

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


def extract_binary(grid: set, boundary: set, x: int, y: int, background: bool) -> int:
    res = 0
    for oy in (-1, 0, 1):
        for ox in (-1, 0, 1):
            loc = (x + ox, y + oy)
            res += res + (1 if loc in grid or (background and loc not in boundary) else 0)
    return res


def setup_grid(lines):
    grid = set()
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            if ch == '#':
                grid.add((x, y))
    return grid


def process_enhancement(lap, iea, grid):
    min_x = min([p[0] for p in grid])
    min_y = min([p[1] for p in grid])
    max_x = max([p[0] for p in grid])
    max_y = max([p[1] for p in grid])
    boundary = {
        (x, y)
        for x in range(min_x, max_x + 1)
        for y in range(min_y, max_y + 1)
    }
    new_grid = set()
    background_state = (lap & 1) == 1
    for y in range(min_y - 1, max_y + 2):
        for x in range(min_x - 1, max_x + 2):
            ofs = extract_binary(grid, boundary, x, y, background_state)
            if iea[ofs] == '#':
                new_grid.add((x, y))
    grid = new_grid
    return grid


def part1(iea, lines):
    """
    """
    grid = setup_grid(lines)

    for lap in range(2):
        grid = process_enhancement(lap, iea, grid)

    return len(grid)
    # 5571


def part2(iea, lines):
    """
    """
    grid = setup_grid(lines)

    for lap in range(50):
        grid = process_enhancement(lap, iea, grid)

    return len(grid)
    # 17965


def main():
    loader = LoaderLib(2021)
    input_text = loader.get_aoc_input(20)

    # with open('input-variant.txt', 'r') as f:
    #     input_text = f.read()
    #     # part 1 result = 5326

    #     input_text = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#
    #
    # #..#.
    # #....
    # ##..#
    # ..#..
    # ..###"""

    # iea = image enhancement algorithm
    iea, _, *lines = lines_to_list(input_text)

    assert len(iea) == 512
    loader.print_solution('setup', f'{len(lines)} ...')
    loader.print_solution(1, part1(iea, lines))
    loader.print_solution(2, part2(iea, lines))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.003337        |        0.003337 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 100 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.236390        |        0.239728 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 5571
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 13.505283       |       13.745011 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 17965
    # --------------------------------------------------------------------------------
