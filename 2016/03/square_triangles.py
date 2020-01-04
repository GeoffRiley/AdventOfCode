def is_triangle(lens) -> bool:
    (a, b, c) = lens
    return ((a + b) > c) and ((a + c) > b) and ((b + c) > a)


with open('input') as f:
    try_angles = f.read()

c = 0
for line in try_angles.splitlines(keepends=False):
    lengths = [int(v) for v in line.split()]
    c += 1 if is_triangle(lengths) else 0

print(f'Part 1: {c}')
# 982

c = 0
lines = [[int(v) for v in line.split()] for line in try_angles.splitlines(keepends=False)]
for line_no in range(0, len(lines), 3):
    a1, a2, a3 = lines[line_no]
    b1, b2, b3 = lines[line_no + 1]
    c1, c2, c3 = lines[line_no + 2]
    for test in [(a1, b1, c1), (a2, b2, c2), (a3, b3, c3)]:
        c += 1 if is_triangle(test) else 0

print(f'Part 2: {c}')
#  1826
