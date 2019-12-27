from functools import reduce
from itertools import combinations
from operator import mul


def pack_the_boxes(boxes: list, divs=3):
    target = sum(boxes) // divs
    load = len(boxes) // divs
    possibles = set()
    for r in range(1, load + 1):
        for c in combinations(boxes, r):
            if sum(c) == target:
                possibles.add(reduce(mul, c))
        if len(possibles) > 0:
            break

    return min(possibles)


if __name__ == '__main__':
    with open('input') as f:
        box_list = [int(v) for v in f.read().splitlines(keepends=False)]
    print(f'Part 1: {pack_the_boxes(box_list)}')
    print(f'Part 2: {pack_the_boxes(box_list, 4)}')
    # Part 1: 10723906903
    # Part 2: 74850409
