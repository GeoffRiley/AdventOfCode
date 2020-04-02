def disassemble_script(inp, ip_reg):
    r_names = ['A', 'B', 'C', 'D', 'E', 'F']
    r_names[ip_reg] = 'IP'
    for n, line in enumerate(inp):
        op, *params = line.split()
        a, b, c = map(int, params)
        print(f'{n:>2}: ', end='')
        if op == 'addr':
            print(f'{op} {r_names[a]} + {r_names[b]} -> {r_names[c]}')
        elif op == 'addi':
            print(f'{op} {r_names[a]} + {b} -> {r_names[c]}')
        elif op == 'mulr':
            print(f'{op} {r_names[a]} * {r_names[b]} -> {r_names[c]}')
        elif op == 'muli':
            print(f'{op} {r_names[a]} * {b} -> {r_names[c]}')
        elif op == 'banr':
            print(f'{op} {r_names[a]} & {r_names[b]} -> {r_names[c]}')
        elif op == 'bani':
            print(f'{op} {r_names[a]} & {b} -> {r_names[c]}')
        elif op == 'borr':
            print(f'{op} {r_names[a]} | {r_names[b]} -> {r_names[c]}')
        elif op == 'bori':
            print(f'{op} {r_names[a]} | {b} -> {r_names[c]}')
        elif op == 'setr':
            print(f'{op} {r_names[a]} -> {r_names[c]}')
        elif op == 'seti':
            print(f'{op} {a} -> {r_names[c]}')
        elif op == 'gtir':
            print(f'{op} {a} > {r_names[b]} -> {r_names[c]}')
        elif op == 'gtri':
            print(f'{op} {r_names[a]} > {b} -> {r_names[c]}')
        elif op == 'gtrr':
            print(f'{op} {r_names[a]} > {r_names[b]} -> {r_names[c]}')
        elif op == 'eqir':
            print(f'{op} {a} == {r_names[b]} -> {r_names[c]}')
        elif op == 'eqri':
            print(f'{op} {r_names[a]} == {b} -> {r_names[c]}')
        elif op == 'eqrr':
            print(f'{op} {r_names[a]} == {r_names[b]} -> {r_names[c]}')


DEBUG = False


def bug(s: str, **kwds):
    if DEBUG:
        print(s, *kwds)


def run_script(inp, ip_reg, pass1=True):
    registers = [0, 0, 0, 0, 0, 0]
    r_names = ['A', 'B', 'C', 'D', 'E', 'F']
    r_names[ip_reg] = 'IP'
    last_unique = 1e600
    history = set()

    while 0 <= registers[ip_reg] <= len(inp):
        if registers[ip_reg] == 17:
            bug(f'L16: [{" ".join([f"{n}:{r:<3}" for r, n in zip(registers, r_names)]):^30}]')
            registers[1] //= 256
            registers[2] = 1
            registers[3] = registers[1]
            registers[ip_reg] = 8
            bug(f'L26: [{" ".join([f"{n}:{r:<3}" for r, n in zip(registers, r_names)]):^30}]')
        if registers[ip_reg] == 27:
            bug(f'L26: [{" ".join([f"{n}:{r:<3}" for r, n in zip(registers, r_names)]):^30}]')
        if registers[ip_reg] == 28:
            bug(f'L27: [{" ".join([f"{n}:{r:<3}" for r, n in zip(registers, r_names)]):^30}]')
            f_reg = registers[5]
            if pass1:
                return f_reg
            else:
                if f_reg in history:
                    return last_unique
                history.add(f_reg)
                last_unique = f_reg
        line = inp[registers[ip_reg]]
        bug(f'[{" ".join([f"{n}:{r:<3}" for r, n in zip(registers, r_names)]):^30}] : ', end='')
        op, *params = line.split()
        a, b, c = map(int, params)
        if op == 'addr':
            registers[c] = registers[a] + registers[b]
            bug(f'{op} {r_names[a]} + {r_names[b]} -> {r_names[c]} [{registers[c]}]')
        elif op == 'addi':
            registers[c] = registers[a] + b
            bug(f'{op} {r_names[a]} + {b} -> {r_names[c]} [{registers[c]}]')
        elif op == 'mulr':
            registers[c] = registers[a] * registers[b]
            bug(f'{op} {r_names[a]} * {r_names[b]} -> {r_names[c]} [{registers[c]}]')
        elif op == 'muli':
            registers[c] = registers[a] * b
            bug(f'{op} {r_names[a]} * {b} -> {r_names[c]} [{registers[c]}]')
        elif op == 'banr':
            registers[c] = registers[a] & registers[b]
            bug(f'{op} {r_names[a]} & {r_names[b]} -> {r_names[c]} [{registers[c]}]')
        elif op == 'bani':
            registers[c] = registers[a] & b
            bug(f'{op} {r_names[a]} & {b} -> {r_names[c]} [{registers[c]}]')
        elif op == 'borr':
            registers[c] = registers[a] | registers[b]
            bug(f'{op} {r_names[a]} | {r_names[b]} -> {r_names[c]} [{registers[c]}]')
        elif op == 'bori':
            registers[c] = registers[a] | b
            bug(f'{op} {r_names[a]} | {b} -> {r_names[c]} [{registers[c]}]')
        elif op == 'setr':
            registers[c] = registers[a]
            bug(f'{op} {r_names[a]} -> {r_names[c]} [{registers[c]}]')
        elif op == 'seti':
            registers[c] = a
            bug(f'{op} {a} -> {r_names[c]} [{registers[c]}]')
        elif op == 'gtir':
            registers[c] = 1 if a > registers[b] else 0
            bug(f'{op} {a} > {r_names[b]} -> {r_names[c]} [{registers[c]}]')
        elif op == 'gtri':
            registers[c] = 1 if registers[a] > b else 0
            bug(f'{op} {r_names[a]} > {b} -> {r_names[c]} [{registers[c]}]')
        elif op == 'gtrr':
            registers[c] = 1 if registers[a] > registers[b] else 0
            bug(f'{op} {r_names[a]} > {r_names[b]} -> {r_names[c]} [{registers[c]}]')
        elif op == 'eqir':
            registers[c] = 1 if a == registers[b] else 0
            bug(f'{op} {a} == {r_names[b]} -> {r_names[c]} [{registers[c]}]')
        elif op == 'eqri':
            registers[c] = 1 if registers[a] == b else 0
            bug(f'{op} {r_names[a]} == {b} -> {r_names[c]} [{registers[c]}]')
        elif op == 'eqrr':
            registers[c] = 1 if registers[a] == registers[b] else 0
            bug(f'{op} {r_names[a]} == {r_names[b]} -> {r_names[c]} [{registers[c]}]')
        registers[ip_reg] += 1
    return registers


def chronal_conversion(inp, ip_reg, pass1=True):
    result = run_script(inp, ip_reg, pass1)
    return result


if __name__ == '__main__':
    with open('input.txt') as code_file:
        code_lines = code_file.read().splitlines(keepends=False)
        ip_reg = -1
        if code_lines[0].startswith('#ip '):
            ip_reg = int(code_lines[0][4:])
        disassemble_script(code_lines[1:], ip_reg)
        print(f'Day 21, pass 1: {chronal_conversion(code_lines[1:], ip_reg)}')
        print(f'Day 21, pass 2: {chronal_conversion(code_lines[1:], ip_reg, False)}')
        # Day 21, pass 1: 12446070
        # Day 21, pass 2: 13928239
