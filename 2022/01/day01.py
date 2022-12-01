"""
Advent of code 2022
Day 01: Calorie Counting
"""
from aoc.loader import LoaderLib


def part1(elf_cal):
    """
    Which elf is carrying the most calories
    """
    return max(map(sum, elf_cal))


def part2(elf_cal):
    """
    Now top three elves!
    """
    sorted_elf_cal = sorted(map(sum, elf_cal))

    return sum(sorted_elf_cal[-3:])


def main():
    loader = LoaderLib(2022)
    input_text = loader.get_aoc_input(1)

    elves = input_text.split('\n\n')

    elf_cal = [tuple(map(int, elf.split('\n'))) for elf in elves]

    loader.print_solution('setup', f'{len(elf_cal)} ...')
    loader.print_solution(1, part1(elf_cal))
    loader.print_solution(2, part2(elf_cal))


if __name__ == '__main__':
    main()
    # --
    # --------------------------------------------------------------------------------
    #  LAP -> 0.005239        |        0.005239 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 249 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.000397        |        0.005636 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 72718
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.000356        |        0.005992 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 213089
    # --------------------------------------------------------------------------------
