"""
Advent of code 2021
Day 7: The Treachery of Whales
"""
from collections import Counter
from functools import lru_cache
from statistics import median, mean
from typing import List

from aoc.loader import LoaderLib
from aoc.utility import to_list_int


def part1(positions: List[int]):
    """Hypothesis: the appropriate position for the crabs to line up
        is at the median of all the values.  This was bourne out by
        the test data and correctly identified the answer for the full
        puzzle set.  It is still possible that this is a coincidence!
    """
    pos_counts = Counter(positions)
    guess = int(median(positions))

    fuel = sum(abs(n - guess) * q for n, q in pos_counts.items())
    return f'{fuel} around {guess}'
    # 354129 around 361


@lru_cache(maxsize=None)
def fuel_calc(move: int) -> int:
    """Fuel is expensive for crab submarines, it increases with
        every move… in a triangular number kind of way.
    """
    move = abs(move)
    return move * (move + 1) // 2


def part2(positions: List[int]):
    """Hypothesis: the appropriate position for the crabs this time will be
        around the mean average of all their current positions.
        This did not appear to be safe: although the rounded value for the
        test data was correct, it did not appear to give a correct reading
        for the full data.  Instead, I opted for performing a binary search
        to locate the correct value.
        Intriguingly the eventual result turned out to be the mean value
        rounded down!!
    """
    pos_counts = Counter(positions)
    guess_mean = mean(positions)
    mean_fuel = sum(fuel_calc(n - guess_mean) * q for n, q in pos_counts.items())

    guess_min = min(positions)
    guess_max = max(positions)
    done = False
    while not done:
        rng = guess_max - guess_min

        guess = rng // 2 + guess_min

        fuel = sum(fuel_calc(n - guess) * q for n, q in pos_counts.items())
        fuel_d = sum(fuel_calc(n - guess - 1) * q for n, q in pos_counts.items())
        fuel_u = sum(fuel_calc(n - guess + 1) * q for n, q in pos_counts.items())
        if fuel_d > fuel < fuel_u:
            done = True
            break
        elif fuel_d < fuel < fuel_u:
            guess_min = guess
            continue
        elif fuel_d > fuel > fuel_u:
            guess_max = guess
            continue
        else:
            raise ValueError('I got stuck')

    return f'{fuel} around {guess} (Original guess: {mean_fuel} around {guess_mean})'
    # 98905973 around 494


def main():
    loader = LoaderLib(2021)
    input_text = loader.get_aoc_input(7)
    # input_text = "16,1,2,0,4,2,7,1,2,14"

    positions = to_list_int(input_text)

    # assert len(lines) == len(...)
    loader.print_solution('setup', f'{len(positions)} ...')
    loader.print_solution(1, part1(positions))
    loader.print_solution(2, part2(positions))
    print(fuel_calc.cache_info())


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.003316        |        0.003316 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 1000 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.001383        |        0.004699 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 354129 around 361
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.023467        |        0.028167 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 98905973 around 494 (Original guess: 98905337.0 around 494.601)
    # --------------------------------------------------------------------------------
    #
    # CacheInfo(hits=19506, misses=2968, maxsize=None, currsize=2968)
