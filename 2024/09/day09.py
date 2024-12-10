"""
Advent of code 2024
Day 09: Disk Fragmenter
"""

from textwrap import dedent

from aoc.loader import LoaderLib


def part1(input_text: str) -> int:
    """ """
    disc_layout = {}
    is_file = True
    file_id = 0
    current_pos = 0
    for ch in input_text:
        block_len = int(ch)
        if is_file:
            disc_layout |= {
                j: file_id for j in range(current_pos, current_pos + block_len)
            }
            file_id += 1
        is_file = not is_file
        current_pos += block_len

    keyset = set(disc_layout.keys())
    free_empty = set(range(max(keyset))) - keyset
    for fs in free_empty:
        if fs in disc_layout:
            print("Darn it's gone wrong")
            break
        src = max(disc_layout.keys())
        if fs < src:
            disc_layout[fs] = disc_layout.pop(src)

    return sum(i * x for i, x in disc_layout.items())


def part2(input_text: list[str]) -> int:
    """ """
    file_space: dict[int, tuple[int, int]] = {}
    file_dir: dict[int, tuple[int, int]] = {}
    free_space: dict[int, int] = {}
    is_file = True
    file_id = 0
    current_pos = 0
    for ch in input_text:
        block_len = int(ch)
        if is_file:
            if block_len <= 0:
                raise ValueError("File size must be positive")
            file_space[current_pos] = (file_id, block_len)
            file_dir[file_id] = (current_pos, block_len)
            file_id += 1
        else:
            if block_len > 0:
                free_space[current_pos] = block_len
        is_file = not is_file
        current_pos += block_len

    # - Iterate over files in descending order of their ID.
    # - For each file, look for the earliest suitable free space block before
    #   its current position.
    # - If found, move the whole file into that space in one operation.
    # - After processing all files, compute the checksum using the update
    #   positions.

    for fid in sorted(file_dir.keys(), reverse=True):
        fpos, fsize = file_dir[fid]
        for fpos_check in sorted(free_space.keys()):
            # Check if the free space is above the file
            if fpos_check > fpos:
                break
            # Check if the freespace is large enough for the file
            if (freesize := free_space[fpos_check]) >= fsize:
                # Reduce freespace size, increase pointer position
                # Move file to where the freespace was
                # Update freespace pointers
                if freesize == fsize:
                    free_space.pop(fpos_check)
                else:
                    new_free_space = freesize - fsize
                    new_free_pos = fpos_check + fsize
                    free_space.pop(fpos_check)
                    free_space[new_free_pos] = new_free_space
                file_dir.pop(fid)
                file_dir[fid] = (fpos_check, fsize)
                file_space.pop(fpos)
                file_space[fpos_check] = (fid, fsize)
                break

    sub_totals = [
        sum(i * x for x in range(base, base + sz))
        for base, (i, sz) in file_space.items()
    ]
    return sum(sub_totals)


def main():
    loader = LoaderLib(2024)
    testing = False
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
    # LAP -> 0.001307        |        0.001307 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : len(input_text)=19999 ...
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 13.832093       |       13.833400 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 6461289671426
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.395257        |       14.228657 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 2   : 6488291456470
    # --------------------------------------------------------------------------------
