"""
Advent of code 2024
Day 04: Ceres Search
"""

from collections import Counter
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import extract_ints, lines_to_list, to_list_int


def part1(lines: list[str]) -> int:
    """
     Find how many occurances of the word "XMAS" appear
     in the given word square
    """
    word = "XMAS"
    nrows = len(lines)
    ncols = len(lines[0])
    count = 0
    directions = [
        (0, 1),    # Right
        (0, -1),   # Left
        (1, 0),    # Down
        (-1, 0),   # Up
        (1, 1),    # Down-Right
        (-1, -1),  # Up-Left
        (1, -1),   # Down-Left
        (-1, 1),   # Up-Right
    ]

    # Convert grid to 2D list of characters for easier access
    grid_chars = [list(row) for row in lines]

    for i in range(nrows):
        for j in range(ncols):
            for dx, dy in directions:
                found = True
                for k in range(len(word)):
                    ni = i + k * dx
                    nj = j + k * dy
                    if 0 <= ni < nrows and 0 <= nj < ncols:
                        if grid_chars[ni][nj] != word[k]:
                            found = False
                            break
                    else:
                        found = False
                        break
                if found:
                    count += 1
    return count


def part2(lines: list[str]) -> int:
    """ """
    nrows = len(lines)
    ncols = len(lines[0])
    count = 0

    # Convert grid to 2D list of characters for easier access
    grid_chars = [list(row) for row in lines]

    for i in range(1, nrows - 1):
        for j in range(1, ncols - 1):
            ch2 = grid_chars[i][j]

            # Get the letters along the NW-SE diagonal
            ch1 = grid_chars[i - 1][j - 1]
            ch3 = grid_chars[i + 1][j + 1]

            # Get the letters along the NE-SW diagonal
            ch4 = grid_chars[i - 1][j + 1]
            ch5 = grid_chars[i + 1][j - 1]

            # Check for all combinations where each "MAS" can be forwards or backwards
            nw_se_options = [('M', 'A', 'S'), ('S', 'A', 'M')]
            ne_sw_options = [('M', 'A', 'S'), ('S', 'A', 'M')]

            for nw_se in nw_se_options:
                for ne_sw in ne_sw_options:
                    if (ch1, ch2, ch3) == nw_se and (ch4, ch2, ch5) == ne_sw:
                        count += 1
    return count


def main():
    loader = LoaderLib(2024)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(4)
    else:
        input_text = dedent(
            """\
                MMMSXXMASM
                MSAMXMSMSA
                AMXSXMAAMM
                MSAMASMSMX
                XMASAMXAMM
                XXAMMXXAMA
                SMSMSASXSS
                SAXAMASAAA
                MAMMMXMMMM
                MXMXAXMASX
            """
        ).strip("\n")
    # lines = [
    #     (extract_ints(param)) for param in [line for line in lines_to_list(input_text)]
    # ]
    # lines = [lines_to_list(line) for line in input_text.split("\n\n")]
    lines = lines_to_list(input_text)

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
    # LAP -> 0.000507        |        0.000507 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : len(lines)=140 ...
    # --------------------------------------------------------------------------------


    # --------------------------------------------------------------------------------
    # LAP -> 0.021737        |        0.022245 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 2633
    # --------------------------------------------------------------------------------


    # --------------------------------------------------------------------------------
    # LAP -> 0.004976        |        0.027220 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 2   : 1936
    # --------------------------------------------------------------------------------

    #
