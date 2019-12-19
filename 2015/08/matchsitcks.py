with open('input') as f:
    santas_list_raw = f.read()
    santas_list = santas_list_raw.splitlines(keepends=False)


def extract_literals(line: str) -> str:
    return line.strip()[1:-1]


def compress_literals(line: str) -> str:
    ptr = 0
    res = ''
    while ptr < len(line):
        c = line[ptr]
        if c == '\\':
            ptr += 1
            c = line[ptr]
            if c == 'x':
                ptr += 2
                c = chr(int(line[ptr - 1:ptr + 1], 16))
        res += c
        ptr += 1
    return res


def encode_literals(line: str) -> str:
    ptr = 0
    res = ''
    while ptr < len(line):
        c = line[ptr]
        if c in '\\"':
            res += '\\'
        res += c
        ptr += 1
    return res


santas_list_literal = [extract_literals(line) for line in santas_list]
santas_decoded_list = [compress_literals(line) for line in santas_list_literal]
santas_encoded_list = [f'"{encode_literals(line)}"' for line in santas_list]

a = len(''.join(santas_list))
b = len(''.join(santas_decoded_list))
c = len(''.join(santas_encoded_list))

print(f'Part 1: {a - b}')
# 1333
print(f'Part 2: {c - a}')
# 2046
