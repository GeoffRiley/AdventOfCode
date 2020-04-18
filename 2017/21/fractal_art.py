import numpy as np


def fractal_art(inp, iterations):
    rules = parse_rules(inp)
    current_state = np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]], dtype=np.int8)
    for n in range(iterations):
        size = len(current_state)
        if size % 2 == 0:
            f, t = 2, 3
        elif size % 3 == 0:
            f, t = 3, 4
        else:
            print(f'Size error: {size}')
            break
        steps = size // f
        next_state = np.zeros((t * steps, t * steps), dtype=np.int8)
        for row in range(steps):
            for col in range(steps):
                orig = current_state[f * row:f * row + f, f * col:f * col + f].copy()
                new = rules[orig.flatten().tobytes()]
                next_state[t * row:t * row + t, t * col:t * col + t] = new.copy()
        current_state = next_state
    return sum(current_state.flatten())


def parse_rules(inp):
    rules = dict()
    for line in inp:
        original, replacement = line.split(' => ')
        original = np.array([0 if x == '.' else 1 for x in original if x in '.#'], dtype=np.int8)
        replacement = np.array([0 if x == '.' else 1 for x in replacement if x in '.#'], dtype=np.int8)
        if len(original) == 4:
            rules.update(monkey_about(original.reshape((2, 2)), replacement.reshape((3, 3))))
        elif len(original) == 9:
            rules.update(monkey_about(original.reshape((3, 3)), replacement.reshape((4, 4))))
        else:
            print(f'Do not understand {line}')
    return rules


def monkey_about(a, b):
    rules = dict()
    for n in range(4):
        rot_a = np.rot90(a, k=n)
        rules[rot_a.flatten().tobytes()] = b
        rules[np.fliplr(rot_a).flatten().tobytes()] = b
        rules[np.flipud(rot_a).flatten().tobytes()] = b
    return rules


if __name__ == '__main__':
    with open('input.txt') as rule_file:
        rule_list = rule_file.read().splitlines(keepends=False)
        print(f'Day 21, part 1: {fractal_art(rule_list, 5)}')
        print(f'Day 21, part 2: {fractal_art(rule_list, 18)}')
        # Day 21, part 1: 164
        # Day 21, part 2: 2355110
