from math import prod
from typing import List, Dict, Set, Optional, Tuple


def range_set(range_str: str) -> Set[int]:
    b: List[str] = range_str.split('-')
    return set(range(int(b[0]), int(b[1]) + 1))


def rule_valid(rule: str) -> Set[int]:
    lower, _, upper = rule.split()
    return set.union(range_set(lower), range_set(upper))


def process_rules(rules: List[str]) -> Tuple[Dict[int, str], List[Set[int]]]:
    rule_names: Dict[int, str] = {i: rule.split(':')[0] for i, rule in enumerate(rules)}
    rule_array: List[Set[int]] = [rule_valid(rule.split(':')[1]) for rule in rules]
    return rule_names, rule_array


def ticket_translation_part1(data: str) -> int:
    rules: List[str]
    nearby: List[str]
    rules, _, nearby = (block.splitlines(keepends=False) for block in data.split("\n\n"))
    _, rule_array = process_rules(rules)

    valid = set.union(*rule_array)
    invalid = list()
    for ticket in nearby[1:]:
        ticket_values = list(map(int, ticket.split(',')))
        invalid.extend(list(i for i in ticket_values if i not in valid))
    return sum(invalid)


def ticket_translation_part2(data: str) -> int:
    rules: List[str]
    mine: List[str]
    nearby: List[str]
    rules, mine, nearby = (block.splitlines(keepends=False) for block in data.split("\n\n"))

    rule_names, rule_array = process_rules(rules)
    rule_count: int = len(rule_names)

    my_ticket: List[int] = list(map(int, mine[1].split(',')))
    assert len(my_ticket) == rule_count

    valid = set.union(*rule_array)
    test_tickets = list()
    for ticket in nearby[1:]:
        ticket_values = list(map(int, ticket.split(',')))
        assert len(ticket_values) == rule_count
        if all(t in valid for t in ticket_values):
            test_tickets.append(ticket_values)
    test_tickets.append(my_ticket)

    validation_array: List[List[bool]] = [[True for _ in range(rule_count)] for _ in range(rule_count)]
    # For each ticket test if each field *could* be valid for each element
    for ticket in test_tickets:
        for i, entry in enumerate(ticket):
            for j, rule in enumerate(rule_array):
                if entry not in rule:
                    validation_array[i][j] = False

    the_mapping: List[Optional[int]] = [None for _ in range(rule_count)]
    the_flags: List[bool] = [True for _ in range(rule_count)]

    found_count = 0
    while found_count < 20:
        for i in range(rule_count):
            selected_rules = [j for j in range(rule_count) if the_flags[j] and validation_array[i][j]]
            if len(selected_rules) == 1:
                found_count += 1
                entry = selected_rules[0]
                the_mapping[i] = entry
                the_flags[entry] = False

    print('   ** Ticket Details **')
    print('\n'.join(sorted(f'{j:02d} -{rule_names[j]:>19s}: {my_ticket[i]}' for i, j in enumerate(the_mapping))))

    return prod(my_ticket[i] for i, j in enumerate(the_mapping) if rule_names[j].startswith('departure'))


if __name__ == '__main__':
    test_text = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""
    assert ticket_translation_part1(test_text) == 71
    # assert ticket_translation_part2(test_text) == 0

    with open('input.txt') as in_file:
        in_text = in_file.read()
        part1 = ticket_translation_part1(in_text)
        print(f'Part1: {part1}')
        part2 = ticket_translation_part2(in_text)
        print(f'Part2: {part2}')

    # Part1: 23115
    #    ** Ticket Details **
    # 00 - departure location: 53
    # 01 -  departure station: 61
    # 02 - departure platform: 89
    # 03 -    departure track: 73
    # 04 -     departure date: 101
    # 05 -     departure time: 113
    # 06 -   arrival location: 107
    # 07 -    arrival station: 83
    # 08 -   arrival platform: 97
    # 09 -      arrival track: 67
    # 10 -              class: 181
    # 11 -           duration: 191
    # 12 -              price: 79
    # 13 -              route: 109
    # 14 -                row: 59
    # 15 -               seat: 149
    # 16 -              train: 103
    # 17 -               type: 151
    # 18 -              wagon: 71
    # 19 -               zone: 127
    # Part2: 239727793813
