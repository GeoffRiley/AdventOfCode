def corner(a, b):
    x1, y1 = [int(v) for v in a.split(',')]
    x2, y2 = [int(v) for v in b.split(',')]
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1
    return x1, y1, x2, y2


def toggle(corner1, corner2, part2=False):
    x1, y1, x2, y2 = corner(corner1, corner2)
    for row in range(y1, y2 + 1):
        for col in range(x1, x2 + 1):
            if part2:
                lamps[row][col] += 2
            else:
                lamps[row][col] = 1 - lamps[row][col]


def turn(on, corner1, corner2, part2=False):
    on_flag = 1 if on == 'on' else -1 if part2 else 0
    x1, y1, x2, y2 = corner(corner1, corner2)
    for row in range(y1, y2 + 1):
        for col in range(x1, x2 + 1):
            if part2:
                lamps[row][col] = max(lamps[row][col] + on_flag, 0)
            else:
                lamps[row][col] = on_flag


lamps = [[0 for i in range(1000)] for j in range(1000)]

with open('input') as f:
    instructions = f.readlines()


def run(part2=False):
    for row in range(1000):
        for col in range(1000):
            lamps[row][col] = 0
    for line in instructions:
        elements = line.split()
        if elements[0] == 'toggle':
            toggle(elements[1], elements[3], part2)
        elif elements[0] == 'turn':
            turn(elements[1], elements[2], elements[4], part2)
        else:
            raise ValueError(f'Unknown function {elements[0]}')
    return sum(v for line in lamps for v in line)


print(f'Part 1 {run()}')
'''Part 1 400410'''
print(f'Part 2 {run(True)}')
'''Part 2 15343601'''
