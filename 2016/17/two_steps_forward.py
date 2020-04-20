from hashlib import md5

MOVES = {
    'U': -1j,
    'D': 1j,
    'L': -1,
    'R': 1
}


def two_steps_forward(inp, part1=True):
    stack = [(0j, '')]
    max_len = 0
    while len(stack) > 0:
        pos, path = stack.pop()
        digest = md5((inp + path).encode()).hexdigest()[:4]
        for d, f in zip(MOVES.keys(), [n > 'a' for n in digest]):
            if f:
                new_pos = pos + MOVES[d]
                if new_pos == 3 + 3j:
                    if part1:
                        return path + d
                    else:
                        max_len = max(max_len, len(path + d))
                        continue
                if 0 <= new_pos.real <= 3 and 0 <= new_pos.imag <= 3:
                    stack.insert(0, (new_pos, path + d))
    return max_len


if __name__ == '__main__':
    puzzle_input = 'mmsxrhfx'
    print(f'Day 17, part 1: {two_steps_forward(puzzle_input)}')
    print(f'Day 17, part 2: {two_steps_forward(puzzle_input, False)}')
    # Day 17, part 1: RLDUDRDDRR
    # Day 17, part 2: 590
