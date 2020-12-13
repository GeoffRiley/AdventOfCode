from math import prod
from typing import List, Tuple


def shuttle_search_part1(data: str) -> int:
    lines: List[str] = data.splitlines(keepends=False)
    earliest_time: int = int(lines[0])
    bus_id_list: List[int] = [int(b) for b in lines[1].split(',') if b != 'x']

    best_bus: Tuple[int, int] = (max(bus_id_list), max(bus_id_list))

    for bus_id in bus_id_list:
        check = bus_id - (earliest_time % bus_id)
        if best_bus[1] > check:
            best_bus = (bus_id, check)

    return best_bus[0] * best_bus[1]


def chinese_remainder(lst: List[Tuple[int, int]]) -> int:
    cumulative = 0
    product = prod(n for n, _ in lst)
    for item, remainder in lst:
        p = product // item
        cumulative += remainder * mod_inv(p, item) * p
    return cumulative % product


# Implementation of pseudocode at https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    last_remainder, remainder = abs(a), abs(b)
    x, last_x, y, last_y = 0, 1, 1, 0
    while remainder:
        last_remainder, (quotient, remainder) = remainder, divmod(last_remainder, remainder)
        x, last_x = last_x - quotient * x, x
        y, last_y = last_y - quotient * y, y
    return (last_remainder,
            last_x * (-1 if a < 0 else 1),
            last_y * (-1 if b < 0 else 1))


def mod_inv(a: int, modulo: int) -> int:
    g, x, y = extended_gcd(a, modulo)
    if g != 1:
        raise ValueError('No result found')
    return x % modulo


def shuttle_search_part2(data: str) -> int:
    lines: List[str] = data.splitlines(keepends=False)
    bus_id_list: List[Tuple[int, int]] = [(int(b), int(b) - n)
                                          for n, b in enumerate(lines[1].split(','))
                                          if b != 'x']
    return chinese_remainder(bus_id_list)


if __name__ == '__main__':
    test_text = """939
7,13,x,x,59,x,31,19"""
    assert shuttle_search_part1(test_text) == 295
    assert shuttle_search_part2(test_text) == 1068781
    for test_text, expected in [
        ("17,x,13,19", 3417),
        ("67,7,59,61", 754018),
        ("67,x,7,59,61", 779210),
        ("67,7,x,59,61", 1261476),
        ("1789,37,47,1889", 1202161486),
    ]:
        assert shuttle_search_part2(f'123\n{test_text}') == expected

    with open('input.txt') as in_file:
        in_text = in_file.read()
        part1 = shuttle_search_part1(in_text)
        print(f'Part1: {part1}')
        part2 = shuttle_search_part2(in_text)
        print(f'Part2: {part2}')

    # Part1: 3966
    # Part2: 800177252346225
