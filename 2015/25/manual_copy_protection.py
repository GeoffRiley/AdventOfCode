"""

Codes are generated in the sequence:
   | 1   2   3   4   5   6
---+---+---+---+---+---+---+
 1 |  1   3   6  10  15  21
 2 |  2   5   9  14  20
 3 |  4   8  13  19
 4 |  7  12  18
 5 | 11  17
 6 | 16

From the first code, 20151125, each subsequent code is  (prev * 252533) % 33554393

Example:
   |    1         2         3         4         5         6
---+---------+---------+---------+---------+---------+---------+
 1 | 20151125  18749137  17289845  30943339  10071777  33511524
 2 | 31916031  21629792  16929656   7726640  15514188   4041754
 3 | 16080970   8057251   1601130   7981243  11661866  16474243
 4 | 24592653  32451966  21345942   9380097  10600672  31527494
 5 |    77061  17552253  28094349   6899651   9250759  31663883
 6 | 33071741   6796745  25397450  24659492   1534922  27995004

"""


# Calculate the element at row 3010, column 3019.

def modpow(b, e, m):
    if e == 0:
        return 1
    elif e % 2 == 0:
        return modpow((b * b) % m, e / 2, m)
    else:
        return (b * modpow(b, e - 1, m)) % m


row = 3010
col = 3019

first_code = 20151125
base_mult = 252533
base_mod = 33554393

exponent = (row + col - 2) * (row + col - 1) / 2 + col - 1
extrapolated = modpow(base_mult, exponent, base_mod) * first_code % base_mod

print(f'Part 1: {extrapolated}')
# Part 1: 8997277
