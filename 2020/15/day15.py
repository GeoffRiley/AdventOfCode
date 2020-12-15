from collections import defaultdict
from typing import List


def rambunctious_recitation_part(data: str, terminal: int = 2020) -> int:
    start_values: List[int] = list(map(int, data.split(',')))

    reminder = defaultdict(int)
    for time_index, current_value in enumerate(start_values[:-1]):
        reminder[current_value] = time_index + 1

    next_value = start_values[-1]

    for time_index in range(len(start_values), terminal):
        current_value = next_value
        next_value = reminder[current_value]
        next_value = 0 if next_value == 0 else time_index - next_value
        reminder[current_value] = time_index

    return next_value


if __name__ == '__main__':
    # List of tests and expected results
    # they take a long time, so don't do them all at once!
    test_text = [
        ["0,3,6", 436, 175594],
        # ["1,3,2", 1, 2578],
        # ["2,1,3", 10, 3544142],
        # ["1,2,3", 27, 261214],
        # ["2,3,1", 78, 6895259],
        # ["3,2,1", 438, 18],
        # ["3,1,2", 1836, 362],
    ]
    for t, r, _ in test_text:
        assert rambunctious_recitation_part(t) == r
    for t, _, r in test_text:
        assert rambunctious_recitation_part(t, 30000000) == r

    in_text = "0,1,4,13,15,12,16"
    part1 = rambunctious_recitation_part(in_text)
    print(f'Part1: {part1}')
    part2 = rambunctious_recitation_part(in_text, 30000000)
    print(f'Part2: {part2}')

    # Part1: 1665
    # Part2: 16439
