import re
from collections import defaultdict
from itertools import permutations


def calc_score(seating, names):
    sc = 0
    for n1, n2, n3 in zip(seating, seating[1:] + seating[:1], seating[2:] + seating[:2]):
        l = names[n2]
        sc += l[n1] + l[n3]
    return sc


def party_happiness(disposition: str, plus_me=False) -> int:
    names = defaultdict(lambda: dict())

    for line in disposition.splitlines(keepends=False):
        # David would gain 41 happiness units by sitting next to Carol.
        match = re.match(r'^(\w+) would (\w+) (\d+) happiness units by sitting next to (\w+)\.', line)
        if match is None:
            raise ValueError(f'Bad disposition string {line}')
        res = match.groups()
        dis_to_neigh = int(res[2]) * (-1 if res[1] == 'lose' else 1)
        names[res[0]][res[3]] = dis_to_neigh
    if plus_me:
        names['myself'] = dict()
        for n in names.keys():
            names[n]['myself'] = 0
            names['myself'][n] = 0

    score = 0
    for seating in permutations(names.keys()):
        new_score = calc_score(seating, names)
        if new_score > score:
            score = new_score
    return score


if __name__ == '__main__':
    with open('input') as f:
        catering_needs = f.read()
    print(f'Part 1: {party_happiness(catering_needs)}')
    print(f'Part 2: {party_happiness(catering_needs, plus_me=True)}')
