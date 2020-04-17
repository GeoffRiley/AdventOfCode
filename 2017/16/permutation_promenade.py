from collections import deque


def permutation_promenade(inp, pass1=True):
    history = []
    progs = deque([chr(97 + c) for c in range(16)])
    history.append(''.join(progs))
    res = ''
    if pass1:
        res = dance(inp, progs)
    else:
        repeat_range = 1_000_000_000
        for c in range(repeat_range):
            res = dance(inp, progs)
            if res in history:
                res = history[repeat_range % (c + 1)]
                break
            history.append(res)
    return res


def dance(inp, progs):
    for move in inp:
        ins, params = move[0], move[1:].split('/')
        if ins == 's':
            progs.rotate(int(params[0]))
        if ins == 'x':
            x, y = list(map(int, params))
            progs[x], progs[y] = progs[y], progs[x]
        if ins == 'p':
            x = progs.index(params[0])
            y = progs.index(params[1])
            progs[x], progs[y] = progs[y], progs[x]
    return ''.join(progs)


if __name__ == '__main__':
    with open('input.txt') as dance_file:
        dance_moves = dance_file.read().strip().split(',')
        print(f'Day 16, part 1: {permutation_promenade(dance_moves)}')
        print(f'Day 16, part 2: {permutation_promenade(dance_moves, False)}')
        # Day 16, part 1: hmefajngplkidocb
        # Day 16, part 2: fbidepghmjklcnoa
