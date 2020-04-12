from itertools import product


def corruption_checksum(inp, part1=True):
    result = 0
    for line in inp:
        line = list(map(int, line.split()))
        if part1:
            result += max(line) - min(line)
        else:
            for x, y in product(line, repeat=2):
                if x != y and x % y == 0:
                    result += x // y
                    break
    return result


if __name__ == '__main__':
    with open('input.txt') as check_file:
        checksums = check_file.read().splitlines(keepends=False)
        print(f'Day 2, part 1: {corruption_checksum(checksums)}')
        print(f'Day 2, part 2: {corruption_checksum(checksums, False)}')
        # Day 2, part 1: 58975
        # Day 2, part 2: 308
