from collections import defaultdict
from typing import List


class LogicParam(object):
    def __init__(self, param: str):
        self._link = None
        self._val = None
        if param.isdigit():
            self._val = int(param)
        else:
            self._link = param

    @property
    def is_val(self):
        return self._val is not None

    @property
    def link(self):
        return self._link

    @property
    def val(self):
        return self._val

    def __repr__(self):
        return f'{self.__class__.__name__}({self._link if self._link is not None else self._val})'

    def __str__(self):
        return f'{self._link}' if self._link is not None else f'#{self._val}'


def nop(val, _):
    return val


nop.name = 'nop'


def op_load(val, _):
    return val


op_load.name = 'op_load'


def op_and(left, right):
    return left & right


op_and.name = 'op_and'


def op_or(left, right):
    return left | right


op_or.name = 'op_name'


def op_not(val, _):
    return ~ val


op_not.name = 'op_name'


def op_lshift(left, right):
    return left << right


op_lshift.name = 'op_lshift'


def op_rshift(left, right):
    return left >> right


op_rshift.name = 'op_rshift'


class BaseLogic(object):
    def __init__(self, name: str, params: List[str]):
        self._name: str = name
        self.left: LogicParam or None = None
        self.right: LogicParam or None = None
        self.function = nop
        self.param_count: int = 0
        self.val = None
        if len(params) == 1:
            self.left = LogicParam(params[0])
            self.function = op_load
            self.param_count = 1
        elif len(params) == 2:
            if params[0] == 'NOT':
                self.left = LogicParam(params[1])
                self.function = op_not
                self.param_count = 1
            else:
                raise TypeError(f'Unitary operation not recognised: {params[0]}')
        elif len(params) == 3:
            if params[1] == 'AND':
                self.function = op_and
            elif params[1] == 'OR':
                self.function = op_or
            elif params[1] == 'LSHIFT':
                self.function = op_lshift
            elif params[1] == 'RSHIFT':
                self.function = op_rshift
            else:
                raise TypeError(f'Unknown operator {params[1]}')
            self.left = LogicParam(params[0])
            self.right = LogicParam(params[2])
            self.param_count = 2
        else:
            raise TypeError(f'Unknown sequence: {" ".join(params)}')

    def _params_repr(self):
        res = []
        if self.left is not None:
            res.append(f'left: {self.left.__str__()}')
        if self.right is not None:
            res.append(f'right: {self.right.__str__()}')
        return ','.join(res)

    def __repr__(self):
        return f'{self.__class__.__name__}(name: {self._name}, fn: {self.function.name}, {self._params_repr()})'


def calc(sig: str, indent: str = ''):
    print(f'{indent}Enter {sig}')
    signal = signals[sig]
    if signal.val is None:
        left = right = 0
        if signal.param_count >= 1:
            if signal.left.is_val:
                left = signal.left.val
            else:
                left = calc(signal.left.link, indent + ' ')
        if signal.param_count >= 2:
            if signal.right.is_val:
                right = signal.right.val
            else:
                right = calc(signal.right.link, indent + ' ')
        signal.val = signal.function(left, right)
    result = signal.val
    print(f'{indent}Exit {sig} ({result})')
    return result


with open('input') as f:
    logic = [line.strip().split(' -> ') for line in f.readlines()]

signals = defaultdict(BaseLogic)

# create signal list
for line in logic:
    inst, targ = line
    signals[targ] = BaseLogic(targ, inst.split())

part1 = calc('a')

# reset circuit
for sig in signals.values():
    sig.val = None

signals['b'].val = part1

part2 = calc('a')

print(f'Part 1: {part1}')
print(f'Part 2: {part2}')

# pprint(signals)
'''
Part 1: 956
Part 2: 40149
'''
