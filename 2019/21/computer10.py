"""
The springdroid
"""
from intcode.intcode import Intcode


class SpringDroid(object):
    def __init__(self, mem_str: str):
        self._processor = Intcode(mem_str)
        self.prompt = ''
        self.result = None
        self.script = ''

    def reset_core(self):
        self._processor.reset_core()
        self.prompt = ''
        self.result = None
        self.script = ''

    def _receiver(self, output, trace):
        if output > 255:
            self.result = output
        else:
            if output == 10:
                if self.prompt == 'Input instructions:':
                    self._processor.receiver(self.script)
                self.prompt = ''
            else:
                self.prompt += chr(output)
            print(chr(output), end='')

    def run(self):
        self._processor.connect(self._receiver)
        self._processor.simulate()


if __name__ == '__main__':
    with open('input') as f:
        mem_dump = f.read()

    droid = SpringDroid(mem_dump)
    # (A' or B' or C') and D
    droid.script = '\n'.join([
        'NOT A J',
        'NOT B T',
        'OR T J',
        'NOT C T',
        'OR T J',
        'AND D J',
        'WALK'
    ]) + '\n'
    droid.run()
    print(f'Part 1: {droid.result}')
    '''
    That's the right answer! You are one gold star closer to rescuing Santa. 
    You got rank 562 on this star's leaderboard. [Continue to Part Two]
    '''
    droid.reset_core()
    # (A' or B' or C') and D
    # De Morgan:
    # (A and B and C)' and D
    # extend with: … and (E or H)'
    droid.script = '\n'.join([
        'OR A J',
        'AND B J',
        'AND C J',
        'NOT J J',
        'AND D J',
        'OR E T',
        'OR H T',
        'AND T J',
        'RUN'
    ]) + '\n'
    droid.run()
    print(f'Part 2: {droid.result}')

    '''
    That's the right answer! You are one gold star closer to rescuing Santa. 
    You got rank 585 on this star's leaderboard.
    '''

    '''
    Part 1: 19359969
    Part 2: 1140082748
    '''
