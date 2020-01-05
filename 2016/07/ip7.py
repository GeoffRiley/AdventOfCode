import re


def find_reflective(s: str) -> bool:
    f = re.search(r'(.)(.)\2\1', s)
    return f is not None and len(f.groups()) == 2 and f.group(1) != f.group(2)


def check_parts(a, b):
    return find_reflective(a), find_reflective(b)


def check_abba(addr: str) -> bool:
    c = addr
    good = bad = False
    while '[' in c and not bad:
        a, b, c = re.match(r'(.*?)\[(.*?)](.*)', c).groups()
        a1, b1 = check_parts(a, b)
        good = good or a1
        bad = bad or b1
    c1 = find_reflective(c)
    good = good or c1
    return good if not bad else False


def get_groups(word: str) -> list:
    res = []
    for n in range(len(word) - 2):
        if word[n] == word[n + 2] != word[n + 1]:
            res.append(word[n:n + 3])
    return res


def check_aba(addr: str) -> bool:
    c = addr
    triples_a = []
    triples_b = []
    bad = False
    while '[' in c:
        a, b, c = re.match(r'(.*?)\[(.*?)](.*)', c).groups()
        a1 = get_groups(a)
        b1 = get_groups(b)
        triples_a.extend(a1)
        triples_b.extend(b1)
    c1 = get_groups(c)
    triples_a.extend(c1)
    for t in triples_a:
        v = t[1] + t[:2]
        if v in triples_b:
            return True
    return False


if __name__ == '__main__':
    with open('input') as f:
        addrs = f.read()
    count_abba = 0
    count_aba = 0
    for addr in addrs.splitlines(keepends=False):
        if check_abba(addr):
            # print(addr)
            count_abba += 1
        if check_aba(addr):
            count_aba += 1

    print(f'Part 1: {count_abba}')
    # Part 1: 105
    print(f'Part 2: {count_aba}')
    # Part 2: 258
