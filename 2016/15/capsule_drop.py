from modint import chinese_remainder


def capsule_drop(discs: list):
    num = []
    rem = []
    for i, (n, r) in enumerate(discs):
        num.append(n)
        rem.append(n - (r + i + 1) % n)
    return chinese_remainder(num, rem)


if __name__ == '__main__':
    disc_list = []
    with open('input') as f:
        for line in f.read().splitlines(keepends=False):
            parts = line.strip('.').split()
            disc_list.append((int(parts[3]), int(parts[-1])))
    print(f'Part 1: {capsule_drop(disc_list)}')
    disc_list.append((11, 0))
    print(f'Part 2: {capsule_drop(disc_list)}')
    # Part 1: 203660
    # Part 2: 2408135
