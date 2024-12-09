"""
Advent of code 2024
Day 09: Disk Fragmenter
"""

from collections import Counter, OrderedDict
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import extract_ints, lines_to_list, to_list_int


def part1(input_text: str) -> int:
    """ """
    disc_layout = {}
    is_file = True
    file_id = 0
    current_pos = 0
    for ch in input_text:
        l = int(ch)
        if is_file:
            disc_layout.update(
                {j: file_id for j in range(current_pos, current_pos + l)}
            )
            file_id += 1
        is_file = not is_file
        current_pos += l

    keyset = set(disc_layout.keys())
    free_empty = set(range(max(keyset))) - keyset
    for fs in free_empty:
        if fs in disc_layout:
            print("Darn it's gone wrong")
            break
        src = max(disc_layout.keys())
        if fs < src:
            disc_layout[fs] = disc_layout.pop(src)

    total = 0
    # for i,x in enumerate(sorted(disc_layout.items(), key=lambda x:x[0])):
    for i, x in disc_layout.items():
        total += i * x

    return total


def part2(input_text: list[str]) -> int:
    """ """
    file_space = {}
    file_dir = {}
    free_space = {}
    is_file = True
    file_id = 0
    current_pos = 0
    for ch in input_text:
        l = int(ch)
        if is_file:
            file_space[current_pos] = (l, file_id)
            file_dir[file_id] = current_pos
            file_id += 1
        else:
            free_space[current_pos] = l
        is_file = not is_file
        current_pos += l

    # - Iterate over files in descending order of their ID.
    # - For each file, look for the earliest suitable free space block before
    #   its current position.
    # - If found, move the whole file into that space in one operation.
    # - After processing all files, compute the checksum using the update
    #   positions.

    raise NotImplementedError


def main():
    loader = LoaderLib(2024)
    testing = True
    if not testing:
        input_text = loader.get_aoc_input(9)
    else:
        input_text = dedent(
            """\
                2333133121414131402
            """
        ).strip("\n")
    # lines = [
    #     (extract_ints(param))
    #         for param in [line for line in lines_to_list(input_text)]
    # ]
    # lines = [lines_to_list(line) for line in input_text.split("\n\n")]
    # lines = lines_to_list(input_text)

    loader.print_solution("setup", f"{len(input_text)=} ...")
    loader.print_solution(
        1,
        part1(
            input_text,
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
            input_text,
        ),
    )


if __name__ == "__main__":
    main()
    # --
    # --------------------------------------------------------------------------------
    # LAP -> 0.372609        |        0.372609 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : len(input_text)=19999 ...
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 26.816726       |       27.189334 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 6461289671426
    # --------------------------------------------------------------------------------
