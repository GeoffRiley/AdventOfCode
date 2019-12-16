from functools import reduce
from operator import mul


def no_maths(parcel_size: str) -> int:
    l, w, h = [int(v) for v in parcel_size.split('x')]
    s = [l * w, l * h, w * h]
    return 2 * sum(s) + min(s)


def ribbon_length(parcel_size: str) -> int:
    sides = [int(v) for v in parcel_size.split('x')]
    smaller = sorted(sides)[:2]
    return reduce(mul, sides, 1) + sum(smaller) * 2


if __name__ == '__main__':
    with open('input') as f:
        parcel_list = f.readlines()
    print(f'Part 1: {sum(no_maths(v) for v in parcel_list)}')
    print(f'Part 2: {sum(ribbon_length(v) for v in parcel_list)}')
