from collections import Counter


def valid_password(pwd: str, part1: bool) -> bool:
    if part1:
        c = Counter(pwd.split())
    else:
        c = Counter([''.join(sorted(word)) for word in pwd.split()])
    return max(c.values()) == 1


def high_entropy_passphrases(inp, part1=True):
    valid_count = 0
    for line in inp:
        if valid_password(line, part1):
            valid_count += 1
    return valid_count


if __name__ == '__main__':
    with open('input.txt') as pwd_file:
        password_list = pwd_file.read().splitlines(keepends=False)
        print(f'Day 4, part 1: {high_entropy_passphrases(password_list)}')
        print(f'Day 4, part 2: {high_entropy_passphrases(password_list, False)}')
        # Day 4, part 1: 451
        # Day 4, part 2: 223
