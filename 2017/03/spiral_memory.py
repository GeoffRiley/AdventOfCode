from math import sqrt, ceil


def spiral_memory(inp):
    circuit = ceil(sqrt(inp)) // 2
    circuit0 = (circuit * 2 - 1) ** 2
    centres = [circuit0 + x * circuit for x in range(1, 8, 2)]
    return circuit + min([abs(inp - x) for x in centres])


def spiral_memory_sums(inp):
    points = (-1 - 1j, -1j, +1 - 1j,
              -1, +1,
              -1 + 1j, +1j, +1 + 1j)
    spiral = dict()


"""
See: https://oeis.org/A141481 & https://oeis.org/A141481/b141481.txt
1 1
2 1
3 2
4 4
5 5
6 10
7 11
8 23
9 25
10 26
11 54
12 57
13 59
14 122
15 133
16 142
17 147
18 304
19 330
20 351
21 362
22 747
23 806
24 880
25 931
26 957
27 1968
28 2105
29 2275
30 2391
31 2450
32 5022
33 5336
34 5733
35 6155
36 6444
37 6591
38 13486
39 14267
40 15252
41 16295
42 17008
43 17370
44 35487
45 37402
46 39835
47 42452
48 45220
49 47108
50 48065
51 98098
52 103128
53 109476
54 116247
55 123363
56 128204
57 130654
58 266330
59 279138
60 295229
"""

if __name__ == '__main__':
    assert spiral_memory(1) == 0
    assert spiral_memory(12) == 3
    assert spiral_memory(23) == 2
    assert spiral_memory(1024) == 31
    print(f'Day 3, part 1: {spiral_memory(289326)}')
    print(f'Day 3, part 1: {spiral_memory_sums(289326)}')
    # Day 3, part 1: 419
    # Day 3, part 2: 295229 # from table above
