import re


def expand_file(compressed: str, ver2=False) -> int:
    unc = 0
    while len(compressed) > 0:
        i = compressed.find('(')
        if i >= 0:
            unc += i
            j = compressed.find(')', i)
            decom = compressed[i:j + 1]
            rep_len, rep_count = [int(v) for v in re.search(r'(\d+)x(\d+)', decom).groups()]
            if ver2:
                unc += expand_file(compressed[j + 1:j + rep_len + 1], ver2=ver2) * rep_count
            else:
                unc += rep_len * rep_count
            compressed = compressed[j + rep_len + 1:]
        else:
            unc += len(compressed)
            compressed = ''
    return unc


if __name__ == '__main__':
    with open('input') as f:
        mystery_file = f.read()

    f_len = expand_file(mystery_file)
    print(f'Part 1: {f_len}')
    # Part 1: 99145
    g_len = expand_file(mystery_file, ver2=True)
    print(f'Part 2: {g_len}')
