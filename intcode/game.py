from collections import defaultdict

from intcode.icsupport import Spot, Rect, sign
from intcode.intcode import Intcode


class Game(object):
    def __init__(self, mem_str: str):
        self._processor = Intcode(mem_str, 'Game')
        self._output_state = 0
        self._output_position = Spot()
        self._game_grid = defaultdict(int)
        self._rect = Rect()
        self.score = 0
        self.bat_pos = 0
        self.ball_pos = 0

    def reset_core(self):
        self._processor.reset_core()
        self._output_state = 0
        self._game_grid.clear()
        self._rect = Rect()
        self.score = 0
        self.bat_pos = 0
        self.ball_pos = 0

    def _receiver(self, output, trace=False):
        if self._output_state == 0:
            self._output_position.x = output
        elif self._output_state == 1:
            self._output_position.y = output
        else:
            if self._output_position.as_tuple() == (-1, 0):
                self.score = output
                if trace:
                    print(f'{self.image()}\nSCORE: {self.score}')
            else:
                self._rect.include(self._output_position.as_tuple())
                self._game_grid[str(self._output_position)] = output
                if output == 3:
                    self.bat_pos = self._output_position.x
                elif output == 4:
                    self.ball_pos = self._output_position.x
        self._output_state = (self._output_state + 1) % 3

    def _sender(self):
        return sign(self.ball_pos - self.bat_pos)

    def run(self, inputs=None, trace=False):
        if inputs is None:
            inputs = []
        self._output_state = 0
        self._processor.connect(self._receiver, self._sender)
        self._processor.simulate(inputs, trace=trace, verbose=True)

    def count_block_tiles(self):
        return sum(1 for n in self._game_grid.values() if n == 2)

    def set_freeplay(self):
        self._processor.core[0] = 2

    IMAGE_ICONS = {0: '  ', 1: '##', 2: 'XX', 3: '==', 4: 'OO'}

    def image(self):
        w = self._rect.width
        h = self._rect.height
        img = [['..' for x in range(w + 1)] for x in range(h + 1)]
        for k, p in self._game_grid.items():
            x, y = [int(n) for n in k.split(',')]
            try:
                if p in self.IMAGE_ICONS:
                    img[abs(y)][x] = self.IMAGE_ICONS[p]
                else:
                    img[abs(y)][x] = '  '
            except IndexError:
                print(f'Index error: ({x},{y}) → ({x},{abs(y)}) : {k}:{p}')
        return '\n'.join(''.join(line) for line in img)

    def get_log(self):
        return self._processor.get_log()

    def __str__(self):
        return f'{self.__class__.__name__} [\n{self.image()}\n]'
