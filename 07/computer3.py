import itertools
import operator
import threading
from collections import namedtuple, deque
from enum import IntEnum
from time import sleep


class AccessMode(IntEnum):
    PARAMETER = 0
    IMMEDIATE = 1


class DisStyle(IntEnum):
    NO_PARAM = 0  # HALT
    THREE_PARAM = 1  # P3 ← P1 op P2
    IN_PARAM = 2  # P1 ← console
    OUT_PARAM = 3  # P1 → console
    COND_JUMP = 4  # (P1) goto P2


OpCodes = namedtuple('OpCodes', 'num instruction length op dis_style')

opcode_list = {
    1: OpCodes(1, 'ADD', 4, operator.add, DisStyle.THREE_PARAM),
    2: OpCodes(2, 'MUL', 4, operator.mul, DisStyle.THREE_PARAM),
    3: OpCodes(3, 'INP', 2, None, DisStyle.IN_PARAM),
    4: OpCodes(4, 'OUT', 2, None, DisStyle.OUT_PARAM),
    5: OpCodes(5, 'JNZ', 3, lambda x: x != 0, DisStyle.COND_JUMP),
    6: OpCodes(6, 'JZ', 3, lambda x: x == 0, DisStyle.COND_JUMP),
    7: OpCodes(7, 'LT', 4, (lambda x, y: 1 if x < y else 0), DisStyle.THREE_PARAM),
    8: OpCodes(8, 'EQ', 4, (lambda x, y: 1 if x == y else 0), DisStyle.THREE_PARAM),
    99: OpCodes(99, 'HLT', 1, None, DisStyle.NO_PARAM)
}


def prepare_mem(init_mem: str):
    return [int(v) for v in init_mem.split(',')]


class Processor(object):
    def __init__(self, mem_str: str):
        self._core = []
        self._mem_str = mem_str
        self._ip = 0
        self._input = deque()
        self._output = list()
        self.reset_core()
        self._sender = None

    def reset_core(self):
        self._core = prepare_mem(self._mem_str)
        self._input.clear()
        self._output.clear()
        self._ip = 0

    def current_instruction(self):
        return opcode_list[int(self.core[self.ip] % 100)]

    def parameter(self, param_num, as_str=False, target=False):
        if 0 < param_num < self.current_instruction().length:
            mode = AccessMode((self.core[self.ip] // 10 ** (param_num + 1)) % 10)
            param = self.core[self.ip + param_num]
            if as_str:
                return f'[{param}]' if mode == AccessMode.PARAMETER else f'#{param}'
            else:
                if target:
                    return param
                else:
                    return self.core[param] if mode == AccessMode.PARAMETER else param
        else:
            raise OverflowError(f'Incorrect parameter number: {param_num} at instruction {self.ip}')

    def receiver(self, input):
        self._input.appendleft(input)

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, val):
        if isinstance(val, int) and 0 <= val < len(self.core):
            self._ip = val
        else:
            raise ValueError('IP can only be set to a positive integer within code space')

    @property
    def core(self):
        return self._core

    @property
    def output(self):
        return self._output

    def opcode(self, instruction: OpCodes):
        ip = self.ip
        op, *param = self.core[ip:ip + instruction.length]
        dump = f'{op:05} ' + " ".join(f'{v:5}' for v in param)
        if instruction.dis_style == DisStyle.THREE_PARAM:
            return f'{dump:23} : {self.parameter(3, True)} ← {self.parameter(1, True)} ' \
                   f'{instruction.instruction} {self.parameter(2, True)} '
        elif instruction.dis_style == DisStyle.IN_PARAM:
            return f'{dump:23} : {self.parameter(1, True)} ← {instruction.instruction}'
        elif instruction.dis_style == DisStyle.OUT_PARAM:
            return f'{dump:23} : {instruction.instruction} ← {self.parameter(1, True)}'
        elif instruction.dis_style == DisStyle.COND_JUMP:
            return f'{dump:23} : {instruction.instruction} ({self.parameter(1, True)}) {self.parameter(2, True)}'
        else:
            return f'{dump:23} : HALT'

    def _wait_for_input(self):
        while len(self._input) == 0:
            sleep(0.0001)

    def step(self):
        inst = self.current_instruction()
        if inst.dis_style == DisStyle.THREE_PARAM:
            self.core[self.parameter(3, target=True)] = inst.op(self.parameter(1), self.parameter(2))
        elif inst.dis_style == DisStyle.IN_PARAM:
            self._wait_for_input()
            self.core[self.parameter(1, target=True)] = self._input.pop()
        elif inst.dis_style == DisStyle.OUT_PARAM:
            print(f'OUT({self.ip:05}) → {self.parameter(1)}')
            if self._sender:
                self._sender(self.parameter(1))
            else:
                self._output.append(self.parameter(1))
        elif inst.dis_style == DisStyle.COND_JUMP:
            if inst.op(self.parameter(1)):
                self.ip = self.parameter(2)
                return
        elif inst.dis_style == DisStyle.NO_PARAM:
            raise GeneratorExit(f'Halt at {self.ip}')
        self.ip += inst.length

    def simulate(self, inputs=None, trace=False):
        if inputs:
            self._input.extendleft(inputs)
        while self.ip < len(self.core):
            if trace:
                inst = self.current_instruction()
                print(f'{self.ip:05} : {self.opcode(inst)}')
            try:
                self.step()
            except GeneratorExit:
                break

    def disassemble(self, patch: str or None = None, start_at=None, end_at=None):
        if patch:
            for s in patch.split(','):
                a, v = [int(x) for x in s.split(':')]
                self.core[a] = v
        if start_at:
            self.ip = start_at
        if not end_at:
            end_at = len(self.core)

        while self.ip < end_at:
            inst = self.current_instruction()
            print(f'{self.ip:05} : {self.opcode(inst)}')
            self.ip += inst.length


class Amplifier(object):
    def __init__(self, mem_str: str):
        self._amps = [Processor(mem_str) for n in range(5)]

    def run(self, inputs: str or list, trace=False):
        out = 0
        p = self._amps[0]
        if isinstance(inputs, str):
            inputs = [int(v) for v in inputs.split(',')]
        for inp in inputs:
            p.reset_core()
            p.simulate([inp, out], trace=trace)
            out = p.output[0]
        return out

    def run_regeneration(self, inputs: str or list):
        if isinstance(inputs, str):
            inputs = [int(v) for v in inputs.split(',')]
        p = self._amps[0]
        p.reset_core()
        for n in self._amps[1:]:
            p._sender = n.receiver
            p = n
            p.reset_core()
        self._amps[-1]._sender = self._amps[0].receiver
        threads = []
        for a, n in zip(self._amps, inputs):
            a.receiver(n)
            t = threading.Thread(target=a.simulate)
            threads.append(t)
            t.start()
        self._amps[0].receiver(0)
        while any(t.is_alive() for t in threads):
            sleep(0.0001)
        return self._amps[0]._input.pop()


if __name__ == '__main__':
    with open('input') as f:
        initial_cells = f.read()

    computer = Amplifier(initial_cells)

    print('Part 1')
    res = []
    for inp in itertools.permutations(range(5)):
        res.append((inp, computer.run(inp, trace=True)))
    print(max(res, key=lambda x: x[1]))

    print('Part 2')
    res = []
    for inp in itertools.permutations(range(5, 10)):
        print(f'Input sequence: {str(inp)}')
        res.append((inp, computer.run_regeneration(inp)))
    print(max(res, key=lambda x: x[1]))

    '''
    '''

    # computer.reset_core()
    # computer.disassemble(patch="6:1101", end_at=223)
    # print('=' * 80)
    # computer.reset_core()
    # computer.disassemble(patch="6:1105", end_at=9)
    # print('...')
    # computer.disassemble(patch="6:1105", start_at=238, end_at=677)
