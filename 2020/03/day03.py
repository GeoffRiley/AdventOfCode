from functools import reduce
from typing import List

TREE = '#'


def count_tree_hits(hillside: List[str], column_skip: int, rep_len: int) -> int:
    current_column = 0
    tree_count = 0
    for row in hillside:
        current_column = (current_column + column_skip) % rep_len
        tree_count += 1 if row[current_column] == TREE else 0
    return tree_count


def toboggan_trajectory_part1(text: str) -> int:
    hillside = text.splitlines(keepends=False)
    rep_len = len(hillside[0])
    return count_tree_hits(hillside[1:], 3, rep_len)


def toboggan_trajectory_part2(text: str) -> int:
    hillside = text.splitlines(keepends=False)
    rep_len = len(hillside[0])
    check_hills = hillside[1:]
    tree_count = []
    for n in range(4):
        tree_count.append(count_tree_hits(check_hills, n * 2 + 1, rep_len))
    tree_count.append(count_tree_hits(hillside[2::2], 1, rep_len))
    return reduce((lambda x, y: x * y), tree_count)


if __name__ == '__main__':
    example = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""
    assert toboggan_trajectory_part1(example) == 7
    assert toboggan_trajectory_part2(example) == 336

    with open('input.txt') as in_file:
        original = in_file.read()
        part1 = toboggan_trajectory_part1(original)
        print(f'Part1: {part1}')
        part2 = toboggan_trajectory_part2(original)
        print(f'Part2: {part2}')

        # Part1: 191
        # Part2: 1478615040
