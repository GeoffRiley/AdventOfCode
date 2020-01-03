from collections import defaultdict, deque
from enum import IntEnum

from intcode.intcode import Intcode


class Compass(IntEnum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4


class DroidStatus(IntEnum):
    WALL = 0
    SUCCESS = 1
    OXYGEN = 2


class MazeCell(IntEnum):
    UNKNOWN = 0
    EMPTY = 1
    WALL = 2
    OXYGEN = 3
    START = 4


CHARS = {
    MazeCell.EMPTY: " ",
    MazeCell.WALL: "█",
    MazeCell.OXYGEN: "O",
    MazeCell.UNKNOWN: "▒",
    MazeCell.START: "■"
}


class CellArray(object):
    def __init__(self):
        self.grid = defaultdict(MazeCell)
        self.pos = [0, 0]
        self.recent = defaultdict(int)

    def north(self, dist: int = 1):
        self.pos[1] += dist

    def south(self, dist: int = 1):
        self.pos[1] -= dist

    def west(self, dist: int = 1):
        self.pos[0] -= dist

    def east(self, dist: int = 1):
        self.pos[0] += dist

    def _hash_pos(self, p=None):
        if p is None:
            p = self.pos
        return f'{p[0]},{p[1]}'

    @property
    def hash_pos(self):
        return self._hash_pos()

    def set_here(self, s: MazeCell = MazeCell.UNKNOWN):
        self.grid[self.hash_pos] = s

    def move(self, d: Compass = Compass.NORTH, dist: int = 1):
        [self.north, self.south, self.west, self.east][d - 1](dist)

    def set_in_dir(self, d: Compass = Compass.NORTH, s: MazeCell = MazeCell.UNKNOWN):
        self.move(d)
        self.set_here(s)
        self.move(d, -1)

    def peek(self, d) -> MazeCell:
        self.move(d)
        res = self.grid.get(self.hash_pos, MazeCell.UNKNOWN)
        self.move(d, -1)
        return res

    def get_bounds(self):
        nrt, wst, sth, est = 0, 0, 0, 0
        for k, v in self.grid.items():
            x, y = [int(a) for a in k.split(',')]
            nrt = max(nrt, y)
            wst = min(wst, x)
            sth = min(sth, y)
            est = max(est, x)
        return nrt, wst, sth, est

    def image(self, plain: bool = False):
        nrt, wst, sth, est = self.get_bounds()
        lines = []
        multiplier = 1 if plain else 2
        for row in range(sth, nrt + 1):
            lines.append(''.join(CHARS[self.grid.get(self._hash_pos((col, row)), MazeCell.UNKNOWN)] * multiplier
                                 for col in range(wst, est + 1)))
        return lines

    def find_next_direction(self) -> Compass:
        for d in Compass:
            if self.peek(d) != MazeCell.UNKNOWN:
                continue
            return d
        newest = 1000000
        newest_dir = -1
        for d in Compass:
            if self.peek(d) == MazeCell.WALL:
                continue
            self.move(d)
            spot = str(self.pos)
            self.move(d, -1)
            if self.recent[spot] < newest:
                newest = self.recent[spot]
                newest_dir = d
        return newest_dir


class Droid(object):
    def __init__(self, mem_str: str):
        self._processor = Intcode(mem_str, 'Game')
        self._step_count = 0
        self._map_grid = CellArray()
        self._map_grid.set_here(MazeCell.START)
        self._current_path = deque()
        self._update_current_path()
        self._dir = Compass.NORTH

    def _update_current_path(self):
        here = self._map_grid.hash_pos
        if here in self._current_path:
            while self._current_path.pop() != here:
                continue
        self._current_path.append(here)

    def _receiver(self, output, trace=False):
        direction = self._dir
        if output == DroidStatus.WALL:
            self._map_grid.set_in_dir(direction, MazeCell.WALL)
            if trace:
                print('W', end='')
        elif output in [DroidStatus.SUCCESS, DroidStatus.OXYGEN]:
            self._map_grid.move(direction)
            self._map_grid.set_here(MazeCell.EMPTY if output == DroidStatus.SUCCESS else MazeCell.OXYGEN)
            if trace:
                print('.', end='')
            if output == DroidStatus.OXYGEN:
                self.path_to_oxygen_length = len(self._current_path)
                if trace:
                    print('#')
                    print(self.image())
                    print(f'Length of path = {self.path_to_oxygen_length}')
                # self._processor.nmi(True)  # Break early when oxygen found
        else:
            raise TypeError(f'Bad response from droid ({output})')
        self._update_current_path()
        self._map_grid.recent[str(self._map_grid.pos)] += 1
        self._step_count += 1
        if self._step_count % 100 == 0:
            print(f'{self._step_count}.', end='')
        if self._step_count > 5150:
            self._processor.nmi(True)

    def _sender(self):
        self._dir = self._map_grid.find_next_direction()
        return self._dir

    def run(self, inputs=None, trace=False):
        if inputs is None:
            inputs = []
        self._step_count = 0
        self._processor.connect(self._receiver, self._sender)
        self._processor.simulate(inputs, trace=trace, verbose=False)

    def image(self, plain: bool = False):
        in_img = self._map_grid.image(plain)
        if not plain:
            w = len(in_img[0])
            lines = '|\n|'.join(''.join(line) for line in in_img[::-1])
            top = '-' * (w + 1)
            out_img = f"/{top}\\\n|{lines}|\n\\{top}/"
        else:
            out_img = '\n'.join(''.join(line) for line in in_img[::-1])
        return out_img

    def spread_oxygen(self):
        in_img = self._map_grid.image(True)
        proc_img = [[ch for ch in line] for line in in_img]
        bleeds = [(col, row) for row, line in enumerate(in_img) for col, ch in enumerate(line) if ch == 'O']
        mins = 0
        while len(bleeds) > 0:
            old_bleeds = bleeds.copy()
            for b in old_bleeds:
                proc_img[b[1]][b[0]] = 'O'
                bleeds.remove(b)
                for x, y in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    if proc_img[b[1] + y][b[0] + x] == ' ':
                        bleeds.append((b[0] + x, b[1] + y))
            if len(bleeds) == 0:
                break
            mins += 1
        print('\n'.join(''.join(ch for ch in line) for line in proc_img[::-1]))
        return mins


if __name__ == '__main__':
    with open('input') as f:
        initial_cells = f.read()

    computer = Droid(initial_cells)

    print('Part 1')
    computer.run([], trace=False)
    print(f'COMPUTER: {str(computer)}')
    print(f'PART 1 RESULT: {computer.path_to_oxygen_length}')

    '''
    +----------------------------------------------------------------------------------+
    |░░██████░░██████░░██████████████████████████░░██████████░░██████████████░░██████░░|
    |██ > > v██ > > v██                 > > > > v██ > > > > v██         > > v██      ██|
    |██ ^██ v██ ^██ v██████████████████ ^██████ v██ ^██████ v██████████ ^██ v██████  ██|
    |██ ^██ > > ^██ > > > > > > > > v██ ^██     > > ^██  ██ > > > > > > ^██ > > > > v██|
    |██ ^██████████████████████████ v██ ^██████████████  ██████████████████████████ v██|
    |██ ^ < < < < < < < < < <██     > > ^██ v < <██ v < <    ██ v < < < < < <██ v < <██|
    |██  ██████████████████ ^██████  ██████ v██ ^██ v██ ^██████ v██████████ ^██ v████░░|
    |██  ██              ██ ^ < <██  ██ v < <██ ^██ v██ ^ < < < <██ > > v██ ^ < <██  ██|
    |██  ██  ██████████  ██████ ^██████ v██████ ^██ v██████████████ ^██ v██████████  ██|
    |██      ██      ██  ██  ██ ^ < < < <    ██ ^██ > > > > > > > > ^██ v██❉❉ < < < <██|
    |░░████████████  ██  ██  ██████████████████ ^██████████████████████ v██████████ ^██|
    |██              ██  ██          ██ > > > > ^██                  ██ v██ > > v██ ^██|
    |██  ██  ██████  ██  ██  ██████  ██ ^██████████  ██████████  ██  ██ v██ ^██ v██ ^██|
    |██  ██      ██  ██      ██      ██ ^██      ██          ██  ██  ██ > > ^██ v██ ^██|
    |██  ██████  ██  ██████  ██████████ ^██  ██  ██████████  ██  ██  ██████████ v██ ^██|
    |██      ██  ██      ██  ██ > > > > ^██  ██      ██      ██  ██          ██ v██ ^██|
    |░░████  ██  ██████  ██  ██ ^██████████  ██████████  ██████  ██  ██████████ v██ ^██|
    |██  ██  ██  ██      ██  ██ ^ < < < <██              ██  ██  ██  ██ v < < < <██ ^██|
    |██  ██  ██  ██████████  ██████████ ^██████████████  ██  ██  ██████ v██████████ ^██|
    |██  ██  ██          ██  ██      ██ ^ < <██ > > v██      ██      ██ v██ > > > > ^██|
    |██  ██  ██████████  ██  ██  ██████████ ^██ ^██ v██  ██████████  ██ v██ ^██████  ██|
    |██      ██      ██      ██          ██ ^██✠✠██ v██  ██ > > v██ v < <██ ^ < <██  ██|
    |██  ██████  ██  ██████████  ██  ██  ██ ^██████ v██████ ^██ v██ v████░░████ ^██  ██|
    |██  ██      ██      ██      ██  ██  ██ ^    ██ > > > > ^██ v██ > > v██ > > ^██  ██|
    |██  ██████████  ██  ██████████  ██████ ^██  ██████████████ v██████ v██ ^██████  ██|
    |██  ██          ██          ██  ██ > > ^██  ██ v < < < <██ > > v██ > > ^██      ██|
    |██  ██  ██████████████████  ██  ██ ^██████████ v██████ ^██████ v██████  ████████░░|
    |██      ██              ██  ██  ██ ^ < < < <██ v██ > > ^    ██ v██      ██ > > v██|
    |░░████████  ██  ██████████  ██  ██████████ ^██ v██ ^██████  ██ v██████████ ^██ v██|
    |██  ██      ██          ██              ██ ^ < <██ ^ < <██  ██ > > > > > > ^██ v██|
    |██  ██  ██████████████  ██████████████  ██████████████ ^████░░████████████████ v██|
    |██  ██          ██  ██              ██  ██          ██ ^ < <██ v < < < < < < < <██|
    |██  ██████████  ██  ██████████████  ██  ██████████  ██████ ^██ v████████████████░░|
    |██  ██      ██          ██      ██  ██  ██      ██      ██ ^ < <██              ██|
    |██  ██  ██  ██████████  ██  ██  ██  ██  ██  ██  ██████  ██████████████████  ██  ██|
    |██      ██          ██      ██  ██  ██  ██  ██                      ██      ██  ██|
    |██  ██████  ██████████████████  ██  ██  ██  ██████████████████████  ██  ██████  ██|
    |██      ██                  ██  ██      ██  ██          ██          ██  ██  ██  ██|
    |░░████  ██████████  ██████████  ██████████  ██  ██████  ██  ██████████  ██  ██  ██|
    |██              ██                          ██      ██                  ██      ██|
    |░░██████████████░░██████████████████████████░░██████░░██████████████████░░██████░░|
    +----------------------------------------------------------------------------------+
    Length of path = 318
    '''

    print('Part 2')

    img = computer.image(True)
    print(img)
    # print(f'COMPUTER: {str(computer)}')
    print(f'PART 2 RESULT: {computer.spread_oxygen()}')
    # # print('\n'.join(computer.get_log()))

    '''
    ▒███▒███▒█████████████▒█████▒███████▒███▒       ▒███▒███▒█████████████▒█████▒███████▒███▒
    █   █   █             █     █       █   █       █OOO█OOO█OOOOOOOOOOOOO█OOOOO█OOOOOOO█OOO█
    █ █ █ █ █████████ ███ █ ███ █████ █ ███ █       █O█O█O█O█████████O███O█O███O█████O█O███O█
    █ █   █         █ █     █ █       █     █       █O█OOO█OOOOOOOOO█O█OOOOO█O█OOOOOOO█OOOOO█
    █ █████████████ █ ███████ █████████████ █       █O█████████████O█O███████O█████████████O█
    █           █     █   █     █       █   █       █OOOOOOOOOOO█OOOOO█OOO█OOOOO█OOOOOOO█OOO█
    █ █████████ ███ ███ █ █ █ ███ █████ █ ██▒       █O█████████O███O███O█O█O█O███O█████O█O██▒
    █ █       █   █ █   █ █ █     █   █   █ █       █O█OOOOOOO█OOO█O█OOO█O█O█OOOOO█OOO█OOO█O█
    █ █ █████ ███ ███ ███ █ ███████ █ █████ █       █O█O█████O███O███O███O█O███████O█O█████O█
    █   █   █ █ █       █ █         █ █O    █       █OOO█OOO█O█O█OOOOOOO█O█OOOOOOOOO█O█OOOOO█
    ▒██████ █ █ █████████ ███████████ █████ █       ▒██████O█O█O█████████O███████████O█████O█
    █       █ █     █     █         █ █   █ █       █OOOOOOO█O█OOOOO█OOOOO█OOOOOOOOO█O█OOO█O█
    █ █ ███ █ █ ███ █ █████ █████ █ █ █ █ █ █       █O█O███O█O█O███O█O█████O█████O█O█O█O█O█O█
    █ █   █ █   █   █ █   █     █ █ █   █ █ █       █O█OOO█O█OOO█OOO█O█OOO█OOOOO█O█O█OOO█O█O█
    █ ███ █ ███ █████ █ █ █████ █ █ █████ █ █       █O███O█O███O█████O█O█O█████O█O█O█████O█O█
    █   █ █   █ █     █ █   █   █ █     █ █ █       █OOO█O█OOO█O█OOOOO█O█OOO█OOO█O█OOOOO█O█O█
    ▒██ █ ███ █ █ █████ █████ ███ █ █████ █ █       ▒██O█O███O█O█O█████O█████O███O█O█████O█O█
    █ █ █ █   █ █     █       █ █ █ █     █ █       █O█O█O█OOO█O█OOOOO█OOOOOOO█O█O█O█OOOOO█O█
    █ █ █ █████ █████ ███████ █ █ ███ █████ █       █O█O█O█████O█████O███████O█O█O███O█████O█
    █ █ █     █ █   █   █   █   █   █ █     █       █O█O█OOOOO█O█OOO█OOO█OOO█OOO█OOO█O█OOOOO█
    █ █ █████ █ █ █████ █ █ █ █████ █ █ ███ █       █O█O█████O█O█O█████O█O█O█O█████O█O█O███O█
    █   █   █   █     █ █■█ █ █   █   █   █ █       █OOO█OOO█OOO█OOOOO█O█■█O█O█OOO█OOO█OOO█O█
    █ ███ █ █████ █ █ █ ███ ███ █ █ ██▒██ █ █       █O███O█O█████O█O█O█O███O███O█O█O██▒██O█O█
    █ █   █   █   █ █ █   █     █ █   █   █ █       █O█OOO█OOO█OOO█O█O█OOO█OOOOO█O█OOO█OOO█O█
    █ █████ █ █████ ███ █ ███████ ███ █ ███ █       █O█████O█O█████O███O█O███████O███O█O███O█
    █ █     █     █ █   █ █     █   █   █   █       █O█OOOOO█OOOOO█O█OOO█O█OOOOO█OOO█OOO█OOO█
    █ █ █████████ █ █ █████ ███ ███ ███ ████▒       █O█O█████████O█O█O█████O███O███O███O████▒
    █   █       █ █ █     █ █     █ █   █   █       █OOO█OOOOOOO█O█O█OOOOO█O█OOOOO█O█OOO█OOO█
    ▒████ █ █████ █ █████ █ █ ███ █ █████ █ █       ▒████O█O█████O█O█████O█O█O███O█O█████O█O█
    █ █   █     █       █   █   █ █       █ █       █O█OOO█OOOOO█OOOOOOO█OOO█OOO█O█OOOOOOO█O█
    █ █ ███████ ███████ ███████ ██▒████████ █       █O█O███████O███████O███████O██▒████████O█
    █ █     █ █       █ █     █   █         █       █O█OOOOO█O█OOOOOOO█O█OOOOO█OOO█OOOOOOOOO█
    █ █████ █ ███████ █ █████ ███ █ ████████▒       █O█████O█O███████O█O█████O███O█O████████▒
    █ █   █     █   █ █ █   █   █   █       █       █O█OOO█OOOOO█OOO█O█O█OOO█OOO█OOO█OOOOOOO█
    █ █ █ █████ █ █ █ █ █ █ ███ █████████ █ █       █O█O█O█████O█O█O█O█O█O█O███O█████████O█O█
    █   █     █   █ █ █ █ █           █   █ █       █OOO█OOOOO█OOO█O█O█O█O█OOOOOOOOOOO█OOO█O█
    █ ███ █████████ █ █ █ ███████████ █ ███ █       █O███O█████████O█O█O█O███████████O█O███O█
    █   █         █ █   █ █     █     █ █ █ █       █OOO█OOOOOOOOO█O█OOO█O█OOOOO█OOOOO█O█O█O█
    ▒██ █████ █████ █████ █ ███ █ █████ █ █ █       ▒██O█████O█████O█████O█O███O█O█████O█O█O█
    █       █             █   █         █   █       █OOOOOOO█OOOOOOOOOOOOO█OOO█OOOOOOOOO█OOO█
    ▒███████▒█████████████▒███▒█████████▒███▒       ▒███████▒█████████████▒███▒█████████▒███▒
    
    PART 2 RESULT: 390
    '''
