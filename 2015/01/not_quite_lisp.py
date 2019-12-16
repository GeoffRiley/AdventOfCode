def find_floor(brackets: str) -> int:
    return sum(1 if c == '(' else -1 for c in brackets)


def find_basement_entry(brackets: str) -> int:
    return [n + 1 for n in range(len(brackets)) if find_floor(brackets[:n + 1]) == -1][0]


if __name__ == '__main__':
    with open('input') as f:
        bracket_text = f.read()
    print(f'Part 1: {find_floor(bracket_text)}')
    print(f'Part 2: {find_basement_entry(bracket_text)}')
