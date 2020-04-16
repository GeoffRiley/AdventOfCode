def dueling_generators(inp, part1=True):
    multipliers = {'A': 16807, 'B': 48271}
    divisor = 2147483647
    generators = dict()
    for line in inp:
        words = line.split()
        generators[words[1]] = int(words[-1])
    assert len(generators) == 2
    judge_count = 0
    if part1:
        for c in range(40_000_000):
            for gen in generators.keys():
                generators[gen] = generators[gen] * multipliers[gen] % divisor
            if generators['A'] & 0xFFFF == generators['B'] & 0xFFFF:
                judge_count += 1
    else:
        gen_a = make_gen(generators['A'], multipliers['A'], divisor, 4 - 1)
        gen_b = make_gen(generators['B'], multipliers['B'], divisor, 8 - 1)
        for c in range(5_000_000):
            if next(gen_a) & 0xFFFF == next(gen_b) & 0xFFFF:
                judge_count += 1
    return judge_count


def make_gen(start_val, multiplier, divisor, mask):
    while True:
        start_val = start_val * multiplier % divisor
        if start_val & mask == 0:
            yield start_val


if __name__ == '__main__':
    with open('input.txt') as gen_file:
        gen_settings = gen_file.read().splitlines(keepends=False)
        print(f'Day 15, part 1: {dueling_generators(gen_settings)}')
        print(f'Day 15, part 2: {dueling_generators(gen_settings, False)}')
        # Day 15, part 1: 600
        # Day 15, part 2: 313
