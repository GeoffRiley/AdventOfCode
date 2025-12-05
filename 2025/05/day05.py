"""
Advent of code 2025
Day 05: Cafeteria
"""
from textwrap import dedent
from typing import Any, Generator

from aoc.loader import LoaderLib
from aoc.utility import (
    lines_to_list,
)


def part1(lines: tuple[list[tuple[int, int]], list[str]]) -> int:
    """ """
    ranges, ingredients_array = lines
    count = 0
    for ingredient in ingredients_array:
        for r in ranges:
            if r[0] <= int(ingredient) <= r[1]:
                count += 1
                break
    return count


def part2(sorted_ranges: list[tuple[int, int]]) -> int:
    """ """
    return sum(e - s for s, e in sorted_ranges)


def sort_and_merge_ranges(ranges_array: list[str]) -> list[
    tuple[Any, Any]]:
    ranges: list[tuple[int, int]] = []
    for line in ranges_array:
        s, e = line.split('-')
        ranges.append((int(s), int(e) + 1))
    return list(merge_ranges(ranges))


def merge_ranges(ranges: list[tuple[int, int]]) -> Generator[tuple[Any, Any], Any, None]:
    """Merge overlapping and adjacent ranges and yield the merged ranges in order."""
    ranges = iter(sorted(ranges))
    current_start, current_stop = next(ranges)
    for start, stop in ranges:
        if start > current_stop:
            # Gap between segments: output current segment and start a new one.
            yield current_start, current_stop
            current_start, current_stop = start, stop
        else:
            # Segments adjacent or overlapping: merge.
            current_stop = max(current_stop, stop)
    yield current_start, current_stop


def main():
    loader = LoaderLib(2025)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(5)
    else:
        input_text = dedent(
            """\
                3-5
                10-14
                16-20
                12-18
                
                1
                5
                8
                11
                17
                32
            """
        ).strip("\n")
    # lines = [
    #     (extract_ints(param)) for param in [line for line in lines_to_list(input_text)]
    # ]
    lines = [lines_to_list(line) for line in input_text.split("\n\n")]
    # lines = lines_to_list(input_text)

    ranges_array, ingredients_array = lines
    sorted_ranges = sort_and_merge_ranges(ranges_array)

    # loader.print_solution("setup", f"{len(lines)=} ...")
    loader.print_solution("setup", f"{len(sorted_ranges)=}, {len(ingredients_array)=}")
    loader.print_solution(
        1,
        part1(
            (sorted_ranges, ingredients_array),
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
            sorted_ranges,
        ),
    )


if __name__ == "__main__":
    main()
    # --
    # -
    # --------------------------------------------------------------------------------
    #  LAP -> 0.000539        |        0.000539 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : len(sorted_ranges)=79, len(ingredients_array)=1000
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.009942        |        0.010481 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 511
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.000054        |        0.010535 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 350939902751909
    # --------------------------------------------------------------------------------
