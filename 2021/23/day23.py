"""
Advent of code 2021
Day 23: Amphipod
I really need to take time to comment this up: it's rather nasty code… although it did prove very handy for
calculating part 2 which I would have had problems doing had I stuck to working on a paper solution at first!
"""
from functools import cache

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list

A, B, C, D = 'ABCD'
INF = float('inf')
MOVE_COSTS = {
    A: 1,
    B: 10,
    C: 100,
    D: 1000,
}
CORRIDOR_ENTRY = {
    1: 2,
    2: 4,
    3: 6,
    4: 8
}
SIDE_ROOMS = set(v for v in CORRIDOR_ENTRY.values())
TARGETS = dict(zip('ABCD', CORRIDOR_ENTRY.values()))


def find_a_path(initial_state, target_state):
    def move_into_room(state):
        for j, amphipod in enumerate(state[0]):
            if amphipod is None:
                continue
            room = ' ABCD'.index(amphipod)
            room_set = set(state[room])
            room_set.discard(None)

            if room_set and {amphipod} != room_set:
                continue

            if j < TARGETS[amphipod]:
                sl = slice(j + 1, TARGETS[amphipod] + 1)
            else:
                sl = slice(TARGETS[amphipod], j)

            for t in state[0][sl]:
                if t is not None:
                    break
            else:
                steps = abs(j - TARGETS[amphipod])
                mutable_state = list(map(list, state))
                mutable_state[0][j] = None
                room_list = mutable_state[room]
                for top_index, val in reversed(list(enumerate(room_list))):
                    if val is None:
                        break
                else:
                    top_index = 0
                assert room_list[top_index] is None
                room_list[top_index] = amphipod
                steps += 1 + top_index
                yield tuple(map(tuple, mutable_state)), steps * MOVE_COSTS[amphipod]

    def possible_moves(state):
        for i in range(1, 5):
            top_index = 0
            try:
                while state[i][top_index] is None:
                    top_index += 1
            except IndexError:
                continue
            mutable_state = list(map(list, state))
            amphipod = mutable_state[i][top_index]

            if TARGETS[amphipod] == (-1, 2, 4, 6, 8)[i] and all(
                    amphipod == other for other in state[i][top_index:]
            ):
                continue

            steps = top_index
            mutable_state[i][top_index] = None

            possible_locations = []
            for j in range(CORRIDOR_ENTRY[i]):
                if j not in SIDE_ROOMS:
                    possible_locations.append(j)
                if mutable_state[0][j] is not None:
                    possible_locations.clear()
            for j in range(CORRIDOR_ENTRY[i], 11):
                if mutable_state[0][j] is not None:
                    break
                if j not in SIDE_ROOMS:
                    possible_locations.append(j)
            semi_mut_state = list(map(tuple, mutable_state))
            corridor = state[0]
            for p in possible_locations:
                mutable_corridor = list(corridor)
                mutable_corridor[p] = amphipod
                semi_mut_state[0] = tuple(mutable_corridor)
                yield tuple(semi_mut_state), ((1 + steps + abs(p - CORRIDOR_ENTRY[i])) * MOVE_COSTS[amphipod])

        yield from move_into_room(state)

    @cache
    def steps_to_final(state):
        if state == target_state:
            return 0
        possible_costs = [INF]
        for new_state, cost in possible_moves(state):
            possible_costs.append(cost + steps_to_final(new_state))
        return min(possible_costs)

    return steps_to_final(initial_state)


def part1(initial_state):
    """Assuming the shape of the input, we need only scan for the amphipods in the side rooms
    """
    room_size = len(initial_state[1])
    target_state = (
        (None,) * 11,
        (A,) * room_size,
        (B,) * room_size,
        (C,) * room_size,
        (D,) * room_size
    )

    return find_a_path(initial_state, target_state)
    # 11536


def part2(initial_state):
    """
    """
    folded_page = (
        (D, D),
        (C, B),
        (B, A),
        (A, C)
    )

    state = (
                (None,) * 11,
            ) + tuple((a, b, c, d) for (a, d), (b, c) in zip(initial_state[1:], folded_page))

    room_size = len(state[1])
    target_state = (
        (None,) * 11,
        (A,) * room_size,
        (B,) * room_size,
        (C,) * room_size,
        (D,) * room_size
    )

    return find_a_path(state, target_state)
    # 55136


def main():
    loader = LoaderLib(2021)
    input_text = loader.get_aoc_input(23)

    #     input_text = """#############
    # #...........#
    # ###B#C#B#D###
    #   #A#D#C#A#
    #   #########"""

    lines = lines_to_list(input_text)
    assert lines[0] == '#' * 13
    assert lines[4].strip() == '#' * 9

    letters = [c for line in lines for c in line if c.isalpha()]
    rows = letters[:4], letters[4:]

    initial_state = (
                        (None,) * 11,
                    ) + tuple(zip(*rows))

    loader.print_solution('setup', f'{len(lines)} ...')
    loader.print_solution(1, part1(initial_state))
    loader.print_solution(2, part2(initial_state))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.002761        |        0.002761 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 5 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 7.439343        |        7.442104 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 11536
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 11.080146       |       18.522251 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 55136
    # --------------------------------------------------------------------------------
