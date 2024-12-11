"""
Advent of code 2024
Day 11: Plutonian Pebbles
"""

from collections import defaultdict
from functools import lru_cache
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import extract_ints


@lru_cache(maxsize=0)
def transform_stone(stone: int) -> list[int]:
    """
    Rules for transforming

      - If the stone is engraved with the number 0, it is replaced by a
        stone engraved with the number 1.
      - If the stone is engraved with a number that has an even number
        of digits, it is replaced by two stones. The left half of the
        digits are engraved on the new left stone, and the right half
        of the digits are engraved on the new right stone. (The new
        numbers don't keep extra leading zeroes: 1000 would become
        stones 10 and 0.)
      - If none of the other rules apply, the stone is replaced by a
        new stone; the old stone's number multiplied by 2024 is
        engraved on the new stone.
    """
    stone_str = str(stone)
    if stone == 0:
        return [1]
    elif ((length := len(stone_str)) & 1) == 0:
        return [int(stone_str[: (length // 2)]), int(stone_str[(length // 2) :])]
    else:
        return [stone * 2024]


def transform_stones(stones: dict[int, int]) -> dict[int, int]:
    """
    Transforms a collection of stones by applying a transformation to each stone type. 
    This function maps the original stones to new stone configurations while preserving their respective counts.

    Args:
        stones (dict[int, int]): A dictionary where keys are stone types and values are their quantities.

    Returns:
        dict[int, int]: A new dictionary with transformed stone types and their updated quantities.
    """
    new_stones = defaultdict(int)
    for stone, count in stones.items():
        tx_stones = transform_stone(stone)
        for new_stone in tx_stones:
            new_stones[new_stone] += count

    return new_stones


def repeated_transformations(stones: list[int], blinks: int) -> int:
    """
    Applies a series of transformations to a collection of stones over a specified number of iterations. 
    The function tracks the stones' transformations and returns the total number of stones after the specified number of blinks.

    Args:
        stones (list[int]): A list of initial stone types.
        blinks (int): The number of transformation iterations to perform.

    Returns:
        int: The total number of stones after the specified transformations.
    """
    current_stones = defaultdict(int)
    for stone in stones:
        current_stones[stone] += 1
    for _ in range(blinks):
        current_stones = transform_stones(current_stones)

    return sum(current_stones.values())


def part1(stones: list[int]) -> int:
    return repeated_transformations(stones,25)


def part2(stones: list[int]) -> int:
    return repeated_transformations(stones,75)


def main():
    loader = LoaderLib(2024)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(11)
    else:
        input_text = dedent(
            """\
                125 17
            """
        ).strip("\n")
    values = extract_ints(input_text)

    loader.print_solution("setup", f"{len(values)=} ...")
    loader.print_solution(
        1,
        part1(
            values,
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
            values,
        ),
    )


if __name__ == "__main__":
    main()
    # --
    # --------------------------------------------------------------------------------
    # LAP -> 0.000540        |        0.000540 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : len(values)=8 ...
    # --------------------------------------------------------------------------------


    # --------------------------------------------------------------------------------
    # LAP -> 0.001155        |        0.001695 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 231278
    # --------------------------------------------------------------------------------


    # --------------------------------------------------------------------------------
    # LAP -> 0.049213        |        0.050908 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 2   : 274229228071551
    # --------------------------------------------------------------------------------

