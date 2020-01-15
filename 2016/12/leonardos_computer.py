CODE = []
REGISTERS = {'a': 0, 'b': 0, 'c': 0, 'd': 0}


def ins_cpy(x, y):
    if x.isdigit():
        REGISTERS[y] = int(x)
    else:
        REGISTERS[y] = REGISTERS[x]
    return 1


def ins_inc(x):
    REGISTERS[x] += 1
    return 1


def ins_dec(x):
    REGISTERS[x] -= 1
    return 1


def ins_jnz(x, y):
    return int(y) if (x.isdigit() and x != 0) or REGISTERS[x] != 0 else 1


OPCODES = {
    'cpy': ins_cpy,
    'inc': ins_inc,
    'dec': ins_dec,
    'jnz': ins_jnz
}


def run():
    ip = 0
    while ip < len(CODE):
        ins, *params = CODE[ip].split()
        ip += OPCODES[ins](*params)


CODE.clear()
with open('input') as f:
    CODE.extend(f.read().splitlines(keepends=False))
run()
print(f'Part 1: {REGISTERS["a"]}')

REGISTERS.update({'a': 0, 'b': 0, 'c': 1, 'd': 0})
run()
print(f'Part 2: {REGISTERS["a"]}')

# Part 1: 318007
# Part 2: 9227661
