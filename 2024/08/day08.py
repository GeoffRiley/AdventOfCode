"""
Advent of code 2024
Day 08: Resonant Collinearity
"""

from itertools import combinations, product
from math import gcd
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


def get_antennas_by_freq(grid, rows, cols):
    antennas_by_freq = {}
    for r, c in product(range(rows), range(cols)):
        ch = grid[r][c]
        if ch.isalnum():  # antenna
            antennas_by_freq.setdefault(ch, []).append((r, c))
    return antennas_by_freq


def get_lines_dict(coords):
    lines = {}
    for (rA, cA), (rB, cB) in combinations(coords, 2):
        dr = rB - rA
        dc = cB - cA
        g = gcd(dr, dc)
        dr //= g
        dc //= g

        # Normalize direction
        if dr < 0 or (dr == 0 and dc < 0):
            dr = -dr
            dc = -dc

            # Compute line constant k: -dc*r + dr*c = k
        k = -dc * rA + dr * cA

        if (dr, dc, k) not in lines:
            lines[(dr, dc, k)] = (rA, cA)
    return lines


def part1(grid: list[str]) -> int:
    """ """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Characters that indicate antennas: a-z, A-Z, 0-9
    # We'll assume any alphanumeric character is an antenna, as stated.

    # Find antennas and group by frequency
    antennas_by_freq = get_antennas_by_freq(grid, rows, cols)

    # Set to hold all antinode positions
    antinodes = set()

    # For each frequency group, find pairs of antennas
    for freq, coords in antennas_by_freq.items():
        # If fewer than 2 antennas, no antinodes
        if len(coords) < 2:
            continue

        # Generate all pairs
        for (rA, cA), (rB, cB) in combinations(coords, 2):
            # Compute the two antinodes for this pair

            # antinode_1 = 2A - B = (2rA - rB, 2cA - cB)
            r1 = 2 * rA - rB
            c1 = 2 * cA - cB

            # antinode_2 = 2B - A = (2rB - rA, 2cB - cA)
            r2 = 2 * rB - rA
            c2 = 2 * cB - cA

            # Check bounds and add if inside
            if 0 <= r1 < rows and 0 <= c1 < cols:
                antinodes.add((r1, c1))
            if 0 <= r2 < rows and 0 <= c2 < cols:
                antinodes.add((r2, c2))

    # The result is the number of unique antinode positions
    return len(antinodes)


def part2(grid: list[str]) -> int:
    """ """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Identify antennas by frequency
    antennas_by_freq = get_antennas_by_freq(grid, rows, cols)

    # A global set for all antinodes
    antinodes = set()

    for freq, coords in antennas_by_freq.items():
        if len(coords) < 2:
            # Only one antenna of this frequency means no lines can be formed
            continue

        # Store lines in a dictionary to avoid duplicates
        lines = get_lines_dict(coords)

        # Enumerate points on each line within the grid
        for (dr, dc, k), (r0, c0) in lines.items():
            # Forward direction
            n = 0
            while True:
                rr = r0 + n * dr
                cc = c0 + n * dc
                if not 0 <= rr < rows or not 0 <= cc < cols:
                    break

                antinodes.add((rr, cc))
                n += 1
            # Backward direction
            n = -1
            while True:
                rr = r0 + n * dr
                cc = c0 + n * dc
                if not 0 <= rr < rows or not 0 <= cc < cols:
                    break

                antinodes.add((rr, cc))
                n -= 1
    # Print the number of antinodes
    return len(antinodes)


def main():
    loader = LoaderLib(2024)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(8)
    else:
        input_text = dedent(
            """\
                ............
                ........0...
                .....0......
                .......0....
                ....0.......
                ......A.....
                ............
                ............
                ........A...
                .........A..
                ............
                ............
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
    # LAP -> 0.000549        |        0.000549 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : len(lines)=50 ...
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.000302        |        0.000850 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 256
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.000563        |        0.001413 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 2   : 1005
    # --------------------------------------------------------------------------------
