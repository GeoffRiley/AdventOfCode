import operator
from collections import namedtuple, deque
from enum import IntEnum
from time import sleep


class ParameterMode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


class DisStyle(IntEnum):
    NO_PARAM = 0  # HALT
    THREE_PARAM = 1  # P3 ← P1 op P2
    IN_PARAM = 2  # P1 ← console
    OUT_PARAM = 3  # P1 → console
    COND_JUMP = 4  # (P1) goto P2
    RELATIVE = 5  # offset


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
    9: OpCodes(9, 'RB', 2, None, DisStyle.RELATIVE),
    99: OpCodes(99, 'HLT', 1, None, DisStyle.NO_PARAM)
}


def prepare_mem(init_mem: str):
    return [int(v) for v in init_mem.split(',')]


def join_comments(comments: list) -> str:
    comments = [c for c in comments if len(c.strip()) > 0]
    if len(comments) > 0:
        return '; ' + ', '.join(comments)
    return ''


class Intcode(object):
    def __init__(self, mem_str: str, name: str = 'Intcode'):
        self.name = name
        self._log = []
        self._core = []
        self._mem_str = mem_str
        self._ip = 0
        self._relative_base = 0
        self._input = deque()
        self._output = list()
        self.reset_core()
        self._verbose = False
        self._sender = None
        self._receiver = None

    def reset_core(self):
        self._log.clear()
        self._core = prepare_mem(self._mem_str + (',0' * len(self._mem_str) * 2))
        self._input.clear()
        self._output.clear()
        self._ip = 0
        self._relative_base = 0
        self._verbose = False

    def log(self, msg):
        self._log.append(msg)
        if self._verbose:
            print(msg)

    def get_log(self):
        return self._log

    def current_instruction(self):
        return opcode_list[int(self.core[self.ip] % 100)]

    def _check_param(self, param_num):
        if 0 < param_num < self.current_instruction().length:
            mode = ParameterMode((self.core[self.ip] // 10 ** (param_num + 1)) % 10)
            param = self.core[self.ip + param_num]
            if mode in [ParameterMode.POSITION, ParameterMode.RELATIVE] and param > len(self.core):
                print(f'param @{param} in memory 0—{len(self.core)}')
            return mode, param
        else:
            raise OverflowError(f'Incorrect parameter number: {param_num} at instruction {self.ip}')

    def parameter(self, param_num, as_str=False, target=False, resolved=False):
        mode, param = self._check_param(param_num)
        if as_str:
            if mode == ParameterMode.POSITION:
                return f'[{param}]'
            elif mode == ParameterMode.IMMEDIATE:
                return f'#{param}'
            elif mode == ParameterMode.RELATIVE:
                if resolved:
                    return f'[{self._relative_base + param}]'
                else:
                    return f'[rel{param:+d}]'
        else:
            if target:
                if mode == ParameterMode.RELATIVE:
                    return self._relative_base + param
                else:
                    return param
            else:
                if mode == ParameterMode.POSITION:
                    return self.core[param]
                elif mode == ParameterMode.IMMEDIATE:
                    return param
                elif mode == ParameterMode.RELATIVE:
                    return self.core[self._relative_base + param]

    def comment_parameter(self, param_num):
        mode, param = self._check_param(param_num)
        if mode == ParameterMode.IMMEDIATE:
            return ''
        return f'{self.parameter(param_num, True, resolved=True)}={self.parameter(param_num)}'

    def receiver(self, input, trace=False):
        if trace:
            self.log(f'Incoming input: {input}')
        self._input.appendleft(input)

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, val):
        if isinstance(val, int) and 0 <= val < len(self.core):
            self._ip = val
        else:
            raise ValueError(f'Bad IP {val}, IP can only be set within code space 0—{len(self.core) - 1}')

    @property
    def core(self):
        return self._core

    @property
    def output(self):
        return self._output

    @property
    def all_output(self):
        return [v for v in self._output]

    def connect(self, receiver, sender=None):
        self._sender = receiver
        self._receiver = sender

    def opcode(self, instruction: OpCodes, trace=False):
        ip = self.ip
        op, *param = self.core[ip:ip + instruction.length]
        dump = f'{op:05} ' + " ".join(f'{v:5}' for v in param)
        comment = ''
        if instruction.dis_style == DisStyle.THREE_PARAM:
            ins = f'{self.parameter(3, True)} ← {self.parameter(1, True)} ' \
                  f'{instruction.instruction} {self.parameter(2, True)} '
            comment = join_comments([self.comment_parameter(1), self.comment_parameter(2)])
        elif instruction.dis_style == DisStyle.IN_PARAM:
            ins = f'{self.parameter(1, True, resolved=True)} ← {instruction.instruction}'
        elif instruction.dis_style == DisStyle.OUT_PARAM:
            ins = f'{instruction.instruction} ← {self.parameter(1, True)}'
            comment = join_comments([self.comment_parameter(1)])
        elif instruction.dis_style == DisStyle.COND_JUMP:
            ins = f'{instruction.instruction} ({self.parameter(1, True)}) {self.parameter(2, True)}'
            comment = join_comments([self.comment_parameter(1), self.comment_parameter(2)])
        elif instruction.dis_style == DisStyle.RELATIVE:
            ins = f'{instruction.instruction} {self.parameter(1, True)}'
            comment = join_comments([self.comment_parameter(1)])
        else:
            ins = 'HALT'
        return f'{dump:23} : {ins:25} {comment if trace else ""}'.strip()

    def _wait_for_input(self, trace=False):
        if trace:
            self.log(f'Waiting for input (@{self.ip:05})')
        while len(self._input) == 0:
            sleep(0.0001)
        inp = self._input.pop()
        if trace:
            self.log(f'        Got {inp}')
        return inp

    def step(self, trace=False):
        inst = self.current_instruction()
        if inst.dis_style == DisStyle.THREE_PARAM:
            self.core[self.parameter(3, target=True)] = inst.op(self.parameter(1), self.parameter(2))
        elif inst.dis_style == DisStyle.IN_PARAM:
            if self._receiver:
                if trace:
                    self.log(f'        Requesting input (@{self.ip:05})')
                self.core[self.parameter(1, target=True)] = self._receiver()
            else:
                self.core[self.parameter(1, target=True)] = self._wait_for_input(trace=trace)
        elif inst.dis_style == DisStyle.OUT_PARAM:
            if trace:
                self.log(f'        Sending out (@{self.ip:05}) → {self.parameter(1)}')
            if self._sender:
                self._sender(self.parameter(1), trace=trace)
            else:
                self._output.append(self.parameter(1))
        elif inst.dis_style == DisStyle.COND_JUMP:
            if inst.op(self.parameter(1)):
                self.ip = self.parameter(2)
                return
        elif inst.dis_style == DisStyle.RELATIVE:
            self._relative_base += self.parameter(1)
            if trace:
                self.log(f'        Relative base now: @{self._relative_base}')
        elif inst.dis_style == DisStyle.NO_PARAM:
            raise GeneratorExit(f'Halt at {self.ip}')
        self.ip += inst.length

    def simulate(self, inputs=None, trace=False, verbose=False):
        self._verbose = verbose
        self.log('Begin simulation' + (f' with default inputs {inputs}' if inputs is not None else ''))
        if inputs:
            self._input.extendleft(inputs)
        while self.ip < len(self.core):
            if trace:
                inst = self.current_instruction()
                self.log(f'{self.ip:05} : {self.opcode(inst, trace=trace)}')
            try:
                self.step(trace=trace)
            except GeneratorExit:
                break

    def disassemble(self, patch: str or None = None, start_at=None, end_at=None):
        end_at = self._setup_patched_dump(end_at, patch, start_at) + 1

        try:
            while self.ip < end_at:
                inst = self.current_instruction()
                print(f'{self.ip:05} : {self.opcode(inst)}')
                self.ip += inst.length
        except ValueError as exc:
            if not str(exc).startswith('Bad IP'):
                raise exc

    def dump(self, patch: str or None = None, start_at=None, end_at=None):
        end_at = self._setup_patched_dump(end_at, patch, start_at) + 1

        while self.ip < end_at:
            s = []
            for i in range(min(end_at - self.ip, 10)):
                s.append(f'{self.core[self.ip + i]:5}')
            print(f'{self.ip:05} : {" ".join(s)}')
            self.ip += len(s)

    def _setup_patched_dump(self, end_at, patch, start_at):
        if patch:
            for s in patch.split(','):
                a, v = [int(x) for x in s.split(':')]
                self.core[a] = v
        if start_at:
            self.ip = start_at
        if not end_at:
            end_at = len(self.core)
        return end_at
