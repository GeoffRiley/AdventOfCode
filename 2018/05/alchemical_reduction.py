def react_all(new_str):
    done = False
    while not done:
        done = True
        old_str = new_str
        last_char = old_str[0]
        new_str = ''
        skip = 0
        for char in old_str[1:]:
            if skip > 0:
                skip -= 1
                last_char = char
                continue
            if last_char != char and last_char.lower() == char.lower():
                done = False
                skip = 1
                continue
            new_str += last_char
            last_char = char
        if skip == 0:
            new_str += last_char
    return new_str


def alchemical_reduction_part_1(inp):
    new_str = react_all(inp[0])
    return len(new_str)


def alchemical_reduction_part_2(inp):
    inp: str = inp[0]
    char_set = set(inp.lower())
    counts = dict()
    for char in char_set:
        tmp = inp.replace(char, '').replace(char.upper(), '')
        counts[char] = react_all(tmp)
    result = min(counts.items(), key=lambda x: len(x[1]))
    return len(result[1])


if __name__ == '__main__':
    with open('input.txt') as chem_file:
        chem_strings = chem_file.read().splitlines(keepends=False)
        print(f'Day 5, part 1: {alchemical_reduction_part_1(chem_strings)}')
        print(f'Day 5, part 2: {alchemical_reduction_part_2(chem_strings)}')
        # Day 5, part 1: 11540
        # Day 5, part 2: 6918
