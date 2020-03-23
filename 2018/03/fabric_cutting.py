import re

# #1 @ 393,863: 11x29
LINE_RE = re.compile(r'\#(?P<id>\d+) \s @ \s (?P<x>\d+) , (?P<y>\d+) : \s (?P<width>\d+) x (?P<height>\d+)$',
                     re.VERBOSE)


def fabric_cutting_part_1(inp):
    cloth = set()
    duplicates = set()
    for line in inp:
        res = LINE_RE.match(line)
        if res is None:
            print('Whoops... incorrectly formatted cutting entry.')
        p_x = int(res.group('x'))
        p_y = int(res.group('y'))
        p_width = int(res.group('width'))
        p_height = int(res.group('height'))
        for x in range(p_x, p_x + p_width):
            for y in range(p_y, p_y + p_height):
                if (x, y) in cloth:
                    duplicates.add((x, y))
                else:
                    cloth.add((x, y))
    return len(duplicates)


def fabric_cutting_part_2(inp):
    cloth = dict()
    all_ids = set()
    duplicate_ids = set()
    for line in inp:
        res = LINE_RE.match(line)
        if res is None:
            print('Whoops... incorrectly formatted cutting entry.')
        p_id = int(res.group('id'))
        all_ids.add(p_id)
        p_x = int(res.group('x'))
        p_y = int(res.group('y'))
        p_width = int(res.group('width'))
        p_height = int(res.group('height'))
        for x in range(p_x, p_x + p_width):
            for y in range(p_y, p_y + p_height):
                if (x, y) in cloth.keys():
                    duplicate_ids.add(p_id)
                    duplicate_ids.add(cloth[(x, y)])
                else:
                    cloth[(x, y)] = p_id
    return all_ids - duplicate_ids


if __name__ == '__main__':
    with open('input.txt') as cutting_list:
        cuttings = cutting_list.read().splitlines(keepends=False)
        print(f'Day 3, part 1: {fabric_cutting_part_1(cuttings)}')
        print(f'Day 3, part 2: {fabric_cutting_part_2(cuttings)}')
        # Day 3, part 1: 98005
        # Day 3, part 2: {331}
