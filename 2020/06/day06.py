def custom_customs_part1(data: str) -> int:
    result = sum(
        len(set.union(*[set(entry) for entry in para.replace('\n', '')]))
        for para in data.split('\n\n')
    )
    return result


def custom_customs_part2(data: str) -> int:
    result = sum(
        len(set.intersection(*[set(entry) for entry in para.split("\n")]))
        for para in data.split('\n\n')
    )
    return result


# 3428
if __name__ == '__main__':
    test_text = """abc

a
b
c

ab
ac

a
a
a
a

b"""
    assert custom_customs_part1(test_text) == 11
    assert custom_customs_part2(test_text) == 6

    with open('input.txt') as in_file:
        in_text = in_file.read().rstrip()
        part1 = custom_customs_part1(in_text)
        print(f'Part1: {part1}')
        part2 = custom_customs_part2(in_text)
        print(f'Part2: {part2}')

    # Part1: 6703
    # Part2: 3430
