"""
Advent of code 2023
Day 12: Hot Springs
"""
from collections import defaultdict
import re
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list, to_list_int


def get_positions(springs: str, group: int) -> list[tuple[int, int]]:
    pattern = f"(?<!#)(?=[?#]{{{group}}}(?!#))"
    return [(m.start(), m.start() + group) for m in re.finditer(pattern, springs)]


next_disabled = re.compile("#")


def get_next_disabled(springs: str, search_start: int) -> int:
    if match := next_disabled.search(springs, search_start):
        return match.start()
    return len(springs)


def count_possibilities(springs: str, groups: list[int]) -> int:
    counts = {(-1, -1): 1}
    for group in groups:
        new_counts = defaultdict(int)
        positions = get_positions(springs, group)
        for (prev_start, prev_end), count in counts.items():
            next_disabled = get_next_disabled(springs, prev_end + 1)
            for curr_start, curr_end in positions:
                if curr_start <= prev_end:
                    continue
                if curr_start > next_disabled:
                    break
                new_counts[curr_start, curr_end] += count
        counts = new_counts
    return sum(count for (_, end), count in counts.items() if "#" not in springs[end:])


def part1(lines: list[tuple[str, list[int]]]) -> int:
    """
    We're going to group the springs into possible groups and then see how many
    ways we can arrange them to fit the given map.
    """
    arrangements = 0
    for pat, param in lines:
        arr = count_possibilities(pat, param)
        # print(pat, param, arr)
        arrangements += arr
    return arrangements


def part2(lines) -> int:
    """
    Now we 'unfold' the lists and count the possibilities.
    """
    arrangements = 0
    for pat, param in lines:
        pat = "?".join(pat for _ in range(5))
        param *= 5
        arr = count_possibilities(pat, param)
        # print(pat, param, arr)
        arrangements += arr
    return arrangements


def main():
    loader = LoaderLib(2023)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(12)
    else:
        input_text = dedent(
            """\
            ???.### 1,1,3
            .??..??...?##. 1,1,3
            ?#?#?#?#?#?#?#? 1,3,1,6
            ????.#...#... 4,1,1
            ????.######..#####. 1,6,5
            ?###???????? 3,2,1
            """
        ).strip("\n")
    lines = [
        (pat, to_list_int(param))
        for pat, param in [line.split() for line in lines_to_list(input_text)]
    ]

    loader.print_solution("setup", f"{len(lines)=} ...")
    loader.print_solution(
        1,
        part1(
            lines,
        ),
    )
    # if testing:
    #     input_text = dedent(
    #         """\
    #         """
    #     ).strip("\n")
    #     lines = lines_to_list(input_text)
    loader.print_solution(
        2,
        part2(
            lines,
        ),
    )


if __name__ == "__main__":
    main()
    # --
    # --------------------------------------------------------------------------------
    # LAP -> 0.000876        |        0.000876 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : len(lines)=1000 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    # LAP -> 0.023905        |        0.024781 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 7173
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    # LAP -> 0.427124        |        0.451905 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 2   : 29826669191291
    # --------------------------------------------------------------------------------
