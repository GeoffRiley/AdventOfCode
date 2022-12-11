"""
Advent of code 2022
Day 11: Monkey in the Middle
"""
from collections import defaultdict, deque
from dataclasses import dataclass
from math import prod
from operator import mul
from textwrap import dedent
from typing import List, Callable, Optional

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list, extract_ints


@dataclass
class Monkey:
    num: int
    initial_items: List[int]
    operation: str
    test: str
    true_target: int
    false_target: int
    _item_queue: deque = None
    _op_func: Callable = None
    _test_func: Callable = None

    def __post_init__(self):
        self._item_queue = deque(self.initial_items)
        self._make_op_func()
        self._make_test_func()

    def _make_op_func(self):
        func: Optional[Callable] = None
        parts = self.operation.split()
        assert parts[0] == 'new'
        assert parts[1] == '='
        assert parts[2] == 'old'
        assert parts[3] in '+*'
        if parts[3] == '+':
            # add
            if parts[4].isdecimal():
                func = eval(f'lambda x: x + {parts[4]}')
            elif parts[4] == 'old':
                func = lambda x: x * 2  # noqa: E731
        else:
            # multiply
            if parts[4].isdecimal():
                func = eval(f'lambda x: x * {parts[4]}')
            elif parts[4] == 'old':
                func = lambda x: x ** 2  # noqa: E731
        self._op_func = func

    def _make_test_func(self):
        parts = self.test.split()
        assert parts[0] == 'divisible'
        assert parts[1] == 'by'
        self._divisor = int(parts[2])
        self._test_func = eval(f'lambda x: (x % {self._divisor}) == 0')

    @property
    def divisor(self):
        return self._divisor

    @property
    def queue(self):
        return str(list(self._item_queue))

    @property
    def has_items(self):
        return len(self._item_queue) > 0

    @property
    def next_item(self):
        element = self._item_queue.popleft()
        return self._op_func(element)

    def target_for(self, item):
        if self._test_func(item):
            return self.true_target
        else:
            return self.false_target

    def add_item(self, new_item: int) -> 'Monkey':
        self._item_queue.append(new_item)
        return self


def parse_monkey(monkey_desc: List[str]) -> Monkey:
    """
        Given a list of strings in the format:
            Monkey 0:
              Starting initial_items: 79, 98
              Operation: new = old * 19
              Test: divisible by 23
                If true: throw to monkey 2
                If false: throw to monkey 3
        create an appropriate Monkey object
    """
    num = -1
    items = []
    operation = ''
    test = ''
    true_target = -1
    false_target = -1
    for line in monkey_desc:
        line_id: str
        line_id, *parts = line.strip().split(':')
        if line_id.startswith('Monkey'):
            num = int(line_id.split()[-1])
            continue
        if line_id.startswith('Starting'):
            items = extract_ints(parts[0])
            continue
        if line_id.startswith('Operation'):
            operation = parts[0].strip()
            continue
        if line_id.startswith('Test'):
            test = parts[0].strip()
            continue
        if line_id.startswith('If true'):
            true_target = int(parts[0].split()[-1])
            continue
        if line_id.startswith('If false'):
            false_target = int(parts[0].split()[-1])
            continue
        raise SyntaxError(f'Unrecognised monkey line: {line}')

    return Monkey(num, items, operation, test, true_target, false_target)


def part1(monkeys: List[List[str]]) -> int:
    """
    """
    monkey_list = [parse_monkey(mon) for mon in monkeys]
    monkey_inspections = defaultdict(int)

    for a_round in range(20):
        for monkey in monkey_list:
            a_monkey = monkey.num
            while monkey.has_items:
                monkey_inspections[a_monkey] += 1
                item = monkey.next_item // 3
                target = monkey.target_for(item)
                monkey_list[target].add_item(item)
        # print(f"*** ROUND {a_round+1} ***")
        # for monkey in monkey_list:
        #     print(f"   Monkey {monkey.num}: {monkey.queue}; Inspections: {monkey_inspections[monkey.num]}")

    return int(mul(*(sorted(monkey_inspections.values())[-2:])))


def part2(monkeys: List[List[str]]) -> int:
    """
    """
    monkey_list = [parse_monkey(mon) for mon in monkeys]
    # We'll need a common divisor to keep things manageable.  The product of the individual
    # divisors will be splendid! (They're all prime numbers and all different so there's no
    # lower common denominator to work out.)
    divisor = prod(m.divisor for m in monkey_list)
    monkey_inspections = defaultdict(int)

    for a_round in range(10000):
        for monkey in monkey_list:
            a_monkey = monkey.num
            while monkey.has_items:
                monkey_inspections[a_monkey] += 1
                item = monkey.next_item % divisor
                target = monkey.target_for(item)
                monkey_list[target].add_item(item)
        # if (a_round + 1) in [1, 20, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]:
        #     print(f"*** ROUND {a_round+1} ***")
        #     for monkey in monkey_list:
        #         print(f"   Monkey inspected items {monkey_inspections[monkey.num]} times.")

    return int(mul(*(sorted(monkey_inspections.values())[-2:])))


def main():
    loader = LoaderLib(2022)
    testing = False

    if not testing:
        input_text = loader.get_aoc_input(11)
    else:
        input_text = dedent('''\
            Monkey 0:
              Starting initial_items: 79, 98
              Operation: new = old * 19
              Test: divisible by 23
                If true: throw to monkey 2
                If false: throw to monkey 3
    
            Monkey 1:
              Starting initial_items: 54, 65, 75, 74
              Operation: new = old + 6
              Test: divisible by 19
                If true: throw to monkey 2
                If false: throw to monkey 0
    
            Monkey 2:
              Starting initial_items: 79, 60, 97
              Operation: new = old * old
              Test: divisible by 13
                If true: throw to monkey 1
                If false: throw to monkey 3
    
            Monkey 3:
              Starting initial_items: 74
              Operation: new = old + 3
              Test: divisible by 17
                If true: throw to monkey 0
                If false: throw to monkey 1
        ''').strip('\n')

    monkeys = [lines_to_list(m) for m in input_text.split('\n\n')]

    loader.print_solution('setup', f'{len(monkeys)} ...')
    loader.print_solution(1, part1(monkeys))
    loader.print_solution(2, part2(monkeys))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.003096        |        0.003096 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 8 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.012940        |        0.016036 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 120384
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 4.273875        |        4.289911 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 32059801242
    # --------------------------------------------------------------------------------
