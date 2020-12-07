import re
from typing import Dict

OUTER_CONTAINER = re.compile(r'^(.*) bags? contain (.*)')
INNER_CONTAINER = re.compile(r'(\d+) (.+?) bags?')


def parse_sack_list(data: str) -> Dict[str, Dict[str, int]]:
    sack_list = dict()
    for line in data.splitlines(keepends=False):
        k, v = OUTER_CONTAINER.match(line).groups()
        sack_list[k] = {matches.group(2): int(matches.group(1))
                        for matches in INNER_CONTAINER.finditer(v)}
    return sack_list


def handy_haversacks_part1(data: str) -> int:
    def sack_contains(sack_colour: str) -> str:
        for colour, options in sack_list.items():
            if sack_colour in options:
                yield colour
                yield from sack_contains(colour)

    sack_list = parse_sack_list(data)
    return len(set(colour for colour in sack_contains('shiny gold')))


def handy_haversacks_part2(data: str) -> int:
    def count_sacks(colour: str) -> int:
        return 1 + sum(n * count_sacks(c) for c, n in sack_list[colour].items())

    sack_list = parse_sack_list(data)
    return count_sacks('shiny gold') - 1


if __name__ == '__main__':
    test_text = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""
    test_text1 = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""
    assert handy_haversacks_part1(test_text) == 4

    assert handy_haversacks_part2(test_text) == 32
    assert handy_haversacks_part2(test_text1) == 126

    with open('input.txt') as in_file:
        in_text = in_file.read()
        part1 = handy_haversacks_part1(in_text)
        print(f'Part1: {part1}')
        part2 = handy_haversacks_part2(in_text)
        print(f'Part2: {part2}')

    # Part1: 142
    # Part2: 10219
