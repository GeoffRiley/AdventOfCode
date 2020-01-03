from intcode.intcode import Intcode


class ExploreDroid(object):
    def __init__(self, mem_code):
        self._processor = Intcode(mem_code)
        self._cmd_buffer = ''
        self.exploration_commands = []

    def _receiver(self, output, trace):
        if 0 < output < 128:
            c = chr(output)
            if output == 10:
                print(self._cmd_buffer)
                self._cmd_buffer = ''
            else:
                self._cmd_buffer += c
                if self._cmd_buffer == 'Command?':
                    if len(self.exploration_commands) > 0:
                        cmd = self.exploration_commands.pop(0)
                    else:
                        cmd = input('cmd?')
                    self._processor.receiver(cmd)
                    self._processor.receiver(10)

    def run(self):
        self._processor.connect(self._receiver)
        self._processor.simulate()


if __name__ == '__main__':
    with open('input') as f:
        mem_dump = f.read()

    droid = ExploreDroid(mem_dump)

    droid.exploration_commands = [
        'south',
        'south',
        'south',
        'take fixed point',
        'south',
        'take festive hat',
        'west',
        'west',
        'take jam',
        'south',
        'take easter egg',
        'north',
        'east',
        'east',
        'north',
        'west',
        'take asterisk',
        'east',
        'north',
        'west',
        'north',
        'north',
        'take tambourine',
        'south',
        'south',
        'east',
        'north',
        'west',
        'south',
        'take antenna',
        'north',
        'west',
        'west',
        'take space heater',
        'west',

        'drop jam',
        'drop festive hat',
        'drop asterisk',
        'drop antenna',
        # 'drop easter egg',
        # 'drop space heater',
        # 'drop tambourine',
        # 'drop fixed point',
        'west'
        # A loud, robotic voice says "Analysis complete! You may proceed." and you enter the cockpit.
        # Santa notices your small droid, looks puzzled for a moment,
        # realizes what has happened, and radios your ship directly.
        # "Oh, hello! You should be able to get in by typing 2147485856 on the keypad at the main airlock."
    ]

    droid.run()
    # Result: 2147485856
