"""
Advent of code 2021
Day 10: Syntax Scoring
"""
from statistics import median

from aoc.loader import LoaderLib
from aoc.search import Stack
from aoc.utility import lines_to_list

BRACKET_SCORES = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}

COMPLETION_SCORE = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4
}

BRACKET_MATCHES = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">"
}

OPENING_BRACKETS = "([{<"


def part1(lines):
    """
    """
    score = 0
    for line in lines:
        open_brackets = Stack()
        for c in line:
            if c in OPENING_BRACKETS:
                open_brackets.push(BRACKET_MATCHES[c])
            else:
                e = open_brackets.pop()
                if c == e:
                    continue
                else:
                    score += BRACKET_SCORES[c]
                    break
    return score
    # 243939


def part2(lines):
    """
    """
    scores = []
    for line in lines:
        open_brackets = Stack()
        for c in line:
            if c in OPENING_BRACKETS:
                open_brackets.push(BRACKET_MATCHES[c])
            else:
                e = open_brackets.pop()
                if c == e:
                    continue
                else:
                    open_brackets.clear()
                    break
        score = 0
        while not open_brackets.empty:
            score = score * 5 + COMPLETION_SCORE[open_brackets.pop()]
        if score:
            scores.append(score)
    return median(scores), f'len(scores) = {len(scores)}'


def main():
    loader = LoaderLib(2021)
    input_text = loader.get_aoc_input(10)

    #     input_text = """[({(<(())[]>[[{[]{<()<>>
    # [(()[<>])]({[<{<<[]>>(
    # {([(<{}[<>[]}>{[]{[(<()>
    # (((({<>}<{<{<>}{[]{[]{}
    # [[<[([]))<([[{}[[()]]]
    # [{[{({}]{}}([{[{{{}}([]
    # {<[[]]>}<{[{[{[]{()[[[]
    # [<(<(<(<{}))><([]([]()
    # <{([([[(<>()){}]>(<<{{
    # <{([{{}}[<[[[<>{}]]]>[]]"""

    lines = lines_to_list(input_text)

    # assert len(lines) == len(...)
    loader.print_solution('setup', f'{len(lines)} ...')
    loader.print_solution(1, part1(lines))
    loader.print_solution(2, part2(lines))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.004429        |        0.004429 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 102 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.006464        |        0.010893 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 243939
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.008342        |        0.019234 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : (2421222841, 'len(scores) = 51')
    # --------------------------------------------------------------------------------
