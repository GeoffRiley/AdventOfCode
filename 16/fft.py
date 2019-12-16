from functools import lru_cache
from itertools import cycle

PATTERN = [0, 1, 0, -1]


@lru_cache(maxsize=None)
def pattern(pass_num: int) -> list:
    patt = [a for a in PATTERN for _ in range(pass_num)]
    return patt[pass_num:] + patt[:pass_num]


@lru_cache(maxsize=None)
def perform_phase_pass(pass_num: int, d_array: tuple) -> int:
    phase_pattern = cycle(pattern(pass_num))
    res = 0
    for d, p in zip(d_array[pass_num - 1:], phase_pattern):
        res += (-d, 0, d)[p + 1]
    return abs(res) % 10


def perform_phase(d_array: tuple, part2: bool = False) -> tuple:
    if part2:
        res = [v for v in d_array]
        for place in range(len(res) - 2, -1, -1):
            res[place] = abs(res[place] + res[place + 1]) % 10
        return tuple(res)
    else:
        p_array = []  # list(d_array)
        for n in range(len(d_array)):
            p_array.append(perform_phase_pass(n + 1, d_array))
        return tuple(p_array)


def fft(original_digits: str, phase_count: int = 100, part2: bool = False) -> str:
    phase = 0
    if part2:
        offset = int(original_digits[:7])
        long_digits = (original_digits * 10000)[offset:]
        long_array = [int(a) for a in long_digits]
        d_array = tuple(long_array)
    else:
        d_array = tuple(int(a) for a in original_digits)
    while phase < phase_count:
        phase += 1
        d_array = perform_phase(d_array, part2=part2)
    return ''.join([str(v) for v in d_array[:8]])


if __name__ == '__main__':
    with open('input') as f:
        digits = f.read()
    print(f'PART 1: {fft(digits)}')
    print(f'PART 2: {fft(digits, part2=True)}')

    '''
    PART 1: 94935919
    PART 2: 24158285
    '''
