from itertools import permutations


def expense_report_part1(text: str) -> int:
    lines = map(int, text.splitlines(keepends=False))
    for a, b in permutations(lines, 2):
        if a + b == 2020:
            return a * b
    raise ValueError('No suitable values found.')


def expense_report_part2(text: str) -> int:
    lines = map(int, text.splitlines(keepends=False))
    for a, b, c in permutations(lines, 3):
        if a + b + c == 2020:
            return a * b * c
    raise ValueError('No suitable values found.')


if __name__ == '__main__':
    test_text = """1721
979
366
299
675
1456"""
    assert expense_report_part1(test_text) == 514579
    assert expense_report_part2(test_text) == 241861950

    with open('input.txt') as in_file:
        in_text = in_file.read()
        part1 = expense_report_part1(in_text)
        print(f'Part1: {part1}')
        part2 = expense_report_part2(in_text)
        print(f'Part2: {part2}')

        # Part1: 928896
        # Part2: 295668576
