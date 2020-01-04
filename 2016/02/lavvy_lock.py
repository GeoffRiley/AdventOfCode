class ConfinedPointer(object):
    def __init__(self):
        self.grid = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
        self.x = 1
        self.y = 1
        self.max_x = 2
        self.max_y = 2

    def set_alternate_grid(self):
        self.grid = [
            ['', '', '1', '', ''],
            ['', '2', '3', '4', ''],
            ['5', '6', '7', '8', '9'],
            ['', 'A', 'B', 'C', ''],
            ['', '', 'D', '', '']
        ]
        self.x = 0
        self.y = 2
        self.max_x = 4
        self.max_y = 4

    def loc(self, x=0, y=0):
        return self.grid[self.y + y][self.x + x]

    def move_up(self):
        if self.y > 0 and self.loc(y=-1):
            self.y -= 1

    def move_down(self):
        if self.y < self.max_y and self.loc(y=1):
            self.y += 1

    def move_left(self):
        if self.x > 0 and self.loc(x=-1):
            self.x -= 1

    def move_right(self):
        if self.x < self.max_x and self.loc(x=1):
            self.x += 1

    @property
    def key(self):
        return self.loc()

    def action(self, direction):
        if direction == 'U':
            self.move_up()
        elif direction == 'D':
            self.move_down()
        elif direction == 'L':
            self.move_left()
        elif direction == 'R':
            self.move_right()
        else:
            raise ValueError(f'Unknown movement value {direction}')


def lavvy_decode(code: str, part2=False) -> str:
    ptr = ConfinedPointer()
    if part2:
        ptr.set_alternate_grid()
    ret = ''
    for line in code.splitlines(keepends=False):
        for c in line:
            ptr.action(c)
        ret += ptr.key
    return ret


if __name__ == '__main__':
    with open('input') as f:
        this_code = f.read()
    print(f'Part 1: {lavvy_decode(this_code)}')
    print(f'Part 2: {lavvy_decode(this_code, True)}')
    # Part 1: 47978
    # Part 2: 659AD
