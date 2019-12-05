from collections import namedtuple
from enum import IntEnum


class AccessMode(IntEnum):
    PARAMETER = 0
    IMMEDIATE = 1


class DisStyle(IntEnum):
    NO_PARAM = 0  # HALT
    THREE_PARAM = 1  # P3 ← P1 op P2
    IN_PARAM = 2  # P1 ← console
    OUT_PARAM = 3  # P1 → console
    COND_JUMP = 4  # (P1) goto P2


OpCodes = namedtuple('OpCodes', 'num instruction length dis_style')

opcode_list = {
    1: OpCodes(1, 'ADD', 4, DisStyle.THREE_PARAM),
    2: OpCodes(2, 'MUL', 4, DisStyle.THREE_PARAM),
    3: OpCodes(3, 'INP', 2, DisStyle.IN_PARAM),
    4: OpCodes(4, 'OUT', 2, DisStyle.OUT_PARAM),
    5: OpCodes(5, 'JNZ', 3, DisStyle.COND_JUMP),
    6: OpCodes(6, 'JZ', 3, DisStyle.COND_JUMP),
    7: OpCodes(7, 'LT', 4, DisStyle.THREE_PARAM),
    8: OpCodes(8, 'EQ', 4, DisStyle.THREE_PARAM),
    99: OpCodes(99, 'HLT', 1, DisStyle.NO_PARAM)
}


def prepare_mem(init_mem: str):
    return [int(v) for v in init_mem.split(',')]


class Processor(object):
    def __init__(self, mem_str: str):
        self._mem_str = mem_str
        self._memory = prepare_mem(mem_str)
        self._ip = 0

    def current_instruction(self):
        return opcode_list[int(self._memory[self._ip] % 100)]

    def parameter(self, param_num, as_str=False):
        instr = f'000000{str(self._memory[self._ip])}'[-5:]
        mode = int(instr[-2 - param_num])
        param = self._memory[self.ip + param_num]
        if as_str:
            return f'[{param}]' if mode == AccessMode.PARAMETER else f'#{param}'
        else:
            return self._memory[param] if mode == AccessMode.PARAMETER else param

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, val):
        if isinstance(val, int) and 0 <= val < len(self._memory):
            self._ip = val
        else:
            raise ValueError('IP can only be set to a positive integer within code space')

    @property
    def memory(self):
        return self._memory


def computer(cells):
    memory = prepare_mem(cells)
    memory = simulate(memory)
    return ','.join(str(v) for v in memory)


def param_read(memory, param, mode):
    if mode == AccessMode.PARAMETER:
        return memory[memory[param]]
    elif mode == AccessMode.IMMEDIATE:
        return memory[param]
    raise ValueError('Bad memory access mode')


def simulate(memory, inputs=None):
    ip = 0
    user_input_vec = 0
    while memory[ip] != 99:
        instr = f'000000{str(memory[ip])}'[-5:]
        op = int(instr[-2:])
        mode = [int(instr[n]) for n in range(-3, -6, -1)]
        if op == 1:
            memory[memory[ip + 3]] = param_read(memory, ip + 1, mode[0]) + param_read(memory, ip + 2, mode[1])
            ip += 4
        elif op == 2:
            memory[memory[ip + 3]] = param_read(memory, ip + 1, mode[0]) * param_read(memory, ip + 2, mode[1])
            ip += 4
        elif op == 3:
            if inputs and user_input_vec < len(inputs):
                user_input = inputs[user_input_vec]
                user_input_vec += 1
            else:
                user_input = input('Enter Value: ')
            memory[memory[ip + 1]] = user_input
            ip += 2
        elif op == 4:
            res = param_read(memory, ip + 1, mode[0])
            print(f'Result: {res}')
            ip += 2
        elif op == 5:
            if param_read(memory, ip + 1, mode[0]) != 0:
                ip = param_read(memory, ip + 2, mode[1])
            else:
                ip += 3
        elif op == 6:
            if param_read(memory, ip + 1, mode[0]) == 0:
                ip = param_read(memory, ip + 2, mode[1])
            else:
                ip += 3
        elif op == 7:
            memory[memory[ip + 3]] = 1 if param_read(memory, ip + 1, mode[0]) < param_read(memory, ip + 2,
                                                                                           mode[1]) else 0
            ip += 4
        elif op == 8:
            memory[memory[ip + 3]] = 1 if param_read(memory, ip + 1, mode[0]) == param_read(memory, ip + 2,
                                                                                            mode[1]) else 0
            ip += 4
        else:
            raise TypeError
    return memory


def run_computer_recover(cells):
    memory = prepare_mem(cells)
    memory[1] = 12
    memory[2] = 2
    memory = simulate(memory)
    print(memory[0])


OPCODES = {1: '+', 2: '*', 3: '←', 4: 'out', 5: 'jnz', 6: 'jz', 7: 'lt', 8: 'eq', 99: 'halt'}


def opcode(instruction: OpCodes, processor: Processor):
    ip = processor.ip
    op, *param = processor.memory[ip:ip + instruction.length]
    dump = f'{op:05} ' + " ".join(f'{v:03}' for v in param)
    if instruction.dis_style == DisStyle.THREE_PARAM:
        return f'{dump:20} : {processor.parameter(3, True)} ← {processor.parameter(1, True)} ' \
               f'{instruction.instruction} {processor.parameter(2, True)} '
    elif instruction.dis_style == DisStyle.IN_PARAM:
        return f'{dump:20} : {processor.parameter(1, True)} ← {instruction.instruction}'
    elif instruction.dis_style == DisStyle.OUT_PARAM:
        return f'{dump:20} : {instruction.instruction} ← {processor.parameter(1, True)}'
    elif instruction.dis_style == DisStyle.COND_JUMP:
        return f'{dump:20} : {instruction.instruction} ({processor.parameter(1, True)}) {processor.parameter(2, True)}'
    else:
        return f'{dump:20} : HALT'


def disassemble(cells: str, patch: str or None = None, start_at=None, end_at=None):
    p = Processor(cells)
    if patch:
        for s in patch.split(','):
            a, v = [int(x) for x in s.split(':')]
            p.memory[a] = v
    if start_at:
        p.ip = start_at
    if not end_at:
        end_at = len(p.memory)

    while p.ip < end_at:
        inst = p.current_instruction()
        print(f'{p.ip:05} : {opcode(inst, p)}')
        p.ip += inst.length


if __name__ == '__main__':
    initial_cells = '3,225,1,225,6,6,1100,1,238,225,104,0,1101,86,8,225,1101,82,69,225,101,36,65,224,1001,224,-106,' \
                    '224,4,224,1002,223,8,223,1001,224,5,224,1,223,224,223,102,52,148,224,101,-1144,224,224,4,224,' \
                    '1002,223,8,223,101,1,224,224,1,224,223,223,1102,70,45,225,1002,143,48,224,1001,224,-1344,224,4,' \
                    '224,102,8,223,223,101,7,224,224,1,223,224,223,1101,69,75,225,1001,18,85,224,1001,224,-154,224,4,' \
                    '224,102,8,223,223,101,2,224,224,1,224,223,223,1101,15,59,225,1102,67,42,224,101,-2814,224,224,4,' \
                    '224,1002,223,8,223,101,3,224,224,1,223,224,223,1101,28,63,225,1101,45,22,225,1101,90,16,225,2,' \
                    '152,92,224,1001,224,-1200,224,4,224,102,8,223,223,101,7,224,224,1,223,224,223,1101,45,28,224,' \
                    '1001,224,-73,224,4,224,1002,223,8,223,101,7,224,224,1,224,223,223,1,14,118,224,101,-67,224,224,' \
                    '4,224,1002,223,8,223,1001,224,2,224,1,223,224,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,' \
                    '0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,' \
                    '265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,' \
                    '1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,' \
                    '1105,1,99999,7,677,677,224,102,2,223,223,1005,224,329,1001,223,1,223,1008,226,226,224,1002,223,' \
                    '2,223,1005,224,344,1001,223,1,223,1107,677,226,224,1002,223,2,223,1006,224,359,1001,223,1,223,' \
                    '107,677,677,224,102,2,223,223,1005,224,374,101,1,223,223,1108,677,226,224,102,2,223,223,1005,' \
                    '224,389,1001,223,1,223,1007,677,677,224,1002,223,2,223,1005,224,404,101,1,223,223,1008,677,226,' \
                    '224,102,2,223,223,1005,224,419,101,1,223,223,1108,226,677,224,102,2,223,223,1006,224,434,1001,' \
                    '223,1,223,8,677,226,224,1002,223,2,223,1005,224,449,101,1,223,223,1008,677,677,224,1002,223,2,' \
                    '223,1006,224,464,1001,223,1,223,1108,226,226,224,1002,223,2,223,1005,224,479,1001,223,1,223,' \
                    '1007,226,677,224,102,2,223,223,1005,224,494,1001,223,1,223,1007,226,226,224,102,2,223,223,1005,' \
                    '224,509,101,1,223,223,107,677,226,224,1002,223,2,223,1006,224,524,1001,223,1,223,108,677,677,' \
                    '224,102,2,223,223,1006,224,539,101,1,223,223,7,677,226,224,102,2,223,223,1006,224,554,1001,223,' \
                    '1,223,1107,226,677,224,102,2,223,223,1005,224,569,101,1,223,223,108,677,226,224,1002,223,2,223,' \
                    '1006,224,584,101,1,223,223,108,226,226,224,102,2,223,223,1006,224,599,1001,223,1,223,1107,226,' \
                    '226,224,102,2,223,223,1006,224,614,1001,223,1,223,8,226,677,224,102,2,223,223,1006,224,629,1001,' \
                    '223,1,223,107,226,226,224,102,2,223,223,1005,224,644,101,1,223,223,8,226,226,224,102,2,223,223,' \
                    '1006,224,659,101,1,223,223,7,226,677,224,102,2,223,223,1005,224,674,101,1,223,223,4,223,99,226 '
    print('Part 1')
    memory = prepare_mem(initial_cells)
    simulate(memory, [1])
    print('Part 2')
    memory = prepare_mem(initial_cells)
    simulate(memory, [5])

    # disassemble(initial_cells, patch="6:1101", end_at=223)
    # print('=' * 80)
    # disassemble(initial_cells, patch="6:1105", end_at=9)
    # print('...')
    # disassemble(initial_cells, patch="6:1105", start_at=238, end_at=677)
