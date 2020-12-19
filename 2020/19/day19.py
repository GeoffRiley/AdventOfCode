import re
from typing import List, Union, Dict

Rules = Union[str, List[Union[int, List[int]]]]


def make_pattern(template: str) -> Rules:
    if '"' in template:
        return template.strip('"')
    if '|' in template:
        return [list(map(int, temp.strip().split())) for temp in template.split('|')]
    return list(map(int, template.split()))


def build_regexp(rules: Dict[int, Rules], current_rule: int = 0):
    regexp = r''
    r = rules[current_rule]
    try:
        if current_rule == 8:
            build_regexp.rule8 += 1
            if build_regexp.rule8 > 10:
                r = [42]
    except AttributeError:
        pass
    try:
        if current_rule == 11:
            build_regexp.rule11 += 1
            if build_regexp.rule11 > 10:
                r = [42, 31]
    except AttributeError:
        pass
    if isinstance(r, str):
        regexp += r
        current_rule = None
    else:
        regexp += '('
        alts = []
        if not isinstance(r[0], list):
            r = [r]
        for r1 in r:
            exp = ''
            for i in r1:
                exp += build_regexp(rules, i)
            alts.append(exp)
        regexp += '|'.join(alts) + ')'
    return regexp


build_regexp.rule8 = 0
build_regexp.rule11 = 0


def monster_messages_part1(data: str) -> int:
    rule_str: str
    message_str: str
    rule_str, message_str = data.split('\n\n')
    rules: Dict[int, Rules] = {int(n): make_pattern(p)
                               for n, p in map(lambda x: x.split(': '), rule_str.splitlines(keepends=False))}
    regexp = rf'^{build_regexp(rules)}$'

    result = 0
    for message in message_str.splitlines(keepends=False):
        if re.match(regexp, message):
            result += 1
    return result


def monster_messages_part2(data: str) -> int:
    rule_str: str
    message_str: str
    rule_str, message_str = data.split('\n\n')
    rules: Dict[int, Rules] = {int(n): make_pattern(p)
                               for n, p in map(lambda x: x.split(': '), rule_str.splitlines(keepends=False))}
    # 'Fix' rules:
    rules[8] = [[42], [42, 8]]
    rules[11] = [[42, 31], [42, 11, 31]]
    regexp = rf'^{build_regexp(rules)}$'

    result = 0
    for message in message_str.splitlines(keepends=False):
        if re.match(regexp, message):
            result += 1
    return result


if __name__ == '__main__':
    test_text = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""
    assert monster_messages_part1(test_text) == 2
    # assert monster_messages_part2(test_text) == 0

    with open('input.txt') as in_file:
        in_text = in_file.read()
        part1 = monster_messages_part1(in_text)
        print(f'Part1: {part1}')
        part2 = monster_messages_part2(in_text)
        print(f'Part2: {part2}')

    # Part1: 124
    # Part2: 228
