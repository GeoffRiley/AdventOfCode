class CPU(object):
    def __init__(self, program):
        self.program = program
        self.ip = 0
        self.registers = {'a': 0, 'b': 0}
        self.instr = {
            'hlf': self.hlf,
            'tpl': self.tpl,
            'inc': self.inc,
            'jmp': self.jmp,
            'jie': self.jie,
            'jio': self.jio
        }

    def reset(self, a, b):
        self.ip = 0
        self.registers['a'] = a
        self.registers['b'] = b

    def decode_cmd_r(self, cmd):
        if cmd not in ['a', 'b']:
            raise TypeError(f'Could not recognise {cmd} as a register')
        return cmd

    def decode_cmd_o(self, cmd):
        return int(cmd)

    def decode_cmd_r_o(self, cmd):
        r, o = cmd.split(', ')
        return self.decode_cmd_r(r), self.decode_cmd_o(o)

    def inc(self, cmd: str):
        r = self.decode_cmd_r(cmd)
        self.registers[r] += 1
        self.ip += 1

    def hlf(self, cmd: str):
        r = self.decode_cmd_r(cmd)
        self.registers[r] //= 2
        self.ip += 1

    def tpl(self, cmd: str):
        r = self.decode_cmd_r(cmd)
        self.registers[r] *= 3
        self.ip += 1

    def jmp(self, cmd: str):
        o = self.decode_cmd_o(cmd)
        self.ip += o

    def jie(self, cmd: str):
        r, o = self.decode_cmd_r_o(cmd)
        if self.registers[r] % 2 == 0:
            self.ip += o
        else:
            self.ip += 1

    def jio(self, cmd: str):
        r, o = self.decode_cmd_r_o(cmd)
        if self.registers[r] == 1:
            self.ip += o
        else:
            self.ip += 1

    def run(self):
        while 0 <= self.ip < len(self.program):
            opcode, param = self.program[self.ip].split(' ', maxsplit=1)
            self.instr[opcode](param.strip())


with open('input') as f:
    program = f.read().splitlines(keepends=False)
processor = CPU(program)
processor.run()
print(f'Part 1: {processor.registers["b"]}')
processor.reset(1, 0)
processor.run()
print(f'Part 2: {processor.registers["b"]}')

# Part 1: 255
# Part 2: 334
