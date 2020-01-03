import operator
import threading
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


class Processor(object):
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

    @property
    def all_output(self):
        return [v for v in self._output]

    def connect(self, receiver):
        self._sender = receiver

    def _join_comments(self, comments: list) -> str:
        comments = [c for c in comments if len(c.strip()) > 0]
        if len(comments) > 0:
            return '; ' + ', '.join(comments)
        return ''

    def opcode(self, instruction: OpCodes, trace=False):
        ip = self.ip
        op, *param = self.core[ip:ip + instruction.length]
        dump = f'{op:05} ' + " ".join(f'{v:5}' for v in param)
        comment = ''
        if instruction.dis_style == DisStyle.THREE_PARAM:
            ins = f'{self.parameter(3, True)} ← {self.parameter(1, True)} ' \
                  f'{instruction.instruction} {self.parameter(2, True)} '
            comment = self._join_comments([self.comment_parameter(1), self.comment_parameter(2)])
        elif instruction.dis_style == DisStyle.IN_PARAM:
            ins = f'{self.parameter(1, True, resolved=True)} ← {instruction.instruction}'
        elif instruction.dis_style == DisStyle.OUT_PARAM:
            ins = f'{instruction.instruction} ← {self.parameter(1, True)}'
            comment = self._join_comments([self.comment_parameter(1)])
        elif instruction.dis_style == DisStyle.COND_JUMP:
            ins = f'{instruction.instruction} ({self.parameter(1, True)}) {self.parameter(2, True)}'
            comment = self._join_comments([self.comment_parameter(1), self.comment_parameter(2)])
        elif instruction.dis_style == DisStyle.RELATIVE:
            ins = f'{instruction.instruction} {self.parameter(1, True)}'
            comment = self._join_comments([self.comment_parameter(1)])
        else:
            ins = 'HALT'
        return f'{dump:23} : {ins:25} {comment if trace else ""}'.strip()

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
        elif inst.dis_style == DisStyle.RELATIVE:
            self._relative_base += self.parameter(1)
            self.log(f' Relative base now: @{self._relative_base}')
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

    computer = Processor(initial_cells)

    print('Part 1')
    computer.simulate([1])
    print(f'PART 1 RESULT: {computer.all_output}')

    '''
Part 1

This part is testing that huge numbers can be used and that the execution of all the three different
addressing modes operate correctly.

Begin simulation with default inputs [1]
        Immediate mode multiplication of rather big numbers, saved in location 63
00000 : 01102 34463338 34463338    63 : [63] ← #34463338 MUL #34463338
        First check that the result of the multiplication isn't less than the original number because
        that would indicate an arithmetic overflow or a storage system with insufficient space.
        A 32-bit integer will store 34463338 as it is 26 bits wide.
        However, a 64-bit integer is needed to store 1187721666102244 as it is 51 bits wide.
00004 : 01007    63 34463338    63 : [63] ← [63] LT #34463338  ; [63]=1187721666102244
        If there was a fault, this jump would be performed
00008 : 01005    63    53       : JNZ ([63]) #53            ; [63]=0
        The big number support has been verified, and it is time to ensure that the relative addressing
        mode is handled correctly with the relative base index.
        
        Setup with location 1000 holding the value 3
00011 : 01101     3     0  1000 : [1000] ← #3 ADD #0
        Relative base starts out at 0, the RB instruction adds a value to the current relative base
        In immediate mode, it's a straight addition
00015 : 00109   988             : RB #988
        Relative base now: @988
        In relative mode, the value is picked up from the location pointed to by the current relative
        base offset by the parameter, in this case the location is 988+12 = 1000
00017 : 00209    12             : RB [rel+12]               ; [1000]=3
        Relative base now: @991
        In position mode, the value is pickup up from the location pointed to by the parameter, in this
        case the location is, again, 1000
00019 : 00009  1000             : RB [1000]                 ; [1000]=3
        Relative base now: @994
        A further couple of uses of relative mode which still picks up location 1000
00021 : 00209     6             : RB [rel+6]                ; [1000]=3
        Relative base now: @997
00023 : 00209     3             : RB [rel+3]                ; [1000]=3
        Relative base now: @1000
        If all the modifications to the relative base have been successful, then the input here will be
        stored in location 1000
00025 : 00203     0             : [1000] ← INP
        Waiting for input (@00025)
        Got 1
        If location 1000 holds 3 instead of 1, then the relative base calculations didn't work
00027 : 01008  1000     1    63 : [63] ← [1000] EQ #1       ; [1000]=1
        Jump if there was no failure
00031 : 01005    63    65       : JNZ ([63]) #65            ; [63]=1
        The relative base has now completed its test and been proved working.
        
00063 : ??                      : Working location
00064 : ??                      : Working location

        It's time to produce a code.
        Lots of setups to produce an initial table:
00065 : 01101    35     0  1007 : [1007] ← #35 ADD #0
00069 : 01102    30     1  1013 : [1013] ← #30 MUL #1
00073 : 01102    37     1  1017 : [1017] ← #37 MUL #1
00077 : 01101    23     0  1006 : [1006] ← #23 ADD #0
00081 : 01101     0    32  1008 : [1008] ← #0 ADD #32
00085 : 01102     1    29  1000 : [1000] ← #1 MUL #29
00089 : 01101     0    38  1010 : [1010] ← #0 ADD #38
00093 : 01101     0    24  1002 : [1002] ← #0 ADD #24
00097 : 01101    33     0  1003 : [1003] ← #33 ADD #0
00101 : 01101     1     0  1021 : [1021] ← #1 ADD #0
00105 : 01102    31     1  1019 : [1019] ← #31 MUL #1
00109 : 01101    27     0  1014 : [1014] ← #27 ADD #0
00113 : 01102    20     1  1005 : [1005] ← #20 MUL #1
00117 : 01101     0     0  1020 : [1020] ← #0 ADD #0
00121 : 01102     1   892  1027 : [1027] ← #1 MUL #892
00125 : 01101   895     0  1026 : [1026] ← #895 ADD #0
00129 : 01102    39     1  1015 : [1015] ← #39 MUL #1
00133 : 01102     1   370  1029 : [1029] ← #1 MUL #370
00137 : 01102     1    28  1001 : [1001] ← #1 MUL #28
00141 : 01102    34     1  1012 : [1012] ← #34 MUL #1
00145 : 01101    25     0  1016 : [1016] ← #25 ADD #0
00149 : 01101     0   375  1028 : [1028] ← #0 ADD #375
00153 : 01101    36     0  1018 : [1018] ← #36 ADD #0
00157 : 01101     0    21  1004 : [1004] ← #0 ADD #21
00161 : 01102     1    26  1009 : [1009] ← #1 MUL #26
00165 : 01101     0   249  1022 : [1022] ← #0 ADD #249
00169 : 01101     0   660  1025 : [1025] ← #0 ADD #660
00173 : 01101     0   665  1024 : [1024] ← #0 ADD #665
00177 : 01102     1    22  1011 : [1011] ← #1 MUL #22
00181 : 01102   242     1  1023 : [1023] ← #242 MUL #1
        Memory setup from preceding code:
            1000  29  28  24  33  21  29  23  35  32  26
            1010  38  22  34  30  27  39  25  37  36  31
            1020   0   1 249 242 665 660 895 892 375 370
            
00185 : 00109     5             : RB #5
        Relative base now: @1005
        Load scratch location 63 with the value at 1008 (32)
00187 : 02102     1     3    63 : [63] ← #1 MUL [rel+3]     ; [1008]=32
        Compare that value with 31 — it's not equal so store 0
00191 : 01008    63    31    63 : [63] ← [63] EQ #31        ; [63]=32
        If they were equal, then jump… they're not, so no jump this time
00195 : 01005    63   205       : JNZ ([63]) #205           ; [63]=0
        Add 1 to scratch location 64
00198 : 01001    64     1    64 : [64] ← [64] ADD #1        ; [64]=0
        Clever use of immediate mode to create an unconditional jump 
00202 : 01105     1   207       : JNZ (#1) #207

        Double up scratch location 64
00207 : 01002    64     2    64 : [64] ← [64] MUL #2        ; [64]=1
        Relative base is on the move…
00211 : 00109     8             : RB #8
        Relative base now: @1013
        Overwrite location (1013+5)=1018 with 40 (was 36)
00213 : 21102    40     1     5 : [rel+5] ← #40 MUL #1
        Now then, was that 37?
00217 : 01008  1018    37    63 : [63] ← [1018] EQ #37      ; [1018]=40
        No it wasn't, so no jumping
00221 : 01005    63   227       : JNZ ([63]) #227           ; [63]=0
        Make this jump instead
00224 : 01105     1   233       : JNZ (#1) #233

        Double scratch 64 again… is this a barrel shifter?
00233 : 01002    64     2    64 : [64] ← [64] MUL #2        ; [64]=2
00237 : 00109     7             : RB #7
        Relative base now: @1020
        Jump
00239 : 02105     1     3       : JNZ (#1) [rel+3]          ; [1023]=242

        Add a bit into scratch 64
00242 : 01001    64     1    64 : [64] ← [64] ADD #1        ; [64]=4
        Jump
00246 : 01106     0   251       : JZ (#0) #251

        Double scratch 64
00251 : 01002    64     2    64 : [64] ← [64] MUL #2        ; [64]=5
        Relative base can move negative amounts by adding a negative number
00255 : 00109    -7             : RB #-7
        Relative base now: @1013
        Load scratch 63 with the value at (1013-7)=1006, (23)
00257 : 01201    -7     0    63 : [63] ← [rel-7] ADD #0     ; [1006]=23
        Compare with 20
00261 : 01008    63    20    63 : [63] ← [63] EQ #20        ; [63]=23
        It's not 20, so don't jump
00265 : 01005    63   271       : JNZ ([63]) #271           ; [63]=0
        Jump
00268 : 01106     0   277       : JZ (#0) #277

        Double scratch 64
00277 : 01002    64     2    64 : [64] ← [64] MUL #2        ; [64]=10
00281 : 00109   -10             : RB #-10
        Relative base now: @1003
        Test if the value at (1003+0) equals 33 (it does)
00283 : 01208     0    33    63 : [63] ← [rel+0] EQ #33     ; [1003]=33
        The values were equal, so jump
00287 : 01005    63   295       : JNZ ([63]) #295           ; [63]=1

        Add in another bit to scratch 64 and shift it left again (multiply by 2)
00295 : 01001    64     1    64 : [64] ← [64] ADD #1        ; [64]=20
00299 : 01002    64     2    64 : [64] ← [64] MUL #2        ; [64]=21
00303 : 00109    -6             : RB #-6
        Relative base now: @997
        Test if the value at (997+4)=1001 is less than 27, it's not
00305 : 01207     4    27    63 : [63] ← [rel+4] LT #27     ; [1001]=28
        Don't jump
00309 : 01005    63   319       : JNZ ([63]) #319           ; [63]=0
        Add in another bit to scratch 64
00312 : 01001    64     1    64 : [64] ← [64] ADD #1        ; [64]=42
        Jump
00316 : 01105     1   321       : JNZ (#1) #321

        Shift scratch 64 left
00321 : 01002    64     2    64 : [64] ← [64] MUL #2        ; [64]=43
00325 : 00109    12             : RB #12
        Relative base now: @1009
00327 : 01207    -1    33    63 : [63] ← [rel-1] LT #33     ; [1008]=32
00331 : 01005    63   339       : JNZ ([63]) #339           ; [63]=1

00339 : 01001    64     1    64 : [64] ← [64] ADD #1        ; [64]=86
00343 : 01002    64     2    64 : [64] ← [64] MUL #2        ; [64]=87
00347 : 00109     6             : RB #6
        Relative base now: @1015
00349 : 01206     6   355       : JZ ([rel+6]) #355         ; [1021]=1
00352 : 01106     0   361       : JZ (#0) #361

00361 : 01002    64     2    64 : [64] ← [64] MUL #2        ; [64]=174
00365 : 00109    21             : RB #21
        Relative base now: @1036
        Jump to the location stored in (1036-8)=1028, which is 375
00367 : 02106     0    -8       : JZ (#0) [rel-8]           ; [1028]=375

00375 : 01001    64     1    64 : [64] ← [64] ADD #1        ; [64]=348
00379 : 01002    64     2    64 : [64] ← [64] MUL #2        ; [64]=349
00383 : 00109   -29             : RB #-29
        Relative base now: @1007
00385 : 01202     0     1    63 : [63] ← [rel+0] MUL #1     ; [1007]=35
00389 : 01008    63    36    63 : [63] ← [63] EQ #36        ; [63]=35
00393 : 01005    63   403       : JNZ ([63]) #403           ; [63]=0
00396 : 01001    64     1    64 : [64] ← [64] ADD #1        ; [64]=698
00400 : 01105     1   405       : JNZ (#1) #405

00405 : 01002    64     2    64 : [64] ← [64] MUL #2        ; [64]=699
00409 : 00109    11             : RB #11
        Relative base now: @1018
00411 : 21107    41    40    -6 : [rel-6] ← #41 LT #40
00415 : 01005  1012   421       : JNZ ([1012]) #421         ; [1012]=0
00418 : 01105     1   427       : JNZ (#1) #427

00427 : 01002    64     2    64 : [64] ← [64] MUL #2        ; [64]=1398
00431 : 00109   -11             : RB #-11
        Relative base now: @1007
00433 : 02101     0    -4    63 : [63] ← #0 ADD [rel-4]     ; [1003]=33
00437 : 01008    63    33    63 : [63] ← [63] EQ #33        ; [63]=33
00441 : 01005    63   453       : JNZ ([63]) #453           ; [63]=1

00453 : 01002    64     2    64 : [64] ← [64] MUL #2        ; [64]=2796
00457 : 00109    -7             : RB #-7
        Relative base now: @1000
00459 : 21108    42    40    10 : [rel+10] ← #42 EQ #40
00463 : 01005  1010   469       : JNZ ([1010]) #469         ; [1010]=0
00466 : 01105     1   475       : JNZ (#1) #475

00475 : 01002    64     2    64 : [64] ← [64] MUL #2        ; [64]=5592
00479 : 00109     1             : RB #1
        Relative base now: @1001
00481 : 01201     4     0    63 : [63] ← [rel+4] ADD #0     ; [1005]=20
00485 : 01008    63    20    63 : [63] ← [63] EQ #20        ; [63]=20
00489 : 01005    63   497       : JNZ ([63]) #497           ; [63]=1

00497 : 01001    64     1    64 : [64] ← [64] ADD #1        ; [64]=11184
00501 : 01002    64     2    64 : [64] ← [64] MUL #2        ; [64]=11185
00505 : 00109     5             : RB #5
        Relative base now: @1006
00507 : 21107    43    44     5 : [rel+5] ← #43 LT #44
00511 : 01005  1011   523       : JNZ ([1011]) #523         ; [1011]=1

00523 : 01002    64     2    64 : [64] ← [64] MUL #2        ; [64]=22370
00527 : 00109    20             : RB #20
        Relative base now: @1026
00529 : 21108    44    44    -7 : [rel-7] ← #44 EQ #44
00533 : 01005  1019   541       : JNZ ([1019]) #541         ; [1019]=1

00541 : 01001    64     1    64 : [64] ← [64] ADD #1        ; [64]=44740
00545 : 01002    64     2    64 : [64] ← [64] MUL #2        ; [64]=44741
00549 : 00109     2             : RB #2
        Relative base now: @1028
00551 : 01205    -8   561       : JNZ ([rel-8]) #561        ; [1020]=0
00554 : 01001    64     1    64 : [64] ← [64] ADD #1        ; [64]=89482
00558 : 01106     0   563       : JZ (#0) #563

00563 : 01002    64     2    64 : [64] ← [64] MUL #2        ; [64]=89483
00567 : 00109   -23             : RB #-23
        Relative base now: @1005
00569 : 02108    22     0    63 : [63] ← #22 EQ [rel+0]     ; [1005]=20
00573 : 01005    63   583       : JNZ ([63]) #583           ; [63]=0
00576 : 01001    64     1    64 : [64] ← [64] ADD #1        ; [64]=178966
00580 : 01105     1   585       : JNZ (#1) #585

00585 : 01002    64     2    64 : [64] ← [64] MUL #2        ; [64]=178967
00589 : 00109    -6             : RB #-6
        Relative base now: @999
00591 : 02107    30     1    63 : [63] ← #30 LT [rel+1]     ; [1000]=29
00595 : 01005    63   605       : JNZ ([63]) #605           ; [63]=0
00598 : 01001    64     1    64 : [64] ← [64] ADD #1        ; [64]=357934
00602 : 01105     1   607       : JNZ (#1) #607

00607 : 01002    64     2    64 : [64] ← [64] MUL #2        ; [64]=357935
00611 : 00109    23             : RB #23
        Relative base now: @1022
00613 : 01205    -1   621       : JNZ ([rel-1]) #621        ; [1021]=1

00621 : 01001    64     1    64 : [64] ← [64] ADD #1        ; [64]=715870
00625 : 01002    64     2    64 : [64] ← [64] MUL #2        ; [64]=715871
00629 : 00109   -19             : RB #-19
        Relative base now: @1003
00631 : 02102     1    -3    63 : [63] ← #1 MUL [rel-3]     ; [1000]=29
00635 : 01008    63    29    63 : [63] ← [63] EQ #29        ; [63]=29
00639 : 01005    63   647       : JNZ ([63]) #647           ; [63]=1

00647 : 01001    64     1    64 : [64] ← [64] ADD #1        ; [64]=1431742
00651 : 01002    64     2    64 : [64] ← [64] MUL #2        ; [64]=1431743
00655 : 00109    28             : RB #28
        Relative base now: @1031
00657 : 02105     1    -7       : JNZ (#1) [rel-7]          ; [1024]=665

00665 : 01001    64     1    64 : [64] ← [64] ADD #1        ; [64]=2863486
00669 : 01002    64     2    64 : [64] ← [64] MUL #2        ; [64]=2863487
00673 : 00109   -17             : RB #-17
        Relative base now: @1014
00675 : 01206     6   687       : JZ ([rel+6]) #687         ; [1020]=0

00687 : 01002    64     2    64 : [64] ← [64] MUL #2        ; [64]=5726974
00691 : 00109     2             : RB #2
        Relative base now: @1016
00693 : 21101    45     0     1 : [rel+1] ← #45 ADD #0
00697 : 01008  1017    42    63 : [63] ← [1017] EQ #42      ; [1017]=45
00701 : 01005    63   707       : JNZ ([63]) #707           ; [63]=0
00704 : 01106     0   713       : JZ (#0) #713

00713 : 01002    64     2    64 : [64] ← [64] MUL #2        ; [64]=11453948
00717 : 00109    -6             : RB #-6
        Relative base now: @1010
00719 : 02101     0    -3    63 : [63] ← #0 ADD [rel-3]     ; [1007]=35
00723 : 01008    63    34    63 : [63] ← [63] EQ #34        ; [63]=35
00727 : 01005    63   733       : JNZ ([63]) #733           ; [63]=0
00730 : 01105     1   739       : JNZ (#1) #739

00739 : 01002    64     2    64 : [64] ← [64] MUL #2        ; [64]=22907896
00743 : 00109     3             : RB #3
        Relative base now: @1013
00745 : 21101    46     0     1 : [rel+1] ← #46 ADD #0
00749 : 01008  1014    46    63 : [63] ← [1014] EQ #46      ; [1014]=46
00753 : 01005    63   761       : JNZ ([63]) #761           ; [63]=1

00761 : 01001    64     1    64 : [64] ← [64] ADD #1        ; [64]=45815792
00765 : 01002    64     2    64 : [64] ← [64] MUL #2        ; [64]=45815793
00769 : 00109     5             : RB #5
        Relative base now: @1018
00771 : 21102    47     1    -7 : [rel-7] ← #47 MUL #1
00775 : 01008  1011    47    63 : [63] ← [1011] EQ #47      ; [1011]=47
00779 : 01005    63   787       : JNZ ([63]) #787           ; [63]=1

00787 : 01001    64     1    64 : [64] ← [64] ADD #1        ; [64]=91631586
00791 : 01002    64     2    64 : [64] ← [64] MUL #2        ; [64]=91631587
00795 : 00109   -24             : RB #-24
        Relative base now: @994
00797 : 02108    24     8    63 : [63] ← #24 EQ [rel+8]     ; [1002]=24
00801 : 01005    63   813       : JNZ ([63]) #813           ; [63]=1

00813 : 01002    64     2    64 : [64] ← [64] MUL #2        ; [64]=183263174
00817 : 00109     5             : RB #5
        Relative base now: @999
00819 : 01208    10    29    63 : [63] ← [rel+10] EQ #29    ; [1009]=26
00823 : 01005    63   829       : JNZ ([63]) #829           ; [63]=0
00826 : 01105     1   835       : JNZ (#1) #835

00835 : 01002    64     2    64 : [64] ← [64] MUL #2        ; [64]=366526348
00839 : 00109     7             : RB #7
        Relative base now: @1006
00841 : 02107    23    -4    63 : [63] ← #23 LT [rel-4]     ; [1002]=24
00845 : 01005    63   853       : JNZ ([63]) #853           ; [63]=1

00853 : 01001    64     1    64 : [64] ← [64] ADD #1        ; [64]=733052696
00857 : 01002    64     2    64 : [64] ← [64] MUL #2        ; [64]=733052697
00861 : 00109    -2             : RB #-2
        Relative base now: @1004
00863 : 01202     0     1    63 : [63] ← [rel+0] MUL #1     ; [1004]=21
00867 : 01008    63    21    63 : [63] ← [63] EQ #21        ; [63]=21
00871 : 01005    63   879       : JNZ ([63]) #879           ; [63]=1

00879 : 01001    64     1    64 : [64] ← [64] ADD #1        ; [64]=1466105394
00883 : 01002    64     2    64 : [64] ← [64] MUL #2        ; [64]=1466105395
00887 : 00109    15             : RB #15
        Relative base now: @1019
00889 : 02106     0     8       : JZ (#0) [rel+8]           ; [1027]=892

00892 : 01106     0   901       : JZ (#0) #901

00901 : 00004    64             : OUT ← [64]                ; [64]=2932210790
        Sending out (@00901) → 2932210790
00903 : 00099                   : HALT
    '''

    print('Part 2')
    computer.reset_core()
    computer.simulate([2], trace=False, verbose=False)
    # print('\n'.join(computer.get_log()))
    print(f'PART 2 RESULT: {computer.all_output}')
