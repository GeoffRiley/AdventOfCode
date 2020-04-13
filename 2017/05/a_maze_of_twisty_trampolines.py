def a_maze_of_twisty_trampolines(inp, part1=True):
    ptr = 0
    count = 0
    jumps = list(map(int, inp))
    while 0 <= ptr < len(jumps):
        nxt = ptr + jumps[ptr]
        if part1:
            jumps[ptr] += 1
        else:
            jumps[ptr] += 1 if jumps[ptr] < 3 else -1
        ptr = nxt
        count += 1
    return count


if __name__ == '__main__':
    with open('input.txt') as maze_file:
        maze = maze_file.read().splitlines(keepends=False)
        print(f'Day 5, part 1: {a_maze_of_twisty_trampolines(maze)}')
        print(f'Day 5, part 2: {a_maze_of_twisty_trampolines(maze, False)}')
        # Day 5, part 1: 391540
        # Day 5, part 2: 30513679
