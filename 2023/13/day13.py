"""
Advent of code 2023
Day 13: Point of Incidence
"""
from pprint import pprint
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


def seek_mirror_line(scan: list[str]) -> tuple[bool, int]:
    """
    Search through the scan list for a mirror line.
    The mirror line is a horizontal line that is has identical rows above and
    below it; as far as the data allows.

    Return the number of rows above the mirror line.
    """
    upper_rows = 0
    found_row = False
    for row in range(len(scan) - 1):
        if scan[row] == scan[row + 1]:
            # We have a candidate for a mirror line
            # Check the rows above and below the candidate
            check_len = min(row+1, len(scan) - row - 2)
            for check in range(check_len):
                if scan[row - check - 1] != scan[row + check + 2]:
                    # The candidate is not the mirror line
                    break
            else:
                # The candidate is the mirror line
                upper_rows += row + 1
                found_row = True
                break
    return found_row, upper_rows


def seek_scuff_line(scan: list[str]) -> int:
    """
    Search through the scan list for a scuff on the mirror line.
    The scuff is a single character that is swapped between '.' and '#'.
    When scanning for the mirror line we are looking for a position where the
    number of '#' characters differs by 1 between the rows above and below the
    candidate mirror line.

    Return the number of rows above the mirror line when the scuff is removed.
    """
    # print("*" * 80)
    # pprint(scan)
    # print(f"    {len(scan)}×{len(scan[0])}")
    for row in range(1, len(scan)):
        upper_rows = scan[:row][::-1]
        lower_rows = scan[row:]

        diff_char_count = 0
        for up_row, down_row in zip(upper_rows, lower_rows):
            for up, down in zip(up_row, down_row):
                if up != down:
                    diff_char_count += 1
        if diff_char_count == 1:
            return row

    # print(f"    {upper_rows_count=}")
    return 0


def part1(lines: list[list[str]]) -> int:
    """
    Here we have a list of scans, each scan is represented by a list of
    strings.
    In each case there is a mirror line, either vertical or horizontal, and it
    is always *between* two rows or columns.  The mirror line is always extends
    the full width or height of the scan.
    We need to identify the mirror line, and then return the number of rows or
    columns that are to the left or above the mirror line.
    We should return the sum of the columns and 100 times the sum of the rows.
    """
    left_columns = 0
    upper_rows = 0
    for scan in lines:
        # Identify the mirror line
        # First look for a horizontal mirror line, this can be achieved by
        # comparing pairs of rows, looking for a pair that is identical and
        # checking the rows spreading out from that pair.
        found, rows = seek_mirror_line(scan)
        if found:
            upper_rows += rows
        else:
            # No horizontal mirror line found, try a vertical mirror line
            # This is the same as above, but we are looking for a pair of
            # columns that are identical.
            # We can achieve this by transposing the scan and then using the
            # same function as above.
            found, columns = seek_mirror_line(list(''.join(s) for s in (zip(*scan))))
            if found:
                left_columns += columns
    # Return the sum of the columns and 100 times the sum of the rows
    return left_columns + 100 * upper_rows


def part2(lines) -> int:
    """
    Again we're looking for mirror lines, but this time we need to remove a
    single character from the field of the mirror line.
    """
    left_columns = 0
    upper_rows = 0
    for scan in lines:
        rows = seek_scuff_line(scan)
        upper_rows += rows
        columns = seek_scuff_line(list(''.join(s) for s in (zip(*scan))))
        left_columns += columns
    return left_columns + 100 * upper_rows


def main():
    loader = LoaderLib(2023)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(13)
    else:
        input_text = dedent(
            """\
            #.##..##.
            ..#.##.#.
            ##......#
            ##......#
            ..#.##.#.
            ..##..##.
            #.#.##.#.

            #...##..#
            #....#..#
            ..##..###
            #####.##.
            #####.##.
            ..##..###
            #....#..#
            """
        ).strip("\n")
    # lines = [
    #     (pat, to_list_int(param))
    #     for pat, param in [line.split() for line in lines_to_list(input_text)]
    # ]
    lines = [lines_to_list(line) for line in input_text.split("\n\n")]

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
    # LAP -> 0.000313        |        0.000313 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : len(lines)=100 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    # LAP -> 0.000491        |        0.000805 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 27637
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    # LAP -> 0.003988        |        0.004793 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 2   : 34224
    # --------------------------------------------------------------------------------
