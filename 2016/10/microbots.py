from collections import defaultdict


def microbots(instructions: str, val_a: int, val_b: int, part2=True) -> int:
    bots = defaultdict(list)
    outputs = defaultdict(list)
    target = {val_a, val_b}
    target_bot = -1
    # Check value prompts first to load the bases
    for line in instructions.splitlines(keepends=False):
        if line.startswith('value '):
            parts = line.split()
            b = int(parts[-1])
            v = int(parts[1])
            bots[b].append(v)

    # Now go through for the bot prompts repeatedly
    changed = True
    while changed:
        changed = False
        for line in instructions.splitlines(keepends=False):
            if line.startswith('bot '):
                parts = line.split()
                b = int(parts[1])
                if len(bots[b]) == 2:
                    l_dest, l_num = parts[5:7]
                    h_dest, h_num = parts[-2:]
                    for dest, num, op in [(l_dest, int(l_num), min), (h_dest, int(h_num), max)]:
                        if dest == 'bot':
                            bots[num].append(op(bots[b]))
                        else:
                            outputs[num].append(op(bots[b]))
                    bots[b] = []
                    changed = True
            for k, bot in bots.items():
                if set(bot) == target:
                    target_bot = k
    if part2:
        print(f'Part 2: {outputs[0][0] * outputs[1][0] * outputs[2][0]}')
    return target_bot


if __name__ == '__main__':
    with open('input') as f:
        insts = f.read()
    print(f'Part 1: {microbots(insts, val_a=17, val_b=61)}')
    # Part 1: 113
    # Part 2: 12803
