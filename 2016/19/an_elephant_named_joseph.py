from collections import deque


def an_elephant_named_joseph(inp, part1=True):
    elves = deque(range(1, inp + 1))
    elves2 = deque()
    if part1:
        while len(elves) > 1:
            elves.rotate(-1)
            elves.popleft()
    else:
        elf_c = inp
        while len(elves) > len(elves2):
            elves2.append(elves.pop())
        while elf_c > 1:
            elves2.pop()
            elves2.appendleft(elves.popleft())
            if len(elves2) - len(elves) > 1:
                elves.append(elves2.pop())
            elf_c -= 1
    return elves[0] if part1 else elves2[0]


if __name__ == '__main__':
    elf_count = 3_004_953
    print(f'Day 19, part 1: {an_elephant_named_joseph(elf_count)}')
    print(f'Day 19, part 2: {an_elephant_named_joseph(elf_count, False)}')
    # Day 19, part 1: 1815603
    # Day 19, part 2: 1410630
