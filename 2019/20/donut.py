"""
NOT WORKING!!  YET.
"""
from dataclasses import dataclass

WALL = '#'
WALK = '.'
SPACE = ' '


@dataclass
class Rect(object):
    top: int
    left: int
    bottom: int
    right: int

    def is_inside(self, row, col):
        return (self.left <= col <= self.right) and (self.top <= row <= self.bottom)

    def is_outside(self, row, col):
        return not self.is_inside(row, col)

    def is_on(self, row, col):
        return self.left == col or self.right == col or self.top == row or self.bottom == row

    def __key__(self):
        return self.top, self.left, self.bottom, self.right

    def __lt__(self, other):
        return self.__key__() < other.__key__()

    def __hash__(self):
        return hash(self.__key__())


@dataclass
class CellLink(object):
    row: int
    col: int
    warp_level: int = 0

    @property
    def pos(self):
        return self.row, self.col

    def __key__(self):
        return self.row, self.col, self.warp_level

    def __lt__(self, other):
        return self.__key__() < other.key()

    def __hash__(self):
        return hash(self.__key__())


class DonutMaze(object):
    def __init__(self, recursive=False):
        self.grid = []
        self.grid_width = 0
        self.grid_height = 0
        self.grid_links = {}
        self.grid_warps = {}
        self.warp_lookups = dict()
        self.outer_boundary = Rect(0, 0, 0, 0)
        self.inner_boundary = Rect(0, 0, 0, 0)
        self.recursive = recursive

    def reset(self):
        self.grid = []
        self.grid_width = 0
        self.grid_height = 0
        self.grid_links = {}
        self.grid_warps = {}
        self.warp_lookups = dict()
        self.outer_boundary = Rect(0, 0, 0, 0)
        self.inner_boundary = Rect(0, 0, 0, 0)

    def neighbours(self, centre_row, centre_col, path_ways=True):
        for dir_row, dir_col in ((0, 1), (-1, 0), (0, -1), (1, 0)):
            target_row, target_col = (centre_row + dir_row, centre_col + dir_col)

            if 0 <= target_row < self.grid_height and 0 <= target_col < self.grid_width:
                try:
                    if path_ways:
                        if self.grid[target_row][target_col] == WALK:
                            yield target_row, target_col
                    else:
                        if self.grid[target_row][target_col] not in [WALL, SPACE, WALK]:
                            yield target_row, target_col
                except IndexError:
                    continue

    def ident_warp(self, pos):
        p_row, p_col = pos
        warp_name = ''
        warp_pos = None
        warp_level = 0
        for n_row, n_col in self.neighbours(p_row, p_col, path_ways=False):
            # if self.grid[n_row][n_col].isupper():
            # this is our 'other' letter… but is it the first or second?
            if (p_row < n_row) or (p_col < n_col):
                warp_name = self.grid[p_row][p_col] + self.grid[n_row][n_col]
            else:
                warp_name = self.grid[n_row][n_col] + self.grid[p_row][p_col]

            warp_pos = [pos, (n_row, n_col)]
            if warp_name in ['AA', 'ZZ']:
                warp_level = 0
            elif self.outer_boundary.is_outside(n_row, n_col):
                warp_level = 1
            else:
                warp_level = -1
            break  # Only looking for a single result!
        else:
            raise ValueError(f'Single value warp, {self.grid[p_row][p_col]}, not possible @{pos}')
        # find '.' adjacent to warp label
        for warp in warp_pos:
            for n_row, n_col in self.neighbours(*warp):
                if self.grid[n_row][n_col] == WALK:
                    self.warp_lookups[(n_row, n_col)] = warp_name
                    return warp_name, CellLink(n_row, n_col, warp_level=warp_level)
        raise ValueError(f'Unable to locate target point for warp {warp_name} around label @{warp_pos}')

    def setup_grid(self, map_text):
        self.reset()
        self.grid = [[col_num for col_num in line] for line in map_text.splitlines(keepends=False)]
        self.grid_height = len(self.grid)
        self.grid_width = max(len(self.grid[n]) for n in range(self.grid_height))

        # check for donut dimensions
        self.setup_horizontal_boundaries()
        self.setup_vertical_boundaries()

        for row_num, row_data in enumerate(self.grid):
            for col_num, cell in enumerate(row_data):
                pos = (row_num, col_num)
                if cell not in [WALL, SPACE]:
                    if pos not in self.grid_links:
                        self.grid_links[pos] = set()

                    if cell.isupper():
                        w, lk = self.ident_warp(pos)
                        if w not in self.grid_warps:
                            self.grid_warps[w] = set()
                        self.grid_warps[w].add(lk)
                    else:
                        for neigh in self.neighbours(*pos):
                            self.grid_links[pos].add(CellLink(*neigh))
        # apply warp fix-ups
        for warp_name, warp_positions in self.grid_warps.items():
            print(f'{warp_name}: {warp_positions}')
            if len(warp_positions) == 2:
                a, b = warp_positions
                self.grid_links[a.pos].add(b)
                self.grid_links[b.pos].add(a)

    def setup_horizontal_boundaries(self):
        a_row = self.grid_height // 2
        p = 0
        for col_num, ch in enumerate(self.grid[a_row]):
            if ch in [WALK, WALL]:
                if p == 0:
                    self.outer_boundary.left = col_num
                    p += 1
                elif p == 2:
                    self.inner_boundary.right = col_num
                    p += 1
            else:
                if p == 1:
                    self.inner_boundary.left = col_num - 1
                    p += 1
                elif p == 3:
                    self.outer_boundary.right = col_num - 1
                    p += 1
                    break

    def setup_vertical_boundaries(self):
        a_col = self.grid_width // 2
        p = 0
        for row_num in range(self.grid_height):
            ch = self.grid[row_num][a_col]
            if ch in [WALK, WALL]:
                if p == 0:
                    self.outer_boundary.top = row_num
                    p += 1
                elif p == 2:
                    self.inner_boundary.bottom = row_num
                    p += 1
            else:
                if p == 1:
                    self.inner_boundary.top = row_num - 1
                    p += 1
                elif p == 3:
                    self.outer_boundary.bottom = row_num - 1
                    p += 1
                    break

    def find_route(self, src, target):
        hydra = [(src, [src], 0)]
        visited = []
        warped = False
        while len(hydra) > 0:
            old_hydra = hydra.copy()
            for pos, pth, lvl in old_hydra:
                if pos.pos in self.warp_lookups:
                    print(f'Visited {self.warp_lookups[pos.pos]} level {lvl}')
                visited.append((pos.pos, lvl))
                hydra.remove((pos, pth, lvl))
                neigh: CellLink
                for neigh in self.grid_links[pos.pos]:
                    if (neigh.pos, lvl) in visited:
                        continue
                    if lvl == 0 and neigh == target:
                        return pth
                    if lvl == 0 and neigh.warp_level != 0 and self.outer_boundary.is_on(*pos.pos):
                        continue
                    new_path = pth.copy()
                    if warped:
                        new_path.append(CellLink(*neigh.pos, lvl))
                        hydra.append((neigh, new_path, lvl))
                        warped = False
                    elif neigh.warp_level != 0:
                        new_path.append(CellLink(*neigh.pos, lvl + neigh.warp_level))
                        hydra.append((neigh, new_path, lvl + neigh.warp_level))
                        warped = True
                    else:
                        new_path.append(CellLink(*neigh.pos, lvl))
                        hydra.append((neigh, new_path, lvl))
        raise LookupError('No route found!')


def donut(maze, rec=False) -> int:
    this_donut = DonutMaze(rec)
    this_donut.setup_grid(maze)
    print(f'Enter maze at {this_donut.grid_warps["AA"]} and exit at {this_donut.grid_warps["ZZ"]}')
    res = this_donut.find_route(src=next(iter(this_donut.grid_warps["AA"])),
                                target=next(iter(this_donut.grid_warps["ZZ"])))
    count = 0
    for p in res:
        count += 1
        for w, l in this_donut.grid_warps.items():
            if p.pos in [i.pos for i in l]:
                if count > 1:
                    print(f'{count} steps')
                print(f'{w} : {p}')
                count = 0
                break
    if count > 0:
        print(f'{count} steps')
    return len(res)


if __name__ == '__main__':
    with open('input') as f:
        maze_str = f.read()

    print(f'Part 1: {donut(maze_str)}')
    # Part 1: 632
