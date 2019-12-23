import math

puzzle_input = 36000000
number_of_visiting_elves = puzzle_input // 10
number_of_visiting_elves2 = puzzle_input // 11


def get_factors(n):
    s = int(math.sqrt(n))
    low = [i for i in range(1, s + 1) if n % i == 0]
    hi = [n // i for i in low if s != i]
    return low + hi


house_number = 1
p1 = None
p2 = None

while p1 is None or p2 is None:
    house_number += 1
    factors = get_factors(house_number)
    if p1 is None and sum(factors) >= number_of_visiting_elves:
        p1 = house_number
    if p2 is None and sum(p for p in factors if house_number // p <= 50) >= number_of_visiting_elves2:
        p2 = house_number

print(f'Part 1: {p1}')
print(f'Part 2: {p2}')
# Part 1: 831600
# Part 2: 884520
