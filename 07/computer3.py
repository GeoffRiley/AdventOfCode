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
    def __init__(self, mem_str: str, name: str = 'Intcode'):
        self.name = name
        self._log = []
        self._core = []
        self._mem_str = mem_str
        self._ip = 0
        self._input = deque()
        self._output = list()
        self.reset_core()
        self._sender = None

    def reset_core(self):
        self._log.clear()
        self._core = prepare_mem(self._mem_str)
        self._input.clear()
        self._output.clear()
        self._ip = 0

    def log(self, msg):
        self._log.append(msg)

    def get_log(self):
        return self._log

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

    def connect(self, receiver):
        self._sender = receiver

    def opcode(self, instruction: OpCodes, trace=False):
        ip = self.ip
        op, *param = self.core[ip:ip + instruction.length]
        dump = f'{op:05} ' + " ".join(f'{v:5}' for v in param)
        comment = ''
        if instruction.dis_style == DisStyle.THREE_PARAM:
            ins = f'{self.parameter(3, True)} ← {self.parameter(1, True)} ' \
                  f'{instruction.instruction} {self.parameter(2, True)} '
            comment = f'; {self.parameter(1, True)}={self.parameter(1)}, {self.parameter(2, True)}={self.parameter(2)}'
        elif instruction.dis_style == DisStyle.IN_PARAM:
            ins = f'{self.parameter(1, True)} ← {instruction.instruction}'
        elif instruction.dis_style == DisStyle.OUT_PARAM:
            ins = f'{instruction.instruction} ← {self.parameter(1, True)}'
            comment = f'; {self.parameter(1, True)}={self.parameter(1)}'
        elif instruction.dis_style == DisStyle.COND_JUMP:
            ins = f'{instruction.instruction} ({self.parameter(1, True)}) {self.parameter(2, True)}'
            comment = f'; {self.parameter(1, True)}={self.parameter(1)}, ; {self.parameter(2, True)}={self.parameter(2)}'
        else:
            ins = 'HALT'
        return f'{dump:23} : {ins:20} {comment if trace else ""}'.strip()

    def _wait_for_input(self):
        self.log(f'Waiting for input (@{self.ip:05})')
        while len(self._input) == 0:
            sleep(0.0001)
        inp = self._input.pop()
        self.log(f'Got {inp}')
        return inp

    def step(self):
        inst = self.current_instruction()
        if inst.dis_style == DisStyle.THREE_PARAM:
            self.core[self.parameter(3, target=True)] = inst.op(self.parameter(1), self.parameter(2))
        elif inst.dis_style == DisStyle.IN_PARAM:
            self.core[self.parameter(1, target=True)] = self._wait_for_input()
        elif inst.dis_style == DisStyle.OUT_PARAM:
            self.log(f'Sending out (@{self.ip:05}) → {self.parameter(1)}')
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
        self.log('Begin simulation' + (f' with default inputs {inputs}' if inputs is not None else ''))
        if inputs:
            self._input.extendleft(inputs)
        while self.ip < len(self.core):
            if trace:
                inst = self.current_instruction()
                self.log(f'{self.ip:05} : {self.opcode(inst, trace=trace)}')
            try:
                self.step()
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


class Amplifier(object):
    def __init__(self, mem_str: str):
        self._amps = [Processor(mem_str, name=f'Amp {n + 1}') for n in range(5)]

    def run(self, inputs: str or list, trace=False, quiet=True):
        out = 0
        p = self._amps[0]
        if isinstance(inputs, str):
            inputs = [int(v) for v in inputs.split(',')]
        for inp in inputs:
            p.reset_core()
            p.simulate([inp, out], trace=trace)
            out = p.output[0]
        if not quiet:
            for p in self._amps:
                msg = f'{p.name} log:'
                print("*" * (len(msg) + 4))
                print(f'* {msg} *')
                print("*" * (len(msg) + 4))
                print('\n'.join(p.get_log()))
        return out

    def run_regeneration(self, inputs: str or list, trace=False, quiet=True):
        if isinstance(inputs, str):
            inputs = [int(v) for v in inputs.split(',')]
        p = self._amps[0]
        p.reset_core()
        for n in self._amps[1:]:
            p.connect(n.receiver)
            p = n
            p.reset_core()
        self._amps[-1].connect(self._amps[0].receiver)
        threads = []
        for a, n in zip(self._amps, inputs):
            a.receiver(n)
            t = threading.Thread(target=a.simulate, kwargs={'trace': trace})
            threads.append(t)
            t.start()
        self._amps[0].receiver(0)
        while any(t.is_alive() for t in threads):
            sleep(0.0001)
        if not quiet:
            for p in self._amps:
                msg = f'{p.name} log:'
                print("*" * (len(msg) + 4))
                print(f'* {msg} *')
                print("*" * (len(msg) + 4))
                print('\n'.join(p.get_log()))

        return self._amps[0]._input.pop()


if __name__ == '__main__':
    with open('input') as f:
        initial_cells = f.read()

    computer = Amplifier(initial_cells)

    print('Part 1')
    res = []
    for inp in itertools.permutations(range(5)):
        res.append((inp, computer.run(inp, trace=False)))
    print(f'PART 1 RESULT: {max(res, key=lambda x: x[1])[1]}')

    print('Part 2')
    res = []
    for inp in itertools.permutations(range(5, 10)):
        # print(f'Input sequence: {str(inp)}')
        res.append((inp, computer.run_regeneration(inp, trace=False)))
    print(f'PART 2 RESULT: {max(res, key=lambda x: x[1])[1]}')

    '''
    The first value passed to the 'amplifier' sets a location into a jump table,
    (in C parlance it's a 'switch' statement)
    '''
    # computer = Processor(initial_cells)
    # computer.disassemble(end_at=8)
    '''
    00000 : 00003     8             : [8] ← INP
    00002 : 01001     8    10     8 : [8] ← [8] ADD #10    ; [8]=0, #10=10
    00006 : 00105     1     0       : JNZ (#1) [0]         ; #1=1, ; [0]=3
    
    Location 00009 is the general purpose storage location used throughout the amplifier
    '''
    # computer.dump(start_at=9, end_at=9)
    '''
    00009 :    00
    
    The table of addresses for the 'switch' @00006 take up ten bytes from 10 to 19:
    '''
    # computer.dump(start_at=10, end_at=19)
    '''
    00010 :    21    42    67    84   109   122   203   284   365   446
    
    So the individual routines start at different location.
    
    Amp function 0:
    result = (((IN * 3) + 5) * 4) + 3
           = 12 * IN + 23
    '''
    # computer.disassemble(start_at=21, end_at=41)
    '''
    00021 : 00003     9             : [9] ← INP
    00023 : 01002     9     3     9 : [9] ← [9] MUL #3
    00027 : 01001     9     5     9 : [9] ← [9] ADD #5
    00031 : 00102     4     9     9 : [9] ← #4 MUL [9]
    00035 : 01001     9     3     9 : [9] ← [9] ADD #3
    00039 : 00004     9             : OUT ← [9]
    00041 : 00099                   : HALT
    
    Amp function 1:
    result = ((((IN + 5) * 3) + 4) * 3) + 3
           = 9 * IN + 60
    '''
    # computer.disassemble(start_at=42, end_at=66)
    '''
    00042 : 00003     9             : [9] ← INP
    00044 : 01001     9     5     9 : [9] ← [9] ADD #5
    00048 : 01002     9     3     9 : [9] ← [9] MUL #3
    00052 : 01001     9     4     9 : [9] ← [9] ADD #4
    00056 : 00102     3     9     9 : [9] ← #3 MUL [9]
    00060 : 00101     3     9     9 : [9] ← #3 ADD [9]
    00064 : 00004     9             : OUT ← [9]
    00066 : 00099                   : HALT
    
    Amp function 2:
    result = ((IN + 5) * 3) + 5
           = 3 * N + 20
    '''
    # computer.disassemble(start_at=67, end_at=83)
    '''
    00067 : 00003     9             : [9] ← INP
    00069 : 00101     5     9     9 : [9] ← #5 ADD [9]
    00073 : 01002     9     3     9 : [9] ← [9] MUL #3
    00077 : 00101     5     9     9 : [9] ← #5 ADD [9]
    00081 : 00004     9             : OUT ← [9]
    00083 : 00099                   : HALT
    
    Amp function 3:
    result = ((((IN * 5) + 5) * 3) + 3) * 2
           = 30 * IN + 36
    '''
    # computer.disassemble(start_at=84, end_at=108)
    '''
    00084 : 00003     9             : [9] ← INP
    00086 : 00102     5     9     9 : [9] ← #5 MUL [9]
    00090 : 00101     5     9     9 : [9] ← #5 ADD [9]
    00094 : 00102     3     9     9 : [9] ← #3 MUL [9]
    00098 : 00101     3     9     9 : [9] ← #3 ADD [9]
    00102 : 00102     2     9     9 : [9] ← #2 MUL [9]
    00106 : 00004     9             : OUT ← [9]
    00108 : 00099                   : HALT
    
    Amp function 4:
    result = (IN +2 ) * 3
           = 3 * IN + 6
    '''
    # computer.disassemble(start_at=109, end_at=121)
    '''
    00109 : 00003     9             : [9] ← INP
    00111 : 00101     2     9     9 : [9] ← #2 ADD [9]
    00115 : 01002     9     3     9 : [9] ← [9] MUL #3
    00119 : 00004     9             : OUT ← [9]
    00121 : 00099                   : HALT
    
    The second set of functions pass a sequence of ten values in and out through a sequence of calls,
    this allows an array of processors to run through a calculation built upon the ordering of the 
    amplifiers. 
    
    Amp function 5:
    results = (IN0 + 2, 
               IN1 + 1, 
               IN2 + 1,
               IN3 + 1,
               IN4 + 1,
               IN5 * 2,
               IN6 * 2,
               IN7 + 2,
               IN8 + 1,
               IN9 * 2)
    '''
    # computer.disassemble(start_at=122, end_at=202)
    '''
    00122 : 00003     9             : [9] ← INP
    00124 : 00101     2     9     9 : [9] ← #2 ADD [9]
    00128 : 00004     9             : OUT ← [9]
    00130 : 00003     9             : [9] ← INP
    00132 : 00101     1     9     9 : [9] ← #1 ADD [9]
    00136 : 00004     9             : OUT ← [9]
    00138 : 00003     9             : [9] ← INP
    00140 : 00101     1     9     9 : [9] ← #1 ADD [9]
    00144 : 00004     9             : OUT ← [9]
    00146 : 00003     9             : [9] ← INP
    00148 : 01001     9     1     9 : [9] ← [9] ADD #1
    00152 : 00004     9             : OUT ← [9]
    00154 : 00003     9             : [9] ← INP
    00156 : 00101     1     9     9 : [9] ← #1 ADD [9]
    00160 : 00004     9             : OUT ← [9]
    00162 : 00003     9             : [9] ← INP
    00164 : 01002     9     2     9 : [9] ← [9] MUL #2
    00168 : 00004     9             : OUT ← [9]
    00170 : 00003     9             : [9] ← INP
    00172 : 01002     9     2     9 : [9] ← [9] MUL #2
    00176 : 00004     9             : OUT ← [9]
    00178 : 00003     9             : [9] ← INP
    00180 : 01001     9     2     9 : [9] ← [9] ADD #2
    00184 : 00004     9             : OUT ← [9]
    00186 : 00003     9             : [9] ← INP
    00188 : 00101     1     9     9 : [9] ← #1 ADD [9]
    00192 : 00004     9             : OUT ← [9]
    00194 : 00003     9             : [9] ← INP
    00196 : 01002     9     2     9 : [9] ← [9] MUL #2
    00200 : 00004     9             : OUT ← [9]
    00202 : 00099                   : HALT
    
    Amp function 6:
    results = (IN0 + 1, 
               IN1 + 2, 
               IN2 * 2,
               IN3 + 1,
               IN4 * 2,
               IN5 + 1,
               IN6 + 1,
               IN7 * 2,
               IN8 + 2,
               IN9 * 2)
    '''
    # computer.disassemble(start_at=203, end_at=283)
    '''
    00203 : 00003     9             : [9] ← INP
    00205 : 01001     9     1     9 : [9] ← [9] ADD #1
    00209 : 00004     9             : OUT ← [9]
    00211 : 00003     9             : [9] ← INP
    00213 : 00101     2     9     9 : [9] ← #2 ADD [9]
    00217 : 00004     9             : OUT ← [9]
    00219 : 00003     9             : [9] ← INP
    00221 : 00102     2     9     9 : [9] ← #2 MUL [9]
    00225 : 00004     9             : OUT ← [9]
    00227 : 00003     9             : [9] ← INP
    00229 : 00101     1     9     9 : [9] ← #1 ADD [9]
    00233 : 00004     9             : OUT ← [9]
    00235 : 00003     9             : [9] ← INP
    00237 : 00102     2     9     9 : [9] ← #2 MUL [9]
    00241 : 00004     9             : OUT ← [9]
    00243 : 00003     9             : [9] ← INP
    00245 : 01001     9     1     9 : [9] ← [9] ADD #1
    00249 : 00004     9             : OUT ← [9]
    00251 : 00003     9             : [9] ← INP
    00253 : 00101     1     9     9 : [9] ← #1 ADD [9]
    00257 : 00004     9             : OUT ← [9]
    00259 : 00003     9             : [9] ← INP
    00261 : 01002     9     2     9 : [9] ← [9] MUL #2
    00265 : 00004     9             : OUT ← [9]
    00267 : 00003     9             : [9] ← INP
    00269 : 00101     2     9     9 : [9] ← #2 ADD [9]
    00273 : 00004     9             : OUT ← [9]
    00275 : 00003     9             : [9] ← INP
    00277 : 01002     9     2     9 : [9] ← [9] MUL #2
    00281 : 00004     9             : OUT ← [9]
    00283 : 00099                   : HALT
    
    Amp function 7:
    results = (IN0 + 2, 
               IN1 + 2, 
               IN2 + 2,
               IN3 + 1,
               IN4 + 1,
               IN5 * 2,
               IN6 * 2,
               IN7 * 2,
               IN8 + 2,
               IN9 + 1)
    '''
    # computer.disassemble(start_at=284, end_at=364)
    '''
    00284 : 00003     9             : [9] ← INP
    00286 : 00101     2     9     9 : [9] ← #2 ADD [9]
    00290 : 00004     9             : OUT ← [9]
    00292 : 00003     9             : [9] ← INP
    00294 : 00101     2     9     9 : [9] ← #2 ADD [9]
    00298 : 00004     9             : OUT ← [9]
    00300 : 00003     9             : [9] ← INP
    00302 : 00101     2     9     9 : [9] ← #2 ADD [9]
    00306 : 00004     9             : OUT ← [9]
    00308 : 00003     9             : [9] ← INP
    00310 : 00101     1     9     9 : [9] ← #1 ADD [9]
    00314 : 00004     9             : OUT ← [9]
    00316 : 00003     9             : [9] ← INP
    00318 : 00101     1     9     9 : [9] ← #1 ADD [9]
    00322 : 00004     9             : OUT ← [9]
    00324 : 00003     9             : [9] ← INP
    00326 : 00102     2     9     9 : [9] ← #2 MUL [9]
    00330 : 00004     9             : OUT ← [9]
    00332 : 00003     9             : [9] ← INP
    00334 : 01002     9     2     9 : [9] ← [9] MUL #2
    00338 : 00004     9             : OUT ← [9]
    00340 : 00003     9             : [9] ← INP
    00342 : 01002     9     2     9 : [9] ← [9] MUL #2
    00346 : 00004     9             : OUT ← [9]
    00348 : 00003     9             : [9] ← INP
    00350 : 00101     2     9     9 : [9] ← #2 ADD [9]
    00354 : 00004     9             : OUT ← [9]
    00356 : 00003     9             : [9] ← INP
    00358 : 01001     9     1     9 : [9] ← [9] ADD #1
    00362 : 00004     9             : OUT ← [9]
    00364 : 00099                   : HALT
    
    Amp function 8:
    results = (IN0 + 1,
               IN1 + 1, 
               IN2 * 2,
               IN3 * 2,
               IN4 + 2,
               IN5 + 1,
               IN6 + 2,
               IN7 * 2,
               IN8 * 2,
               IN9 * 2)
    '''
    # computer.disassemble(start_at=365, end_at=445)
    '''
    00365 : 00003     9             : [9] ← INP
    00367 : 01001     9     1     9 : [9] ← [9] ADD #1
    00371 : 00004     9             : OUT ← [9]
    00373 : 00003     9             : [9] ← INP
    00375 : 00101     1     9     9 : [9] ← #1 ADD [9]
    00379 : 00004     9             : OUT ← [9]
    00381 : 00003     9             : [9] ← INP
    00383 : 00102     2     9     9 : [9] ← #2 MUL [9]
    00387 : 00004     9             : OUT ← [9]
    00389 : 00003     9             : [9] ← INP
    00391 : 01002     9     2     9 : [9] ← [9] MUL #2
    00395 : 00004     9             : OUT ← [9]
    00397 : 00003     9             : [9] ← INP
    00399 : 01001     9     2     9 : [9] ← [9] ADD #2
    00403 : 00004     9             : OUT ← [9]
    00405 : 00003     9             : [9] ← INP
    00407 : 01001     9     1     9 : [9] ← [9] ADD #1
    00411 : 00004     9             : OUT ← [9]
    00413 : 00003     9             : [9] ← INP
    00415 : 01001     9     2     9 : [9] ← [9] ADD #2
    00419 : 00004     9             : OUT ← [9]
    00421 : 00003     9             : [9] ← INP
    00423 : 01002     9     2     9 : [9] ← [9] MUL #2
    00427 : 00004     9             : OUT ← [9]
    00429 : 00003     9             : [9] ← INP
    00431 : 01002     9     2     9 : [9] ← [9] MUL #2
    00435 : 00004     9             : OUT ← [9]
    00437 : 00003     9             : [9] ← INP
    00439 : 00102     2     9     9 : [9] ← #2 MUL [9]
    00443 : 00004     9             : OUT ← [9]
    00445 : 00099                   : HALT
    
    Amp function 9:
    results = (IN0 * 2,
               IN1 * 2, 
               IN2 + 2,
               IN3 + 2,
               IN4 + 1,
               IN5 * 2,
               IN6 + 1,
               IN7 + 2,
               IN8 * 2,
               IN9 + 1)
    '''
    # computer.disassemble(start_at=446)
    '''
    00446 : 00003     9             : [9] ← INP
    00448 : 00102     2     9     9 : [9] ← #2 MUL [9]
    00452 : 00004     9             : OUT ← [9]
    00454 : 00003     9             : [9] ← INP
    00456 : 01002     9     2     9 : [9] ← [9] MUL #2
    00460 : 00004     9             : OUT ← [9]
    00462 : 00003     9             : [9] ← INP
    00464 : 00101     2     9     9 : [9] ← #2 ADD [9]
    00468 : 00004     9             : OUT ← [9]
    00470 : 00003     9             : [9] ← INP
    00472 : 00101     2     9     9 : [9] ← #2 ADD [9]
    00476 : 00004     9             : OUT ← [9]
    00478 : 00003     9             : [9] ← INP
    00480 : 00101     1     9     9 : [9] ← #1 ADD [9]
    00484 : 00004     9             : OUT ← [9]
    00486 : 00003     9             : [9] ← INP
    00488 : 01002     9     2     9 : [9] ← [9] MUL #2
    00492 : 00004     9             : OUT ← [9]
    00494 : 00003     9             : [9] ← INP
    00496 : 00101     1     9     9 : [9] ← #1 ADD [9]
    00500 : 00004     9             : OUT ← [9]
    00502 : 00003     9             : [9] ← INP
    00504 : 01001     9     2     9 : [9] ← [9] ADD #2
    00508 : 00004     9             : OUT ← [9]
    00510 : 00003     9             : [9] ← INP
    00512 : 00102     2     9     9 : [9] ← #2 MUL [9]
    00516 : 00004     9             : OUT ← [9]
    00518 : 00003     9             : [9] ← INP
    00520 : 00101     1     9     9 : [9] ← #1 ADD [9]
    00524 : 00004     9             : OUT ← [9]
    00526 : 00099                   : HALT
    '''
