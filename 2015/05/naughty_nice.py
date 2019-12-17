import re


def is_nice(name: str) -> bool:
    return (sum(1 for c in name if c in 'aeiuo') > 2) and (len(re.findall(r'(.)\1', name)) > 0) and (
            len(re.findall(r'ab|cd|pq|xy', name)) == 0)


def is_nicer(name: str) -> bool:
    return (len(re.findall(r'(.).\1', name)) > 0) and (len(re.findall(r'(..).*\1', name)) > 0)


if __name__ == '__main__':
    with open('input') as f:
        name_list = f.readlines()
    c = sum(1 if is_nice(name) else 0 for name in name_list)
    print(f'Part 1: {c}')
    c = sum(1 if is_nicer(name) else 0 for name in name_list)
    print(f'Part 2: {c}')
