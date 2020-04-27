CODE = []
REGISTERS = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
ip: int = 0


def val_or_reg(x):
    if x.lstrip('+-').isdigit():
        return int(x)
    else:
        return REGISTERS[x]


def ins_cpy(x, y):
    REGISTERS[y] = val_or_reg(x)
    return 1


def ins_inc(x):
    REGISTERS[x] += 1
    return 1


def ins_dec(x):
    REGISTERS[x] -= 1
    return 1


def ins_jnz(x, y):
    return val_or_reg(y) if val_or_reg(x) != 0 else 1


OPCODE_TX = {
    'inc': 'dec',
    'dec': 'inc',
    'jnz': 'cpy',
    'cpy': 'jnz',
    'tgl': 'inc',
    'out': 'inc'
}


def ins_tgl(x):
    global ip
    target_ip = ip + val_or_reg(x)
    if 0 <= target_ip < len(CODE):
        temp = CODE[target_ip]
        CODE[target_ip] = OPCODE_TX[temp[:3]] + temp[3:]
    return 1


def ins_out(x):
    n = val_or_reg(x)
    if n != ins_out.target:
        raise ValueError(f'Expected {ins_out.target}, got {n}')
    else:
        ins_out.target = 1 - ins_out.target
        ins_out.count += 1
        if ins_out.count > 1000:
            raise StopIteration(f'Looks like a match')
    return 1


ins_out.target = 0
ins_out.count = 0

OPCODES = {
    'cpy': ins_cpy,
    'inc': ins_inc,
    'dec': ins_dec,
    'jnz': ins_jnz,
    'tgl': ins_tgl,
    'out': ins_out
}


def run():
    global ip
    ins_out.target = 0
    ins_out.count = 0
    ip = 0
    while ip < len(CODE):
        if ip == 0:
            # 0: cpy a d
            # 1: cpy 9 c
            # 2: cpy 282 b
            # 3: inc d
            # 4: dec b
            # 5: jnz b -2
            # 6: dec c
            # 7: jnz c -5
            # becomes:
            REGISTERS['d'] = REGISTERS['a'] + 9 * 282
            ip = 8
        elif ip == 10:
            # 10: cpy a b
            # 11: cpy 0 a
            # 12: cpy 2 c
            # 13: jnz b 2
            # 14: jnz 1 6
            # 15: dec b
            # 16: dec c
            # 17: jnz c -4
            # 18: inc a
            # 19: jnz 1 -7
            # becomes:
            REGISTERS['a'], REGISTERS['c'] = divmod(REGISTERS['a'], 2)
            REGISTERS['c'] = 2 - REGISTERS['c']
            ip = 20
        else:
            ins, *params = CODE[ip].split()
            ip += OPCODES[ins](*params)


if __name__ == '__main__':
    with open('input.txt') as assembunny_file:
        CODE.extend(assembunny_file.read().splitlines(keepends=False))
    a = 1
    while True:
        print(a, end=', ')
        REGISTERS["a"] = a
        try:
            run()
        except ValueError:
            pass
        except StopIteration:
            break
        a += 1
    print(f'\nDay 25, part 1: {a}')
    # Day 25, part 1: 192
