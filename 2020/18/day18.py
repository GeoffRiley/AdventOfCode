from enum import Enum
from typing import Tuple, List


class Tokens(Enum):
    NUMBER = 1
    OP_ADD = 2
    OP_MUL = 4
    OPEN_PAREN = 8
    CLOSE_PAREN = 16
    STOP = 128


def tokenize_string(calc: str) -> Tuple[List[Tokens], List[int]]:
    tokens: List[Tokens] = []
    numbers: List[int] = []
    value: List[str] = []

    def add_token(tok):
        if len(value):
            tokens.append(Tokens.NUMBER)
            numbers.append(int(''.join(value)))
            value.clear()
        tokens.append(tok)

    for c in calc:
        if c == ' ':
            continue
        if c == '(':
            add_token(Tokens.OPEN_PAREN)
        elif c == ')':
            add_token(Tokens.CLOSE_PAREN)
        elif c == '+':
            add_token(Tokens.OP_ADD)
        elif c == '*':
            add_token(Tokens.OP_MUL)
        elif c.isdigit():
            value.append(c)

    add_token(Tokens.STOP)
    return tokens, numbers


def evaluate(calc: str, pass2: bool = False) -> int:
    tokens, numbers = tokenize_string(calc)

    def next_term():
        tok = tokens.pop(0)
        if tok == Tokens.OPEN_PAREN:
            return solve()
        if tok == Tokens.NUMBER:
            return numbers.pop(0)
        raise SyntaxError(f'Missing term: token received {tok.name}')

    def solve():
        acc = next_term()
        while True:
            op = tokens.pop(0)
            if op in [Tokens.CLOSE_PAREN, Tokens.STOP]:
                return acc
            value = next_term()
            if tokens[0] == Tokens.OP_ADD and pass2:
                _ = tokens.pop(0)
                value2 = next_term()
                value += value2
            if op == Tokens.OP_ADD:
                acc += value
            elif op == Tokens.OP_MUL:
                acc *= value
            else:
                raise SyntaxError(f'Unexpected token for operator: token received {op.name}')

    return solve()


def operation_order_part1(data: str) -> int:
    calcs = data.splitlines(keepends=False)
    running_total = 0
    for calc in calcs:
        running_total += evaluate(calc)
    return running_total


def operation_order_part2(data: str) -> int:
    calcs = data.splitlines(keepends=False)
    running_total = 0
    for calc in calcs:
        running_total += evaluate(calc, pass2=True)
    return running_total


if __name__ == '__main__':
    test_text = [
        # ["1 + 2 * 3 + 4 * 5 + 6", 71, 231],
        # ["1 + (2 * 3) + (4 * (5 + 6))", 51, 51],
        # ["2 * 3 + (4 * 5)", 26, 46],
        ["5 + (8 * 3 + 9 + 3 * 4 * 3)", 437, 1445],
        # ["5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 12240, 669060],
        # ["((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 13632, 23340],
    ]
    for test, expected, _ in test_text:
        assert operation_order_part1(test) == expected
    # for test, _, expected in test_text:
    #     assert operation_order_part2(test) == expected

    with open('input.txt') as in_file:
        in_text = in_file.read()
        part1 = operation_order_part1(in_text)
        print(f'Part1: {part1}')
        # part2 = operation_order_part2(in_text)
        # print(f'Part2: {part2}')

        # Part1: 12956356593940
