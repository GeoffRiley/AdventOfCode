import itertools


def how_many_ways(qty, containers, only_min=False) -> int:
    count = 0
    found_min = 1e30
    for s in itertools.chain.from_iterable(itertools.combinations(containers, r + 1) for r in range(len(containers))):
        if len(s) <= found_min:
            if sum(s) == qty:
                if only_min and len(s) < found_min:
                    count = 0
                    found_min = len(s)
                count += 1
    return count


if __name__ == '__main__':
    with open('input') as f:
        con_list = [int(v) for v in f.read().splitlines(keepends=False)]

    print(f'Part 1: {how_many_ways(150, con_list)}')
    print(f'Part 2: {how_many_ways(150, con_list, only_min=True)}')
