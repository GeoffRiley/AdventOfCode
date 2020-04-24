from itertools import permutations


def scrambled_letters_and_hash(inp, pwd):
    if not isinstance(pwd, list):
        pwd = list(pwd)
    for inst in inp:
        parts = inst.split()
        nums = [int(a) for a in parts if a.isdigit()]
        if parts[0] == 'swap':
            if parts[1] == 'position':
                x, y = nums[0], nums[1]
            # elif parts[1] == 'letter':
            else:
                x, y = pwd.index(parts[2]), pwd.index(parts[5])
            pwd[x], pwd[y] = pwd[y], pwd[x]
        elif parts[0] == 'rotate':
            if parts[1] == 'based':
                ch = parts[-1]
                c = pwd.index(ch)
                c += (c >= 4) + 1
                c = -(c % len(pwd))
            else:
                c = nums[0]
                if parts[1] == 'right':
                    c = -c
                # elif parts[1] == 'left':
                #     pass
            pwd = pwd[c:] + pwd[:c]
        elif parts[0] == 'reverse':
            x, y = nums[0], nums[1]
            pwd[x:y + 1] = pwd[x:y + 1][::-1]
        elif parts[0] == 'move':
            x, y = nums[0], nums[1]
            c = pwd.pop(x)
            pwd = pwd[:y] + [c] + pwd[y:]
        else:
            print(f'Unrecognised instruction {inst}')
    return ''.join(pwd)


def scrambled_letters_and_hash_find(inst, target):
    pwd = list(target)
    for test in permutations(pwd):
        if scrambled_letters_and_hash(inst, test) == target:
            return ''.join(test)


if __name__ == '__main__':
    with open('input.txt') as instructions_file:
        instructions_list = instructions_file.read().splitlines(keepends=False)
        print(f'Day 21, part 1: {scrambled_letters_and_hash(instructions_list, "abcdefgh")}')
        print(f'Day 21, part 1: {scrambled_letters_and_hash_find(instructions_list, "fbgdceah")}')
        # Day 21, part 1: gcedfahb
        # Day 21, part 1: hegbdcfa
