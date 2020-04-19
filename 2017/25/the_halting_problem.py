from collections import defaultdict


class StateException(Exception):
    pass


class TuringTransition(object):
    def __init__(self, actions, state):
        self._target_actions = actions
        self._target_state = state

    def go(self):
        for action in self._target_actions:
            action()
        return self._target_state


class TuringMachine(object):
    def __init__(self):
        self._tape = defaultdict(lambda: 0)
        self._tape_pos = 0
        self._transitions = dict()
        self._state = None
        self._start_state = None

    def left(self):
        self._tape_pos -= 1

    def right(self):
        self._tape_pos += 1

    def write0(self):
        self.cell = 0

    def write1(self):
        self.cell = 1

    def start(self):
        self._state = self._start_state

    def step(self):
        if self._state is None:
            raise StateException('Turing machine not running')
        from_state = (self._state, self.cell)
        if from_state not in self._transitions:
            raise StateException(f'Current state {from_state} not expressed in transitions')
        self._state = self._transitions[from_state].go()

    def which_write(self, value):
        if value == 0:
            return self.write0
        elif value == 1:
            return self.write1
        else:
            raise StateException(f'Cannot function with writing value {value}')

    def which_direction(self, value):
        if value == 'left':
            return self.left
        elif value == 'right':
            return self.right
        else:
            raise StateException(f'Cannot move in a direction {value}')

    def add_state(self, state_name, state_test, state_write, state_cursor, next_state):
        self._transitions[(state_name, state_test)] = TuringTransition(
            (self.which_write(state_write), self.which_direction(state_cursor)),
            next_state
        )

    @property
    def cell(self):
        return self._tape[self._tape_pos]

    @cell.setter
    def cell(self, value):
        self._tape[self._tape_pos] = value

    @property
    def start_state(self):
        return self._start_state

    @start_state.setter
    def start_state(self, value):
        self._start_state = value

    @property
    def diagnostic_total(self):
        return sum(self._tape.values())


PREAMBLE = 0
STATE_NAME = 1
STATE_TEST = 2
WRITE_VALUE = 3
MOVE_CURSOR = 4
NEXT_STATE = 5
SECONDARY = 16

FileReadStates = {
    PREAMBLE: STATE_NAME,
    STATE_NAME: STATE_TEST,
    STATE_TEST: WRITE_VALUE,
    WRITE_VALUE: MOVE_CURSOR,
    MOVE_CURSOR: NEXT_STATE,
    NEXT_STATE: SECONDARY + STATE_TEST,
    SECONDARY + STATE_TEST: SECONDARY + WRITE_VALUE,
    SECONDARY + WRITE_VALUE: SECONDARY + MOVE_CURSOR,
    SECONDARY + MOVE_CURSOR: SECONDARY + NEXT_STATE,
    SECONDARY + NEXT_STATE: STATE_NAME
}


def the_halting_problem(inp):
    # A state machine to read the state machine description!
    t_machine = TuringMachine()
    diag_steps = 1
    state_name, state_test, state_write, state_cursor = None, None, None, None
    parse_s = PREAMBLE
    for line in inp:
        if len(line.strip()) == 0:
            continue
        parse_t = parse_s & ~SECONDARY
        line_s = line.strip().split()
        if parse_t == PREAMBLE:
            if line.startswith('Begin'):
                t_machine.start_state = line_s[-1].strip('.')
                continue
            if line.startswith('Perform'):
                diag_steps = int(line_s[-2])
        elif parse_t == STATE_NAME:
            state_name = line_s[-1].strip(':')
        elif parse_t == STATE_TEST:
            state_test = int(line_s[-1].strip(':'))
        elif parse_t == WRITE_VALUE:
            state_write = int(line_s[-1].strip('.'))
        elif parse_t == MOVE_CURSOR:
            state_cursor = line_s[-1].strip('.')
        elif parse_t == NEXT_STATE:
            t_machine.add_state(state_name, state_test, state_write, state_cursor, line_s[-1].strip('.'))
        parse_s = FileReadStates[parse_s]
    t_machine.start()
    for r in range(diag_steps):
        t_machine.step()
    return t_machine.diagnostic_total


if __name__ == '__main__':
    with open('input.txt') as turing_file:
        turing_description = turing_file.read().splitlines(keepends=False)
        print(f'Day 25, part 1: {the_halting_problem(turing_description)}')
        # Day 25, part 1: 2846
