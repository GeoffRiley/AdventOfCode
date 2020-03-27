from collections import deque


def subterranean_sustainability_part_1(inp):
    pot_start = 0
    pots = inp[0].split()[2]
    rules = dict(tuple(line.split(' => ')) for line in inp[1:] if len(line) > 0)
    gen = 0
    while gen < 20:
        pot_start, pots = next_gen(pot_start, pots, rules)
        gen += 1
    return calc_pots_value(pot_start, pots)


def subterranean_sustainability_part_2(inp):
    pot_start = 0
    pots = inp[0].split()[2]
    rules = dict(tuple(line.split(' => ')) for line in inp[1:] if len(line) > 0)
    gen = 0
    diffs = deque(maxlen=100)
    last_pots_value = calc_pots_value(pot_start, pots)
    while gen < 1000:
        pot_start, pots = next_gen(pot_start, pots, rules)
        gen += 1
        pots_value = calc_pots_value(pot_start, pots)
        diffs.append(pots_value - last_pots_value)
        last_pots_value = pots_value
    average_diff = sum(diffs) // len(diffs)
    total = (50000000000 - 1000) * average_diff + calc_pots_value(pot_start, pots)
    return total


def next_gen(pot_start, pots, rules):
    if '#' in pots[0:4]:
        pots = '....' + pots
        pot_start -= 4
    if '#' in pots[-6:]:
        pots += '.....'
    new_pots = '..'
    for pos in range(len(pots) - 4):
        match = pots[pos:pos + 5]
        new_pots += rules[match]
    return pot_start, new_pots


def calc_pots_value(pot_start, pots):
    total = 0
    for x, c in enumerate(pots, start=pot_start):
        if c == '#':
            total += x
    return total


if __name__ == '__main__':
    with open('input.txt') as rule_file:
        rule_lines = rule_file.read().splitlines(keepends=False)
        print(f'Pass 12, part 1: {subterranean_sustainability_part_1(rule_lines)}')
        print(f'Pass 12, part 2: {subterranean_sustainability_part_2(rule_lines)}')
        # Pass 12, part 1: 2040
        # Pass 12, part 2: 1700000000011
