"""
Advent of code 2025
Day 03: Lobby
"""

from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


def part1(lines: list[str]) -> int:
    """ """
    max_joltage = 0
    for line in lines:
        m, p = pick_best(line)
        n = max(list(line[p:]))
        max_joltage += int(''.join([m, n]))
    return max_joltage


def pick_best(choices: str, seek_from: int = 0, remaining_choices: int = 1) -> tuple[str, int]:
    best_choice = max(list(choices[seek_from:-remaining_choices]))
    best_choice_position = choices.index(best_choice, seek_from) + 1
    return best_choice, best_choice_position


def part2(lines: list[str]) -> int:
    """ """
    max_joltage = 0
    for line in lines:
        elements = []
        p = 0
        for i in range(11, 0, -1):
            m, p = pick_best(line, p, i)
            elements.append(m)
        n = max(list(line[p:]))
        max_joltage += int(''.join(elements + [n]))
    return max_joltage


def main():
    loader = LoaderLib(2025)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(3)
    else:
        input_text = dedent(
            """\
                987654321111111
                811111111111119
                234234234234278
                818181911112111
            """
        ).strip("\n")
    # lines = [(extract_ints(param)) for param in list(lines_to_list(input_text))]
    # lines = [lines_to_list(line) for line in input_text.split("\n\n")]
    lines = lines_to_list(input_text)
    # lines = input_text.split(',')

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
    #
