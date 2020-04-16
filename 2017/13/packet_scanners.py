def packet_scanners(inp, delay=0):
    result = 0
    caught = False
    for depth, rng in inp.items():
        if (depth + delay) % (rng * 2 - 2) == 0:
            result += rng * depth
            caught = True
            if delay > 0:
                break
    return result, caught


def chop_to_dict(lines):
    res = dict()
    for line in lines:
        k, v = map(int, line.split(': '))
        res[k] = v
    return res


if __name__ == '__main__':
    eg = chop_to_dict('''0: 3
1: 2
4: 4
6: 4'''.splitlines(keepends=False))
    assert packet_scanners(eg) == (24, True)
    with open('input.txt') as scanner_file:
        scanner_list = chop_to_dict(scanner_file.read().splitlines(keepends=False))
        print(f'Day 13, part 1: {packet_scanners(scanner_list)[0]}')
        delay_value = 1
        while packet_scanners(scanner_list, delay_value)[1]:
            delay_value += 1
        print(f'Day 13, part 2: {delay_value}')
        # Day 13, part 1: 2164
        # Day 13, part 2: 3861798
