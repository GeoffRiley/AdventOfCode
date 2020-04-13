def memory_reallocation(inp, part1=True):
    history = []
    count = 0
    while tuple(inp) not in history:
        history.append(tuple(inp))
        ptr = inp.index(max(inp))
        val, inp[ptr] = inp[ptr], 0
        while val > 0:
            ptr += 1
            if ptr >= len(inp):
                ptr = 0
            inp[ptr] += 1
            val -= 1
        count += 1
    if part1:
        return count
    else:
        return count - history.index(tuple(inp))


if __name__ == '__main__':
    with open('input.txt') as block_file:
        blocks = list(map(int, block_file.read().split()))
        print(f'Day 6, part 1: {memory_reallocation(blocks.copy())}')
        print(f'Day 6, part 2: {memory_reallocation(blocks, False)}')
        # Day 6, part 1: 12841
        # Day 6, part 2: 8038
