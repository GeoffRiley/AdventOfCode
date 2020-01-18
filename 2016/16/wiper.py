def wiper(base: str, size: int):
    a = base
    trs = str.maketrans('01', '10')
    while len(a) < size:
        b = a[::-1].translate(trs)
        a = a + '0' + b
    a = a[:size]
    c = a
    while len(c) % 2 == 0:
        c = ''.join(['1' if c[x] == c[x + 1] else '0' for x in range(0, len(c), 2)])
    return a, c


if __name__ == '__main__':
    print(f'Part 1: {wiper("01111001100111011", 272)[1]}')
    print(f'Part 2: {wiper("01111001100111011", 35651584)[1]}')
    # Part 1: 11111000111110000
    # Part 2: 10111100110110100
