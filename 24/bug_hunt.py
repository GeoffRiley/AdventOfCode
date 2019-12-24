# Built on game of life code from 2015 AoC day 18
# Got too complex for part 2 though, so started afresh in bug_hunt_2.py without classes and an estimation of
# the full depth of recursion from scratch


class Cell(object):
    def __init__(self, row=0, col=0, depth=0):
        self.neighbours = []
        self.current_state = False
        self.next_state = False
        self.fixed = False
        self.recursion_point = False
        self._row = row
        self._col = col
        self._depth = depth

    @property
    def pos(self):
        return (self._row, self._col), self._depth

    def check_neighbours_valid(self):
        self.neighbours = list(set(self.neighbours))

    def count_neighbours(self) -> int:
        count = 0
        if not self.recursion_point:
            for n in self.neighbours:
                if n.current_state:
                    count += 1
        return count

    def ready_change(self):
        if self.fixed:
            self.next_state = True
        else:
            count = self.count_neighbours()
            if self.current_state:
                self.next_state = count == 1
            else:
                self.next_state = count in [1, 2]

    def switch(self):
        self.current_state = self.next_state

    def __repr__(self):
        return f'{self.pos}→{self.__str__()}'

    def __str__(self):
        return '?' if self.recursion_point else '#' if self.current_state else '.'


class LifeGrid(object):
    def __init__(self, depth, recursive=False):
        self._depth = depth
        self.grid = self._init_blank_level(depth)
        self.recursive = recursive
        if recursive:
            self.centre_cell().recursion_point = True

    @staticmethod
    def _init_blank_level(depth=0):
        return [[Cell(row, col, depth) for col in range(5)] for row in range(5)]

    def centre_cell(self):
        return self.grid[2][2]

    def add_neighbour(self, row, col, neigh: Cell):
        if neigh not in self.grid[row][col].neighbours:
            if not self.recursive or (self.recursive and neigh != self.centre_cell()):
                self.grid[row][col].neighbours.append(neigh)

    def check_all_neighbours_valid(self):
        for line in self.grid:
            for cell in line:
                cell.check_neighbours_valid()

    def on_lamps(self):
        return sum(1 for line in self.grid for cell in line if cell.current_state)

    def __str__(self):
        return ''.join(str(c) for line in self.grid for c in line)


class Life(object):
    def __init__(self, initial_grid, recursive=False):
        self._grid_levels = dict()
        self._recursive = recursive
        self._level = 0
        self._level_min = 0
        self._level_max = 0
        self.setup_grid(initial_grid, recursive=recursive)

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, lvl):
        self._level = lvl
        if lvl not in self._grid_levels.keys():
            self._grid_levels[lvl] = LifeGrid(lvl, recursive=self._recursive)
            self._level_max = max(lvl, self._level_max)
            self._level_min = min(lvl, self._level_min)
            if lvl + 1 in self._grid_levels.keys():
                level_up = self._grid_levels[lvl + 1]
            else:
                level_up = None
            if lvl - 1 in self._grid_levels.keys():
                level_down = self._grid_levels[lvl - 1]
            else:
                level_down = None
            self.fixup_neighbours(level_down, self._grid_levels[lvl], level_up)
        self.sort_recursive()
        self._grid_levels[lvl].check_all_neighbours_valid()

    def fixup_neighbours(self, lvld: LifeGrid or None, lvl: LifeGrid, lvlu: LifeGrid or None):
        height = len(lvl.grid)
        width = len(lvl.grid[0])
        mid_h = height // 2
        mid_w = width // 2
        centre_cell = lvl.centre_cell()
        for row, line in enumerate(lvl.grid):
            for col, cell in enumerate(line):
                cell.neighbours = [lvl.grid[r][c] for r, c in self.neighbours(row, col)]
                if self._recursive:
                    if centre_cell in cell.neighbours:
                        cell.neighbours.remove(centre_cell)
                    if (row, col) == (mid_h, mid_w):
                        if lvld:
                            for c in range(width):
                                lvld.add_neighbour(0, c, lvl.grid[row - 1][col])
                                lvld.add_neighbour(height - 1, c, lvl.grid[row + 1][col])
                                lvl.add_neighbour(row - 1, c, lvld.grid[0][c])
                                lvl.add_neighbour(row + 1, c, lvld.grid[height - 1][c])
                            for r in range(height):
                                lvld.add_neighbour(r, 0, lvl.grid[row][col - 1])
                                lvld.add_neighbour(r, width - 1, lvl.grid[row][col + 1])
                                lvl.add_neighbour(row, col - 1, lvld.grid[r][0])
                                lvl.add_neighbour(row, col + 1, lvld.grid[r][width - 1])
                    else:
                        if lvlu:
                            if row == 0:
                                for c in range(width):
                                    cell.neighbours.append(lvlu.grid[mid_h - 1][mid_w])
                                    lvlu.grid[mid_h - 1][mid_w].neighbours.append(cell)
                            if row == height - 1:
                                for c in range(width):
                                    cell.neighbours.append(lvlu.grid[mid_h + 1][mid_w])
                                    lvlu.grid[mid_h + 1][mid_w].neighbours.append(cell)
                            if col == 0:
                                for r in range(height):
                                    cell.neighbours.append(lvlu.grid[mid_h][mid_w - 1])
                                    lvlu.grid[mid_h][mid_w - 1].neighbours.append(cell)
                            if col == width - 1:
                                for r in range(height):
                                    cell.neighbours.append(lvlu.grid[mid_h][mid_w + 1])
                                    lvlu.grid[mid_h][mid_w + 1].neighbours.append(cell)

    def setup_grid(self, initial_grid, recursive=False, level=0):
        self._recursive = recursive
        self.level = level
        for row, line in enumerate(self.grid):
            for col, cell in enumerate(line):
                cell.current_state = initial_grid[row][col] == '#'

    def sort_recursive(self):
        if self._recursive:

            min_level = ''.join([str(cell) for line in self._grid_levels[self._level_min].grid for cell in line])
            if min_level.find('#') >= 0:
                self.level = self._level_min - 1
            max_level = ''.join([str(cell) for line in self._grid_levels[self._level_max].grid for cell in line])
            if max_level.find('#') >= 0:
                self.level = self._level_max + 1

    @property
    def grid(self):
        return self._grid_levels[self.level].grid

    @staticmethod
    def neighbours(row, col):
        for n_r, n_c in [[-1, 0], [0, -1], [0, 1], [1, 0]]:
            pos = row + n_r, col + n_c
            if 0 <= pos[0] < 5 and 0 <= pos[1] < 5:
                yield pos

    def on_lamps(self):
        return sum(grid.on_lamps() for grid in self._grid_levels.values())

    def generation(self):
        for lvl in range(self._level_min, self._level_max + 1):
            self.level = lvl
            for line in self.grid:
                for cell in line:
                    cell.ready_change()
        for lvl in range(self._level_min, self._level_max + 1):
            self.level = lvl
            for line in self.grid:
                for cell in line:
                    cell.switch()

    def __str__(self):
        return ''.join(str(cell) for line in self.grid for cell in line)

    def print_grid(self):
        for lvl in range(self._level_min, self._level_max + 1):
            self.level = lvl
            self.level = lvl  # Side effects: bad, but need to set twice until fixed!!
            print(f'Depth {self.level}:')
            for line in self.grid:
                print(''.join(str(cell) for cell in line))
            print()


if __name__ == '__main__':
    with open('input') as f:
        initial_grid = f.read().splitlines(keepends=False)
    life = Life(initial_grid)
    pre_states = set()
    while str(life) not in pre_states:
        pre_states.add(str(life))
        life.generation()

    life.print_grid()

    part1 = sum(1 << i for i, c in enumerate(str(life)) if c == "#")
    print(f'Part 1: {part1}')
    assert part1 == 18375063
    # Part 1: 18375063
    # That's the right answer! You are one gold star closer to rescuing Santa.
    # You got rank 242 on this star's leaderboard. [Continue to Part Two]

#     initial_grid2 = '''....#
# #..#.
# #.?##
# ..#..
# #....'''.splitlines(keepends=False)
#
#     life2 = Life(initial_grid2, recursive=True)
#
#     print('*'*40)
#     life2.print_grid()
#     print('*'*20)
#     life2.generation()
#     life2.print_grid()
#     print('*'*20)

# for _ in range(9):
#     life2.generation()
# life2.print_grid()
#
# assert life2.on_lamps() == 99

# print(f'Part 2: {life.on_lamps()}')
# Part 2:
