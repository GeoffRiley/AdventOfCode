# I must have struggled: there are comments!!
from collections import deque
from itertools import chain
from typing import List, Set, Tuple, Union


class Node:
    def __init__(self, cup: int):
        self.cup: int = cup
        self.next: Union['Node', None] = None

    def __repr__(self):
        return f'{self.cup}→{self.next.cup or "¤"}'


def crab_cups_part1(data: str) -> str:
    # This deque form was fine for part 1, but FAR too slow
    # for part 2!!
    cups = deque(int(c) for c in data.strip())
    for _ in range(100):
        current_cup = cups[0]
        # step 1: remove 3 cups
        cups.rotate(-1)
        temp_cups = [cups.popleft() for _ in range(3)]
        # step 2: select new 'destination cup'
        # subtract 1
        destination_cup = current_cup - 1
        while destination_cup not in cups:
            destination_cup -= 1
            if destination_cup < 0:
                destination_cup = max(cups)
        # get the new current cup to the top
        while cups[0] != destination_cup:
            cups.rotate()
        # insert the removed cups
        cups.rotate(-1)
        cups.extend(temp_cups)
        # get the 'current cup' to the end of the deque
        while cups[-1] != current_cup:
            cups.rotate()

    while cups[0] != 1:
        cups.rotate()
    cups.popleft()
    return ''.join(str(x) for x in list(cups))


def dec_cup(cup: int, rng: Tuple[int, int]) -> int:
    cup -= 1
    if cup < rng[0]:
        cup = rng[1]
    return cup


def cup_order(first_cup: int, node_list: List[Node]) -> List[int]:
    o = []
    cup = first_cup
    while node_list[cup].next.cup != first_cup:
        o.append(cup)
        cup = node_list[cup].next.cup
    o.append(cup)
    return o


def crab_cups_part2(data: str, cup_max: int = None, loops: int = 100) -> Union[int, List[int]]:
    start_array = [int(c) for c in data.strip()]
    if cup_max:
        link_range = (1, cup_max)
    else:
        link_range = (1, max(start_array))
    # Big list of 'Node's, they'll be chained together
    # in the appropriate order dictated by 'data'
    node_list: List[Node] = [Node(n) for n in range(link_range[1] + 1)]
    # Link the nodes from 'data' first, coming in from the end
    # and then link the remaining nodes in order
    # ** index 0 unused except to hold the final loopback
    link_from: int = 0
    # for n in chain(map(int, [c for c in data.strip()]), range(len(data)+1, link_range[1]+1)):
    for n in chain(start_array, range(len(start_array) + 1, link_range[1] + 1)):
        node_list[link_from].next = node_list[n]
        link_from = n
    # get the loopback to complete the circle
    node_list[link_from].next = node_list[0].next
    node_list[0].next = None

    # keep a history of the last 50 moves
    history = deque(maxlen=50)
    # Identify the 'current cup' at the start
    current_cup: int = int(data[0])
    # for a in node_list[1:]:
    #     assert a.next is not None
    # Now to run the rules… a lot
    for _ in range(loops):
        # 1 remove next three cups
        temp_cup1: Node = node_list[current_cup].next
        temp_cup2: Node = temp_cup1.next
        temp_cup3: Node = temp_cup2.next
        temp_cups: Set[int] = {temp_cup1.cup, temp_cup2.cup, temp_cup3.cup}
        # unlink those cups
        node_list[current_cup].next = temp_cup3.next
        temp_cup3.next = None
        # 2 select the destination cup, making sure to not select
        # one that has been removed, or disappear off the bottom!
        destination_cup: int = dec_cup(current_cup, link_range)
        while destination_cup in temp_cups:
            destination_cup = dec_cup(destination_cup, link_range)

        # history.append({'curr': current_cup, 'dest': destination_cup, 'temps': temp_cups})

        # A couple of sanity checks
        # if not(link_range[0] <= destination_cup <= link_range[1]):
        #     raise ValueError(f'Destination cup out of range: {destination_cup}')
        # if node_list[destination_cup].next is None:
        #     raise ValueError(f'destination cup broken list: {destination_cup}')

        dest_node = node_list[destination_cup]
        # 3 reinsert the removed cups
        # We had: … temp_cup1.next → temp_cup2.next → temp_cup3.next → None
        # and: … dest_node.next → 'following cups'
        # We want:
        # … dest_node.next → temp_cup1.next → temp_cup2.next → temp_cup3.next → 'following cups'
        # So, what was in dest_node.next is put as the temp_cup3.next
        # and dest_node.next is reassigned with temp_cup1
        temp_cup3.next = dest_node.next
        dest_node.next = temp_cup1

        # 4 move the 'current cup' onward to the next cup
        current_cup = node_list[current_cup].next.cup

    if cup_max:

        star_cup1 = node_list[1].next.cup
        star_cup2 = node_list[star_cup1].next.cup
        return star_cup1 * star_cup2

    else:

        return int(''.join(str(n) for n in cup_order(1, node_list)[1:]))


if __name__ == '__main__':
    test_text = '389125467'
    assert crab_cups_part1(test_text) == '67384529'
    assert crab_cups_part2(test_text) == 67384529
    assert crab_cups_part2(test_text, 1_000_000, 10_000_000) == 149245887792

    # with open('input.txt') as in_file:
    in_text = '469217538'
    part1 = crab_cups_part1(in_text)
    print(f'Part1: {part1}')
    part2 = crab_cups_part2(in_text, 1_000_000, 10_000_000)
    print(f'Part2: {part2}')

    # Part1: 27956483
    # Part2: 18930983775
