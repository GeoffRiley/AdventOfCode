"""
Advent of code 2022
Day 02: Rock Paper Scissors
"""
from functools import lru_cache
from typing import List

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


@lru_cache()
def get_score(them: str, us: str) -> int:
    elem: dict[str, int] = {"X": 1, "Y": 2, "Z": 3}
    wins: dict[str, str] = {"X": "C", "Y": "A", "Z": "B"}
    draws: dict[str, str] = {"X": "A", "Y": "B", "Z": "C"}
    score = 0
    if wins[us] == them:
        score += 6
    elif draws[us] == them:
        score += 3
    score += elem[us]

    return score


def part1(lines: List[str]) -> int:
    """
    A = X = Rock
    B = Y = Paper
    C = Z = Scissors
    """
    # score = 0
    # for line in lines:
    #     them, us = line.split()
    #     score += get_score(them, us)

    score = sum(get_score(them, us) for them, us in (line.split() for line in lines))

    return score


@lru_cache()
def get_strategic(them: str, strategy: str) -> int:
    win_strategy: dict[str, str] = {"A": "Y", "B": "Z", "C": "X"}
    draw_strategy: dict[str, str] = {"A": "X", "B": "Y", "C": "Z"}
    lose_strategy: dict[str, str] = {"A": "Z", "B": "X", "C": "Y"}
    strategy_lookup = {"X": lose_strategy, "Y": draw_strategy, "Z": win_strategy}
    us = strategy_lookup[strategy][them]
    score = get_score(them, us)
    return score


def part2(lines: List[str]) -> int:
    """
    A = Rock
    B = Paper
    C = Scissors
    X = Lose
    Y = Draw
    Z = Win
    """
    # score = 0
    # for line in lines:
    #     them, strategy = line.split()
    #     score += get_strategic(them, strategy)

    score = sum(get_strategic(them, us) for them, us in (line.split() for line in lines))

    return score


def main():
    loader = LoaderLib(2022)
    input_text = loader.get_aoc_input(2)

    # input_text = dedent("""\
    #                 A Y
    #                 B X
    #                 C Z
    #                 """).strip('\n')

    lines = lines_to_list(input_text)

    loader.print_solution('setup', f'{len(lines)} ...')
    loader.print_solution(1, part1(lines))
    loader.print_solution(2, part2(lines))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.003323        |        0.003323 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 2500 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.002674        |        0.005997 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 8890
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.002564        |        0.008561 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 10238
    # --------------------------------------------------------------------------------
