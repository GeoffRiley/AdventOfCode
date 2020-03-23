from collections import Counter


def boxscan_part_1(inp):
    count2 = count3 = 0
    for line in inp:
        tmp = Counter(line)
        if 2 in tmp.values():
            count2 += 1
        if 3 in tmp.values():
            count3 += 1
    return count3 * count2


def boxscan_part_2(inp):
    for line in inp:
        for line2 in inp:
            diffs = -1
            for c, (a, b) in enumerate(zip(line, line2)):
                if a != b:
                    if diffs > -1:
                        diffs = -1
                        break
                    diffs = c
            if diffs > -1:
                print(f'Box 1: {line}\nBox 2: {line2}')
                return line[:diffs] + line[diffs + 1:]
    print('Failed to find similar boxes')


if __name__ == '__main__':
    with open('input.txt') as boxlist:
        box_strings = boxlist.read().splitlines(keepends=False)
        print(f'Day 2, part 1: {boxscan_part_1(box_strings)}')
        print(f'Day 2, part 2: {boxscan_part_2(box_strings)}')
        # Day 2, part 1: 7163
        # Box 1: ighfbbyijnoumxjlxevacpwqtr
        # Box 2: ighfbsyijnoumxjlxevacpwqtr
        # Day 2, part 2: ighfbyijnoumxjlxevacpwqtr
