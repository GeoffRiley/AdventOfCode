def combo_breaker_part1(data: str) -> int:
    key1, key2 = tuple(map(int, data.splitlines(keepends=False)))
    subject = 7
    found = False
    loop_size = None
    loop_count = 1
    while not found:
        loop_count += 1
        subject = transform(subject)
        if subject == key2:
            loop_size = loop_count
            found = True

    working = 1
    for n in range(loop_size):
        working = transform(working, key1)

    return working


def transform(key: int, subject: int = 7) -> int:
    return (key * subject) % 20201227


# def combo_breaker_part2(data: str) -> int:
#     pass


if __name__ == '__main__':
    test_text = """5764801
17807724"""
    assert combo_breaker_part1(test_text) == 14897079
    # assert combo_breaker_part2(test_text) == 0

    with open('input.txt') as in_file:
        in_text = in_file.read()
        part1 = combo_breaker_part1(in_text)
        print(f'Part1: {part1}')
        # part2 = combo_breaker_part2(in_text)
        # print(f'Part2: {part2}')

    # Part1: 448851
