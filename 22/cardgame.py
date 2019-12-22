def cardgame(deck: list, instr: str) -> list:
    # brute force… perform the actions on a representation of the deck
    for line in instr.splitlines(keepends=False):
        cmd = line.split()
        if cmd[0] == 'deal':
            if line == 'deal into new stack':
                deck = deck[::-1]
            elif cmd[1] + cmd[2] == 'withincrement':
                incr = int(cmd[3])
                tmp = deck.copy()
                deck = [-1 for _ in range(len(deck))]
                pos = 0
                for n in tmp:
                    deck[pos] = n
                    pos = (pos + incr) % (len(deck))
                try:
                    if deck.index(-1) >= 0:
                        raise TypeError('Deal with increment failed')
                except ValueError:
                    pass
            else:
                raise ValueError(f'Unrecognised deal command: {line}')
        elif cmd[0] == 'cut':
            pos = int(cmd[1])
            if pos >= 0:
                deck = deck[pos:] + deck[:pos]
            else:
                deck = deck[pos:] + deck[:pos]
        else:
            raise ValueError(f'Unrecognised command: {line}')
    return deck


def modpow(b, e, m):
    if e == 0:
        return 1
    elif e % 2 == 0:
        return modpow((b * b) % m, e / 2, m)
    else:
        return (b * modpow(b, e - 1, m)) % m


def modinv(a, m):
    return modpow(a, m - 2, m)


def cardgame2(deck_size: int, repeat: int, target: int, instr: str) -> list:
    # work backwards from target keeping track of transformations
    a, b = 1, 0
    for line in reversed(instr.splitlines(keepends=False)):
        cmd = line.split()
        if cmd[0] == 'deal':
            if line == 'deal into new stack':
                a, b = -a, deck_size - 1 - b
            elif cmd[1] + cmd[2] == 'withincrement':
                incr = int(cmd[3])
                inc_inv = modinv(incr, deck_size)
                a, b = a * inc_inv, b * inc_inv
            else:
                raise ValueError(f'Unrecognised deal command: {line}')
        elif cmd[0] == 'cut':
            cut_pos = int(cmd[1])
            if cut_pos < 0:
                cut_pos = deck_size + cut_pos
            a, b = a, b + cut_pos
        else:
            raise ValueError(f'Unrecognised command: {line}')
    a, b = a % deck_size, b % deck_size
    ans = (target *
           modpow(a, repeat, deck_size) +
           (modpow(a, repeat, deck_size) - 1) * b *
           modinv(a - 1, deck_size)) % deck_size
    return ans


if __name__ == '__main__':
    with open('input') as f:
        script = f.read()
    deck = [n for n in range(10007)]
    res = cardgame(deck, script)
    print(f'Part 1: {res.index(2019)}')
    '''
    Part 1: 4284
    That's the right answer! You are one gold star closer to rescuing Santa. 
    You got rank 738 on this star's leaderboard. [Continue to Part Two]
    '''
    deck_size = 119315717514047
    rep = 101741582076661
    res = cardgame2(deck_size, rep, 2020, script)
    print(f'Part 2: {res}')
    '''
    Part 2: 96797432275571
    That's the right answer! You are one gold star closer to rescuing Santa. 
    You got rank 702 on this star's leaderboard.
    '''
