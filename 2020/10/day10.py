from collections import defaultdict
from typing import List


def create_adapter_list(data: str) -> List[int]:
    adapter_list = list(map(int, data.splitlines(keepends=False)))
    adapters = list(sorted(adapter_list + [0, max(adapter_list) + 3]))
    return adapters


def adapter_array_part1(data: str) -> int:
    adapters = create_adapter_list(data)
    gaps = {1: 0, 3: 0}
    for x, y in zip(adapters[:-1], adapters[1:]):
        gaps[y - x] += 1

    return gaps[1] * gaps[3]


def adapter_array_part2(data: str) -> int:
    adapters = create_adapter_list(data)
    routes = defaultdict(int)
    routes[0] = 1
    for place in adapters[1:]:
        routes[place] = routes[place - 3] + routes[place - 2] + routes[place - 1]

    return routes[max(adapters)]


if __name__ == '__main__':
    test_text = """16
10
15
5
1
11
7
19
6
12
4"""
    test_text2 = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""
    assert adapter_array_part1(test_text) == 7 * 5
    assert adapter_array_part1(test_text2) == 22 * 10
    assert adapter_array_part2(test_text) == 8
    assert adapter_array_part2(test_text2) == 19208

    with open('input.txt') as in_file:
        in_text = in_file.read()
        part1 = adapter_array_part1(in_text)
        print(f'Part1: {part1}')
        part2 = adapter_array_part2(in_text)
        print(f'Part2: {part2}')

    # Part1: 1856
    # Part2: 2314037239808
