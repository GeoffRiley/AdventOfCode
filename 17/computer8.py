from intcode.intcode import Intcode


class Ascii(object):
    def __init__(self, mem_str: str):
        self._processor = Intcode(mem_str, 'ASCII')
        self._port_view = [[]]
        self._robot_at = (-1, -1)
        self._robot_point = '^'
        self._vac_mode = False
        self._cmd = ''

    def reset_core(self):
        self._processor.reset_core()

    def _receiver(self, output, trace=False):
        c = chr(output)
        if self._vac_mode:
            if 128 > output > 31:
                print(c, end='')
            elif output == 10:
                print()
            else:
                print(f'[{output}]')
        else:
            if output == 10:
                if len(self._port_view[-1]) > 0:
                    self._port_view.append([])
            else:
                self._port_view[-1].append(c)
                if c in ['^v<>']:
                    self._robot_at = (len(self._port_view[-1]) - 1, len(self._port_view) - 1)
                    self._robot_point = c

    def _sender(self):
        return self._processor._input.pop()

    def run(self, inputs=None, trace=False, vac=False):
        if inputs is None:
            inputs = []
        if vac:
            self._vac_mode = True
            self._processor.core[0] = 2
        self._processor.connect(self._receiver, self._sender)
        self._processor.simulate(inputs, trace=trace, verbose=True)
        if len(self._port_view[-1]) == 0:
            self._port_view.remove(self._port_view[-1])

    def get_cell(self, col, row):
        if col < 0 or row < 0 or row >= len(self._port_view) or col >= len(self._port_view[row]):
            return '.'
        return self._port_view[row][col]

    def get_neighbours(self, col, row):
        return self._port_view[row - 1][col] + \
               self._port_view[row][col + 1] + \
               self._port_view[row + 1][col] + \
               self._port_view[row][col - 1]

    def find_crossings(self):
        alignments = []
        for row in range(1, len(self._port_view) - 1):
            for col in range(1, len(self._port_view[row]) - 1):
                if self._port_view[row][col] == '#':
                    # on scaffold
                    if self.get_neighbours(col, row) == '####':
                        # on junction
                        self._port_view[row][col] = 'O'
                        alignments.append((col) * (row))
        return sum(alignments)

    # def get_full_path(self):
    #     path = []
    #     while True:
    #         col, row = self._robot_at
    #         neighbours = self.get_neighbours(col, row)


if __name__ == '__main__':
    with open('input') as f:
        mem_code = f.read()

    computer = Ascii(mem_code)

    computer.run(trace=False)

    crossings = computer.find_crossings()
    print('\n'.join(''.join(c for c in line) for line in computer._port_view))
    print(f'Part 1: {crossings}')

    '''
    ####^.................................. 
    #...................................... 
    #...................................... 
    #......................................   -: MANUAL WORKING :-
    ###########...###########.............. 
    ..........#...#........................ L,4,L,4,L,10,R,4,       A
    ..........#...#........................ R,4,L,4,L,4,R,8,R,10,   B
    ..........#...#........................ L,4,L,4,L,10,R,4,       A
    ......#####...#........................ R,4,L,10,R,10,          C
    ......#.......#........................ L,4,L,4,L,10,R,4,       A
    ......#.......#.###########...######### R,4,L,10,R,10,          C
    ......#.......#.#.........#...#.......# R,4,L,4,L,4,R,8,R,10,   B
    ......#####...#####.......#...#.......# R,4,L,10,R,10,          C
    ..........#.....#.#.......#...#.......# R,4,L,10,R,10,          C
    ....#####.#.....#.#.......#####.......# R,4,L,4,L,4,R,8,R,10    B
    ....#...#.#.....#.#...................# 
    ....#...#.#...#####...................# 
    ....#...#.#...#.#.....................# A,B,A,C,A,C,B,C,C,B
    ....#...###########...................# L,4,L,4,L,10,R,4
    ....#.....#...#.#.#...................# R,4,L,4,L,4,R,8,R,10
    ###########.#####.#...............##### R,4,L,10,R,10
    #...#.......#.#...#...............#.... n
    #...#.......#.#...#...............#.... 
    #...#.......#.#...#...............#.... 
    #####.......###########...........#.... 
    ..............#...#...#...........#.... 
    ..............###########.........#.... 
    ..................#...#.#.........#.... 
    ..................#####.#.........#.... 
    ........................#.........#.... 
    ........................###########.... 
    '''
    computer.reset_core()
    instructions = [
        'A,B,A,C,A,C,B,C,C,B',
        'L,4,L,4,L,10,R,4',
        'R,4,L,4,L,4,R,8,R,10',
        'R,4,L,10,R,10',
        'n'
    ]
    computer.run([ord(c) for c in '\n'.join(instructions) + '\n'], trace=False, vac=True)

    '''
    Main:
    Function A:
    Function B:
    Function C:
    Continuous video feed?
    
    #####..................................
    #......................................
    #......................................
    #......................................
    ###########...##########>..............
    ..........#...#........................
    ..........#...#........................
    ..........#...#........................
    ......#####...#........................
    ......#.......#........................
    ......#.......#.###########...#########
    ......#.......#.#.........#...#.......#
    ......#####...#####.......#...#.......#
    ..........#.....#.#.......#...#.......#
    ....#####.#.....#.#.......#####.......#
    ....#...#.#.....#.#...................#
    ....#...#.#...#####...................#
    ....#...#.#...#.#.....................#
    ....#...###########...................#
    ....#.....#...#.#.#...................#
    ###########.#####.#...............#####
    #...#.......#.#...#...............#....
    #...#.......#.#...#...............#....
    #...#.......#.#...#...............#....
    #####.......###########...........#....
    ..............#...#...#...........#....
    ..............###########.........#....
    ..................#...#.#.........#....
    ..................#####.#.........#....
    ........................#.........#....
    ........................###########....
    
    [597517]
    '''
