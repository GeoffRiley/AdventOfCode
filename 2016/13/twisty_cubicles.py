# stack holds a list of tuples (x,y,dist)
STACK = [(1, 1, 0)]
# visited holds a dictionary of tuple indexes to distance
VISITED = {}


def is_space(x, y):
    num = x * x + 3 * x + 2 * x * y + y + y * y + 1352
    return not (bin(num).count('1') % 2 or x < 0 or y < 0)


def find_next(x, y, dist):
    for p_x, p_y in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        t_x, t_y = x + p_x, y + p_y
        if t_x < 0 or t_y < 0:
            continue
        if is_space(t_x, t_y) and (t_x, t_y) not in VISITED:
            yield t_x, t_y, dist + 1


while len(STACK) > 0:
    x, y, dist = STACK.pop(0)
    VISITED[(x, y)] = dist
    STACK.extend([nxt for nxt in find_next(x, y, dist)])

print(f'Part 1: {VISITED[(31, 39)]}')
print(f'Part 2: {sum(1 for x in VISITED.values() if x <= 50)}')
# Part 1: 90
# Part 2: 135
