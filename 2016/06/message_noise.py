from collections import Counter


def scrub_noise(message: str, part2=False) -> str:
    lines = message.splitlines(keepends=False)
    counts = [Counter() for _ in range(len(lines[0]))]
    for line in lines:
        for ct, ch in zip(counts, line):
            ct[ch] += 1
    if part2:
        return ''.join(c.most_common()[-1][0] for c in counts)
    else:
        return ''.join(c.most_common(1)[0][0] for c in counts)


if __name__ == '__main__':
    with open('input') as f:
        repeated_message = f.read()
    res = scrub_noise(repeated_message)
    res2 = scrub_noise(repeated_message, True)

    print(f'Part 1: {res}')
    print(f'Part 2: {res2}')
    # Part 1: qrqlznrl
    # Part 2: kgzdfaon
