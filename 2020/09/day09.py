from itertools import permutations


def encoding_error_part1(data: str, preable: int = 25) -> int:
    lst = list(map(int, data.splitlines(keepends=False)))

    place = preable
    while place < len(lst):
        if not any(x + y == lst[place] for x, y in permutations(lst[place - preable:place], 2)):
            return lst[place]
        place += 1
    raise ValueError('No bad value found')


def encoding_error_part2(data: str, target: int) -> int:
    lst = list(map(int, data.splitlines(keepends=False)))

    place = [0, 0]
    acc = 0
    while place[0] < len(lst):
        while place[1] < len(lst):
            acc += lst[place[1]]
            place[1] += 1
            while acc > target:
                acc -= lst[place[0]]
                place[0] += 1
            if acc == target:
                return min(lst[place[0]:place[1]]) + max(lst[place[0]:place[1]])


if __name__ == '__main__':
    test_text = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""
    assert encoding_error_part1(test_text, preable=5) == 127
    assert encoding_error_part2(test_text, 127) == 62

    with open('input.txt') as in_file:
        in_text = in_file.read()
        part1 = encoding_error_part1(in_text)
        print(f'Part1: {part1}')
        part2 = encoding_error_part2(in_text, part1)
        print(f'Part2: {part2}')

    # Part1: 756008079
