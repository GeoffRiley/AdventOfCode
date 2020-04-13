from collections import defaultdict

FUNCTIONS = {
    '<': lambda x, y: x < y,
    '<=': lambda x, y: x <= y,
    '>': lambda x, y: x > y,
    '>=': lambda x, y: x >= y,
    '==': lambda x, y: x == y,
    '!=': lambda x, y: x != y,
    'inc': lambda x, y: x + y,
    'dec': lambda x, y: x - y
}


def i_heard_you_like_registers(inp):
    regs = defaultdict(lambda: 0)
    highest = 0
    for line in inp:
        # o dec -427 if wnh < -1
        target, fn, t_val, _, src, test, s_val = line.split()
        t_val, s_val = int(t_val), int(s_val)
        if FUNCTIONS[test](regs[src], s_val):
            regs[target] = FUNCTIONS[fn](regs[target], t_val)
            highest = max(highest, regs[target])
    return max(regs.values()), highest


if __name__ == '__main__':
    with open('input.txt') as prog_file:
        program = prog_file.read().splitlines(keepends=False)
        result = i_heard_you_like_registers(program)
        print(f'Day 8, part 1: {result[0]}')
        print(f'Day 8, part 2: {result[1]}')
        # Day 8, part 1: 4448
        # Day 8, part 2: 6582
