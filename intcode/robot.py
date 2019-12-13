from collections import defaultdict

from intcode.icsupport import RobotPuck, Rect, Heading
from intcode.intcode import Intcode


class Robot(object):
    def __init__(self, mem_str: str):
        self._processor = Intcode(mem_str, 'Painting Robot')
        self._grid_pos = RobotPuck()
        self._grid_history = defaultdict(int)
        self._painted = defaultdict(bool)
        self._paint = True
        self._rect = Rect()
        self.move_count = 0

    def reset_core(self):
        self._processor.reset_core()
        self._grid_pos = RobotPuck()
        self._grid_history.clear()
        self._painted.clear()
        self._paint = True
        self._rect = Rect()
        self.move_count = 0

    def get_log(self):
        return self._processor.get_log()

    def _receiver(self, output, trace=False):
        if self._paint:
            if trace:
                self._processor.log(f'        Painting ({self._location}) {"white" if output == 1 else "black"}')
            self._grid_history[self._location] = output
            self._painted[self._location] = True
        else:
            if trace:
                self._processor.log(f'        Turn {"right" if output == 1 else "left"}')
            self._grid_pos.turn(output)
            self._grid_pos.forward()
            self.move_count += 1
            self._rect.include(self._grid_pos)
            self._processor.receiver(self._grid_history[self._location])
        self._paint = not self._paint

    @property
    def _location(self):
        return f'{self._grid_pos.x},{self._grid_pos.y}'

    def run(self, inputs=None, trace=False):
        if inputs is None:
            inputs = []
        self._processor.connect(self._receiver)
        self._processor.simulate(inputs, trace=trace, verbose=False)

    def visited(self):
        return len(self._painted)

    def image(self):
        w = self._rect.width
        h = self._rect.height
        img = [['..' for x in range(w + 1)] for x in range(h + 1)]
        for k, p in self._grid_history.items():
            x, y = [int(n) for n in k.split(',')]
            try:
                if p == 1:
                    img[abs(y)][x] = '##'
                else:
                    img[abs(y)][x] = '  '
            except IndexError:
                print(f'Index error: ({x},{y}) → ({x},{abs(y)}) : {k}:{p}')
        return '\n'.join(''.join(line) for line in img)

    def __str__(self):
        return f'{self._processor.name}: {self._grid_pos} {Heading(self._grid_pos.dir).name} {self._rect} (moves: {self.move_count})'
