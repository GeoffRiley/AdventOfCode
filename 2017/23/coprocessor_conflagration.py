from collections import defaultdict


def coprocessor_conflagration(inp, part1=True):
    registers = defaultdict(lambda: 0)
    if not part1:
        registers['a'] = 1

    def reg_or_val(s: str) -> int:
        if len(s) == 1 and s.isalpha():
            return registers[s]
        else:
            return int(s)

    if part1:
        ip = 0
        mul_count = 0
        while 0 <= ip < len(inp):
            line = inp[ip]
            mnemonic, *params = line.split()
            if mnemonic == 'set':
                registers[params[0]] = reg_or_val(params[1])
            elif mnemonic == 'sub':
                registers[params[0]] -= reg_or_val(params[1])
            elif mnemonic == 'mul':
                registers[params[0]] *= reg_or_val(params[1])
                mul_count += 1
            elif mnemonic == 'jnz':
                if reg_or_val(params[0]) != 0:
                    ip += reg_or_val(params[1])
                    continue
            else:
                print(f'Bad mnemonic {mnemonic} at {ip}')
            ip += 1
        return mul_count

    b = 93 * 100 + 100000
    c = b + 17000
    h = 0
    for b in range(b, c + 1, 17):
        for d in range(2, b):
            if b % d == 0:
                h += 1
                break
    return h


if __name__ == '__main__':
    with open('input.txt') as prog_file:
        prog_lines = prog_file.read().splitlines(keepends=False)
        print(f'Day 23, part 1: {coprocessor_conflagration(prog_lines)}')
        print(f'Day 23, part 2: {coprocessor_conflagration(prog_lines, False)}')
        # Day 23, part 1: 8281
        # Day 23, part 2: 911
