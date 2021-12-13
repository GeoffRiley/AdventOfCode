"""
Advent of code 2021
Day 13: Transparent Origami
"""
from typing import List

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list
from aoc.utility import to_list_int


def make_fold(axis: str, pos: str, grid: set) -> set:
    pos = int(pos)
    pos2 = pos * 2
    if axis == 'x':
        # vertical fold
        new_grid = {(x, y) if x < pos else (pos2 - x, y) for x, y in grid}
    else:
        # horizontal fold
        new_grid = {(x, y) if y < pos else (x, pos2 - y) for x, y in grid}
    return new_grid


def part1(dots: List[List[int]], folds: List[List[str]]):
    """
    """
    grid = {(x, y) for x, y in dots}

    axis, pos = folds[0]
    grid = make_fold(axis, pos, grid)

    return len(grid)


def part2(dots: List[List[int]], folds: List[List[str]]):
    """
    """
    grid = {(x, y) for x, y in dots}

    for axis, pos in folds:
        grid = make_fold(axis, pos, grid)

    top_left = min(grid)
    bottom_right = max(grid)
    text_image = []
    for row in range(top_left[1], bottom_right[1] + 1):
        line = ''
        for col in range(top_left[0], bottom_right[0] + 1):
            line += '#' if (col, row) in grid else '.'
        text_image.append(line)
    return '\n' + '\n'.join(text_image)


def main():
    loader = LoaderLib(2021)
    input_text = loader.get_aoc_input(13)

    #     input_text = """6,10
    # 0,14
    # 9,10
    # 0,3
    # 10,4
    # 4,11
    # 6,0
    # 6,12
    # 4,1
    # 0,13
    # 10,12
    # 3,4
    # 3,0
    # 8,4
    # 1,10
    # 2,14
    # 8,10
    # 9,0
    #
    # fold along y=7
    # fold along x=5"""

    dots_t, folds_t = input_text.split('\n\n')
    dots: List[List[int]] = [to_list_int(line) for line in lines_to_list(dots_t)]
    folds: List[List[str]] = [line.lstrip('fold along ').split('=') for line in lines_to_list(folds_t)]

    # assert len(lines) == len(...)
    loader.print_solution('setup', f'{len(dots)} dots and {len(folds)} folds')
    loader.print_solution(1, part1(dots, folds))
    loader.print_solution(2, part2(dots, folds))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.005744        |        0.005744 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 867 dots and 12 folds
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.001154        |        0.006898 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 735
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.002843        |        0.009741 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   :
    # #..#.####.###..####.#..#..##..#..#.####
    # #..#.#....#..#....#.#.#..#..#.#..#....#
    # #..#.###..#..#...#..##...#..#.#..#...#.
    # #..#.#....###...#...#.#..####.#..#..#..
    # #..#.#....#.#..#....#.#..#..#.#..#.#...
    # .##..#....#..#.####.#..#.#..#..##..####
    # --------------------------------------------------------------------------------
