from collections import namedtuple, deque, defaultdict

Instruction = namedtuple('Instruction', ['opcode', 'in_a', 'in_b', 'out'])


class TimeComputer(object):
    def __init__(self, before_regs: str, instruction_bytes: str, after_regs: str):
        self.before_regs = list(map(int, before_regs[1:-1].split(', ')))
        self.instructions = Instruction(*map(int, instruction_bytes.split()))
        self.after_regs = list(map(int, after_regs[1:-1].split(', ')))

    def addr(self):
        a = self.before_regs[self.instructions.in_a]
        b = self.before_regs[self.instructions.in_b]
        c = a + b
        return self.after_regs[self.instructions.out] == c

    def addi(self):
        a = self.before_regs[self.instructions.in_a]
        b = self.instructions.in_b
        c = a + b
        return self.after_regs[self.instructions.out] == c

    def mulr(self):
        a = self.before_regs[self.instructions.in_a]
        b = self.before_regs[self.instructions.in_b]
        c = a * b
        return self.after_regs[self.instructions.out] == c

    def muli(self):
        a = self.before_regs[self.instructions.in_a]
        b = self.instructions.in_b
        c = a * b
        return self.after_regs[self.instructions.out] == c

    def banr(self):
        a = self.before_regs[self.instructions.in_a]
        b = self.before_regs[self.instructions.in_b]
        c = a & b
        return self.after_regs[self.instructions.out] == c

    def bani(self):
        a = self.before_regs[self.instructions.in_a]
        b = self.instructions.in_b
        c = a & b
        return self.after_regs[self.instructions.out] == c

    def borr(self):
        a = self.before_regs[self.instructions.in_a]
        b = self.before_regs[self.instructions.in_b]
        c = a | b
        return self.after_regs[self.instructions.out] == c

    def bori(self):
        a = self.before_regs[self.instructions.in_a]
        b = self.instructions.in_b
        c = a | b
        return self.after_regs[self.instructions.out] == c

    def setr(self):
        a = self.before_regs[self.instructions.in_a]
        c = a
        return self.after_regs[self.instructions.out] == c

    def seti(self):
        a = self.instructions.in_a
        c = a
        return self.after_regs[self.instructions.out] == c

    def gtir(self):
        a = self.instructions.in_a
        b = self.before_regs[self.instructions.in_b]
        c = 1 if a > b else 0
        return self.after_regs[self.instructions.out] == c

    def gtri(self):
        a = self.before_regs[self.instructions.in_a]
        b = self.instructions.in_b
        c = 1 if a > b else 0
        return self.after_regs[self.instructions.out] == c

    def gtrr(self):
        a = self.before_regs[self.instructions.in_a]
        b = self.before_regs[self.instructions.in_b]
        c = 1 if a > b else 0
        return self.after_regs[self.instructions.out] == c

    def eqir(self):
        a = self.instructions.in_a
        b = self.before_regs[self.instructions.in_b]
        c = 1 if a == b else 0
        return self.after_regs[self.instructions.out] == c

    def eqri(self):
        a = self.before_regs[self.instructions.in_a]
        b = self.instructions.in_b
        c = 1 if a == b else 0
        return self.after_regs[self.instructions.out] == c

    def eqrr(self):
        a = self.before_regs[self.instructions.in_a]
        b = self.before_regs[self.instructions.in_b]
        c = 1 if a == b else 0
        return self.after_regs[self.instructions.out] == c

    def test_opcode(self):
        fns = {'addr': self.addr,
               'addi': self.addi,
               'mulr': self.mulr,
               'muli': self.muli,
               'banr': self.banr,
               'bani': self.bani,
               'borr': self.borr,
               'bori': self.bori,
               'setr': self.setr,
               'seti': self.seti,
               'gtir': self.gtir,
               'gtri': self.gtri,
               'gtrr': self.gtrr,
               'eqir': self.eqir,
               'eqri': self.eqri,
               'eqrr': self.eqrr}
        result = []
        for k, f in fns.items():
            if f():
                result.append(k)
        return result

    @property
    def opcode(self):
        return self.instructions.opcode


def chronal_classification_part_1(inp):
    computers = deque()
    for n in range(len(inp) // 4):
        lines = inp[n * 4: (n + 1) * 4]
        if lines[0].startswith('Before:'):
            computers.append(TimeComputer(lines[0].lstrip('Before: '), lines[1], lines[2].lstrip('After: ')))
        else:
            break
    result = 0
    for puter in computers:
        if len(puter.test_opcode()) >= 3:
            result += 1
    return result


def chronal_classification_part_2(inp):
    computers = deque()
    script_line = None
    for n in range(len(inp) // 4):
        lines = inp[n * 4: (n + 1) * 4]
        if lines[0].startswith('Before:'):
            computers.append(TimeComputer(lines[0].lstrip('Before: '), lines[1], lines[2].lstrip('After: ')))
        else:
            script_line = n * 4
            break
    opcode_table = create_opcode_table(computers)

    print('+--------+----------+')
    print('| Opcode | Mnemonic |')
    print('+--------+----------+')
    for x in range(16):
        print(f'|{x:^8}| {opcode_table[x]:^9}|')
    print('+--------+----------+')

    registers = run_script(inp[script_line:], opcode_table)

    return registers[0]


def create_opcode_table(computers):
    opcode_election = defaultdict(set)
    for computer in computers:
        for check in computer.test_opcode():
            opcode_election[check].add(computer.opcode)
    opcode_results = dict(sorted(opcode_election.items(), key=lambda x: len(x[1])))
    opcode_table = dict()
    claimed_opcodes = set()
    while len(opcode_results) > 0:
        new_results = dict()
        for mnemonic, opcode_set in opcode_results.items():
            opcode_set -= claimed_opcodes
            if len(opcode_set) == 1:
                this_opcode = opcode_set.pop()
                claimed_opcodes.add(this_opcode)
                opcode_table[this_opcode] = mnemonic
            else:
                new_results[mnemonic] = opcode_set
        opcode_results = new_results
    return opcode_table


def run_script(inp, opcode_table):
    registers = [0, 0, 0, 0]

    for line in inp:
        if len(line.strip()) == 0:
            continue
        op, a, b, c = map(int, line.split())
        fn = opcode_table[op]
        if fn == 'addr':
            registers[c] = registers[a] + registers[b]
        elif fn == 'addi':
            registers[c] = registers[a] + b
        elif fn == 'mulr':
            registers[c] = registers[a] * registers[b]
        elif fn == 'muli':
            registers[c] = registers[a] * b
        elif fn == 'banr':
            registers[c] = registers[a] & registers[b]
        elif fn == 'bani':
            registers[c] = registers[a] & b
        elif fn == 'borr':
            registers[c] = registers[a] | registers[b]
        elif fn == 'bori':
            registers[c] = registers[a] | b
        elif fn == 'setr':
            registers[c] = registers[a]
        elif fn == 'seti':
            registers[c] = a
        elif fn == 'gtir':
            registers[c] = 1 if a > registers[b] else 0
        elif fn == 'gtri':
            registers[c] = 1 if registers[a] > b else 0
        elif fn == 'gtrr':
            registers[c] = 1 if registers[a] > registers[b] else 0
        elif fn == 'eqir':
            registers[c] = 1 if a == registers[b] else 0
        elif fn == 'eqri':
            registers[c] = 1 if registers[a] == b else 0
        elif fn == 'eqrr':
            registers[c] = 1 if registers[a] == registers[b] else 0
    return registers


if __name__ == '__main__':
    with open('input.txt') as instruction_file:
        instruction_strings = instruction_file.read().splitlines(keepends=False)
        print(f'Day 16, part 1: {chronal_classification_part_1(instruction_strings)}')
        print(f'Day 16, part 2: {chronal_classification_part_2(instruction_strings)}')
        # Day 16, part 1: 642
        # +--------+----------+
        # | Opcode | Mnemonic |
        # +--------+----------+
        # |   0    |   eqir   |
        # |   1    |   addi   |
        # |   2    |   gtir   |
        # |   3    |   setr   |
        # |   4    |   mulr   |
        # |   5    |   seti   |
        # |   6    |   muli   |
        # |   7    |   eqri   |
        # |   8    |   bori   |
        # |   9    |   bani   |
        # |   10   |   gtrr   |
        # |   11   |   eqrr   |
        # |   12   |   addr   |
        # |   13   |   gtri   |
        # |   14   |   borr   |
        # |   15   |   banr   |
        # +--------+----------+
        # Day 16, part 2: 481
