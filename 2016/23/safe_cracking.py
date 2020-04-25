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
    'tgl': 'inc'
}


def ins_tgl(x):
    global ip
    target_ip = ip + val_or_reg(x)
    if 0 <= target_ip < len(CODE):
        temp = CODE[target_ip]
        CODE[target_ip] = OPCODE_TX[temp[:3]] + temp[3:]
    return 1


OPCODES = {
    'cpy': ins_cpy,
    'inc': ins_inc,
    'dec': ins_dec,
    'jnz': ins_jnz,
    'tgl': ins_tgl
}


def run():
    global ip
    ip = 0
    while ip < len(CODE):
        if ip == 5:
            #  5: inc a
            #  6: dec c
            #  7: jnz c -2
            #  8: dec d
            #  9: jnz d -5
            # becomes:
            REGISTERS['a'] = REGISTERS['c'] * REGISTERS['d']
            ip = 10
        else:
            ins, *params = CODE[ip].split()
            ip += OPCODES[ins](*params)


if __name__ == '__main__':
    with open('input.txt') as assembunny_file:
        CODE.extend(assembunny_file.read().splitlines(keepends=False))
    REGISTERS["a"] = 7
    run()
    print(f'Day 23, part 1: {REGISTERS["a"]}')
    CODE.clear()
    with open('input.txt') as assembunny_file:
        CODE.extend(assembunny_file.read().splitlines(keepends=False))
    REGISTERS["a"] = 12
    run()
    print(f'Day 23, part 2: {REGISTERS["a"]}')
    # Day 23, part 1: 13685
    # Day 23, part 2: 479010245
