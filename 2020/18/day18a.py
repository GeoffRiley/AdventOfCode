from sly import Lexer, Parser


class CalcLexer(Lexer):
    tokens = {NUMBER, PLUS, TIMES, LPAREN, RPAREN}
    ignore = ' \t'

    # Tokens
    NUMBER = r'\d+'

    # Special symbols
    PLUS = r'\+'
    TIMES = r'\*'
    LPAREN = r'\('
    RPAREN = r'\)'

    # Ignored pattern
    ignore_newline = r'\n+'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1


class CalcParser1(Parser):
    tokens = CalcLexer.tokens
    precedence = (
        ('left', PLUS, TIMES),
    )

    def __init__(self):
        self.names = {}

    @_('expr')
    def statement(self, p):
        return p.expr

    @_('expr PLUS expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('expr TIMES expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return int(p.NUMBER)


class CalcParser2(Parser):
    tokens = CalcLexer.tokens
    precedence = (
        ('left', TIMES),
        ('left', PLUS),
    )

    def __init__(self):
        self.names = {}

    @_('expr')
    def statement(self, p):
        return p.expr

    @_('expr PLUS expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('expr TIMES expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return int(p.NUMBER)


def operation_order_part1(data: str) -> int:
    lexer = CalcLexer()
    parser = CalcParser1()
    calcs = data.splitlines(keepends=False)
    running_total = 0
    for calc in calcs:
        answer = parser.parse(lexer.tokenize(calc))
        running_total += answer
    return running_total


def operation_order_part2(data: str) -> int:
    lexer = CalcLexer()
    parser = CalcParser2()
    calcs = data.splitlines(keepends=False)
    running_total = 0
    for calc in calcs:
        answer = parser.parse(lexer.tokenize(calc))
        running_total += answer
    return running_total


if __name__ == '__main__':
    test_text = [
        ["1 + 2 * 3 + 4 * 5 + 6", 71, 231],
        ["1 + (2 * 3) + (4 * (5 + 6))", 51, 51],
        ["2 * 3 + (4 * 5)", 26, 46],
        ["5 + (8 * 3 + 9 + 3 * 4 * 3)", 437, 1445],
        ["5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 12240, 669060],
        ["((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 13632, 23340],
    ]
    for test, expected, _ in test_text:
        assert operation_order_part1(test) == expected
    for test, _, expected in test_text:
        assert operation_order_part2(test) == expected

    with open('input.txt') as in_file:
        in_text = in_file.read()
        part1 = operation_order_part1(in_text)
        print(f'Part1: {part1}')
        part2 = operation_order_part2(in_text)
        print(f'Part2: {part2}')

        # Part1: 12956356593940
        # Part2: 94240043727614
