import re
from collections import defaultdict, deque

STRATA_BAND = re.compile(r'^(?P<left>[xy])=(?P<lparam>\d+),\s(?P<right>[xy])=(?P<rparam1>\d+)\.\.(?P<rparam2>\d+)$')


def reservoir_research(inp):
    clay_positions = defaultdict(lambda: False)
    still_water = set()
    flowing_water = set()
    for line in inp:
        match = STRATA_BAND.match(line)
        if match is None:
            raise SyntaxError(f'"{line}" does not match pattern')
        lparam = int(match.group('lparam'))
        rparam1 = int(match.group('rparam1'))
        rparam2 = int(match.group('rparam2'))
        if match.group('left') == 'x' and match.group('right') == 'y':
            for y in range(rparam1, rparam2 + 1):
                clay_positions[lparam + y * 1j] = True
        elif match.group('left') == 'y' and match.group('right') == 'x':
            for x in range(rparam1, rparam2 + 1):
                clay_positions[x + lparam * 1j] = True
        else:
            raise SyntaxError(f'Unrecognised line {line}')
    y_list = [int(r.imag) for r in clay_positions]
    ymin, ymax = min(y_list), max(y_list)
    spring = 500
    tasks = deque([spring])
    while len(tasks) > 0:
        new_tasks = deque()
        for position in tasks:
            flowing_water.add(position)
            down, left, right = position + 1j, position - 1, position + 1

            if not clay_positions[down]:
                if down not in flowing_water and 1 <= down.imag <= ymax:
                    new_tasks.append(down)
                    continue
                if down not in still_water:
                    continue

            while not clay_positions[left] and (clay_positions[left + 1j] or left + 1j in still_water):
                flowing_water.add(left)
                left -= 1

            while not clay_positions[right] and (clay_positions[right + 1j] or right + 1j in still_water):
                flowing_water.add(right)
                right += 1

            if not clay_positions[left]:
                new_tasks.append(left)

            if not clay_positions[right]:
                new_tasks.append(right)

            if clay_positions[left] and clay_positions[right]:
                left += 1
                while left in flowing_water:
                    still_water.add(left)
                    left += 1
                new_tasks.append(position - 1j)

        tasks = new_tasks

    return len([pt for pt in flowing_water | still_water if ymin <= pt.imag <= ymax]), len(
        [pt for pt in still_water if ymin <= pt.imag <= ymax])


if __name__ == '__main__':
    with open('input.txt') as strata_file:
        strata_lines = strata_file.read().splitlines(keepends=False)
        p1, p2 = reservoir_research(strata_lines)
        print(f'Day 17, part 1: {p1}')
        print(f'Day 17, part 2: {p2}')
        # Day 17, part 1: 33362
        # Day 17, part 2: 27801
