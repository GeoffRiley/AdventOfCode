from collections import deque


def spinlock(inp, part1=True):
    spin_buffer = deque([0])
    top = 2017 if part1 else 50_000_000
    for c in range(1, top + 1):
        spin_buffer.rotate(inp)
        spin_buffer.appendleft(c)
    if part1:
        return spin_buffer[-1]
    else:
        zero = spin_buffer.index(0)
        return spin_buffer[zero - 1]


if __name__ == '__main__':
    assert spinlock(3) == 638
    spin_value = 363
    print(f'Day 17, part 1: {spinlock(spin_value)}')
    print(f'Day 17, part 2: {spinlock(spin_value, False)}')
    # Day 17, part 1: 136
    # Day 17, part 2: 1080289
