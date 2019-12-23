class Cell(object):
    def __init__(self):
        self.neighbours = [None for _ in range(8)]
        self.current_state = False
        self.next_state = False
        self.fixed = False

    def count_neighbours(self) -> int:
        count = 0
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
                self.next_state = count in [2, 3]
            else:
                self.next_state = count == 3

    def switch(self):
        self.current_state = self.next_state

    def __str__(self):
        return '#' if self.current_state else '.'


class Life(object):
    def __init__(self, initial_grid):
        self.grid = [[Cell() for _ in range(100)] for _ in range(100)]
        self.setup_grid(initial_grid)

    def setup_grid(self, initial_grid, fixed_corners=False):
        for row, line in enumerate(self.grid):
            for col, cell in enumerate(line):
                if fixed_corners and (col == 0 or col == 99) and (row == 0 or row == 99):
                    cell.current_state = True
                    cell.fixed = True
                    cell.neighbours = []
                else:
                    cell.current_state = initial_grid[row][col] == '#'
                    cell.neighbours = [self.grid[r][c] for r, c in self.neighbours(row, col)]

    def neighbours(self, row, col):
        for n_r, n_c in [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]:
            pos = row + n_r, col + n_c
            if 0 <= pos[0] < 100 and 0 <= pos[1] < 100:
                yield pos

    def on_lamps(self):
        return sum(1 for line in self.grid for cell in line if cell.current_state)

    def generation(self):
        for line in self.grid:
            for cell in line:
                cell.ready_change()
        for line in self.grid:
            for cell in line:
                cell.switch()

    def print_grid(self):
        for line in self.grid:
            for cell in line:
                print(cell, end='')
            print()


if __name__ == '__main__':
    with open('input') as f:
        initial_grid = f.read().splitlines(keepends=False)
    life = Life(initial_grid)
    for _ in range(100):
        life.generation()
    life.print_grid()

    print(f'Part 1: {life.on_lamps()}')
    # Part 1: 814

    life.setup_grid(initial_grid, fixed_corners=True)
    for _ in range(100):
        life.generation()
    life.print_grid()

    print(f'Part 2: {life.on_lamps()}')
    # Part 2: 924
