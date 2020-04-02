def run_script(inp, ip_reg, zero_start):
    registers = [zero_start, 0, 0, 0, 0, 0]
    r_names = ['A', 'B', 'C', 'D', 'IP', 'F']

    if zero_start == 2:
        while 0 <= registers[ip_reg] <= len(inp):
            line = inp[registers[ip_reg]]
            print(f'[{" ".join([f"{n}:{r:<3}" for r, n in zip(registers, r_names)]):^30}] : ', end='')
            op, *params = line.split()
            a, b, c = map(int, params)
            if op == 'addr':
                registers[c] = registers[a] + registers[b]
                print(f'{op} {r_names[a]} + {r_names[b]} -> {r_names[c]} [{registers[c]}]')
            elif op == 'addi':
                registers[c] = registers[a] + b
                print(f'{op} {r_names[a]} + {b} -> {r_names[c]} [{registers[c]}]')
            elif op == 'mulr':
                registers[c] = registers[a] * registers[b]
                print(f'{op} {r_names[a]} * {r_names[b]} -> {r_names[c]} [{registers[c]}]')
            elif op == 'muli':
                registers[c] = registers[a] * b
                print(f'{op} {r_names[a]} * {b} -> {r_names[c]} [{registers[c]}]')
            elif op == 'banr':
                registers[c] = registers[a] & registers[b]
                print(f'{op} {r_names[a]} & {r_names[b]} -> {r_names[c]} [{registers[c]}]')
            elif op == 'bani':
                registers[c] = registers[a] & b
                print(f'{op} {r_names[a]} & {b} -> {r_names[c]} [{registers[c]}]')
            elif op == 'borr':
                registers[c] = registers[a] | registers[b]
                print(f'{op} {r_names[a]} | {r_names[b]} -> {r_names[c]} [{registers[c]}]')
            elif op == 'bori':
                registers[c] = registers[a] | b
                print(f'{op} {r_names[a]} | {b} -> {r_names[c]} [{registers[c]}]')
            elif op == 'setr':
                registers[c] = registers[a]
                print(f'{op} {r_names[a]} -> {r_names[c]} [{registers[c]}]')
            elif op == 'seti':
                registers[c] = a
                print(f'{op} {a} -> {r_names[c]} [{registers[c]}]')
            elif op == 'gtir':
                registers[c] = 1 if a > registers[b] else 0
                print(f'{op} {a} > {r_names[b]} -> {r_names[c]} [{registers[c]}]')
            elif op == 'gtri':
                registers[c] = 1 if registers[a] > b else 0
                print(f'{op} {r_names[a]} > {b} -> {r_names[c]} [{registers[c]}]')
            elif op == 'gtrr':
                registers[c] = 1 if registers[a] > registers[b] else 0
                print(f'{op} {r_names[a]} > {r_names[b]} -> {r_names[c]} [{registers[c]}]')
            elif op == 'eqir':
                registers[c] = 1 if a == registers[b] else 0
                print(f'{op} {a} == {r_names[b]} -> {r_names[c]} [{registers[c]}]')
            elif op == 'eqri':
                registers[c] = 1 if registers[a] == b else 0
                print(f'{op} {r_names[a]} == {b} -> {r_names[c]} [{registers[c]}]')
            elif op == 'eqrr':
                registers[c] = 1 if registers[a] == registers[b] else 0
                print(f'{op} {r_names[a]} == {r_names[b]} -> {r_names[c]} [{registers[c]}]')
            registers[ip_reg] += 1
    else:
        a, b, c, d, ip, f = registers
        if a == 0:
            f = 964
        else:
            f = 10551364
        ##
        # Assembly code reduces to:
        #
        # a = 0
        # for d in range(1, f + 1):
        #     for b in range(1, f + 1):
        #         if b * d == f:
        #             print(f'Add in {d}')
        #             a += d
        #
        # This code finds all the factors of 'f' and sums them, this is expressed more concisely as:
        ##
        c = list([b, f // b] for b in range(1, int(f ** 0.5) + 1) if f % b == 0)
        a = sum(sum(d) for d in c)
        registers = a, b, c, d, ip, f
    return registers


def go_with_the_flow(inp, zero_start=0):
    script = inp.copy()
    ip_reg = -1
    if script[0].startswith('#ip '):
        ip_reg = int(script[0][4:])
        script.remove(script[0])
    registers = run_script(script, ip_reg, zero_start)
    return registers[0]


if __name__ == '__main__':
    with open('input.txt') as bg_code_file:
        bg_code_string = bg_code_file.read().splitlines(keepends=False)
        print(f'Day 19, part 1: {go_with_the_flow(bg_code_string)}')
        print(f'Day 19, part 2: {go_with_the_flow(bg_code_string, 1)}')
        # Day 19, part 1: 1694
        # Day 19, part 2: 18964204
