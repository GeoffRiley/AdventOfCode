from collections import defaultdict
from typing import List, Tuple


def electromagnetic_moat(inp):
    bricks = defaultdict(set)
    components = set()
    for a, b in [tuple(map(int, line.split('/'))) for line in inp]:
        # Hint... map both directions!!
        bricks[a].add(b)
        bricks[b].add(a)
        components.add((a, b) if a < b else (b, a))
    bridges = dict()
    stack = [(0, list(), 0)]
    while len(stack) > 0:
        next_val: int
        bridge: List[Tuple[int, int]]
        bridge_val: int
        next_val, bridge, bridge_val = stack.pop()
        for b in bricks[next_val]:
            brick = (next_val, b) if next_val < b else (b, next_val)
            if brick not in bridge:
                new_bridge = bridge.copy()
                new_bridge.append(brick)
                new_bridge_val = bridge_val + next_val + b
                stack.append((b, new_bridge, new_bridge_val))
                if tuple(new_bridge) not in bridges:
                    bridges[tuple(new_bridge)] = new_bridge_val
    return max(bridges.items(), key=lambda x: x[1]), max(bridges.items(), key=lambda x: (len(x[0]), x[1]))


if __name__ == '__main__':
    with open('input.txt') as moat_file:
        moat_text = moat_file.read().splitlines(keepends=False)
        bridge_values = electromagnetic_moat(moat_text)
        print(f'Day 24, part 1: {bridge_values[0][1]}')
        print(f'Day 24, part 2: {bridge_values[1][1]}')
        # Day 24, part 1: 1906
        # Day 24, part 2: 1824
