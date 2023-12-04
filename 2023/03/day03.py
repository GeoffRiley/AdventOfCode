"""
Advent of code 2023
Day 03: Gear Ratios
"""
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.grid import Grid


def scan_digit(
    grid: Grid,
    location: tuple,
    only_asterisks: bool = False
) -> tuple:
    """
    Scan the grid from the given location for a string of digits.
    Return the string of digits, the list of non-space characters
    encountered and the location of the next non-digit character.
    If only_asterisks is True, then return a string of digits along with
    the co-ordinates of the asterisk character.
    """
    digit_string = ""
    non_space_list = set()
    non_apace_locations = set()
    current_location = location
    current_row = location[1]
    # ensure that we stick to the same row—we stop when we change rows
    while current_location is not None and current_row == current_location[1]:
        char = grid.get(current_location)
        if char.isdigit():  # and char != "0":
            digit_string += char
            non_space_list.update(
                [
                    grid.get(loc)
                    for loc in grid.neighbors(
                        current_location, diagonals=True, valid_only=True
                    )
                    if grid.get(loc) not in ".0123456789"
                ]
            )
            non_apace_locations.update(
                [
                    loc
                    for loc in grid.neighbors(
                        current_location, diagonals=True, valid_only=True
                    )
                    if grid.get(loc) == "*"]
            )
        elif len(digit_string) > 0:
            """
            Make sure that we have a string of digits.
            Otherwise we're still looking for the start of a string of digits.
            """
            break
        current_location = grid.next_location(current_location)

    # print(f"{digit_string} {non_space_list} "
    #       f"{non_apace_locations} {current_location}")

    if only_asterisks:
        return digit_string, list(non_apace_locations), current_location
    else:
        return digit_string, list(non_space_list), current_location


def part1(grid):
    """
    Scan through the grid seeking strings of digits.
    For each string of digits, return the value of that string
    along with a list of any non-space characters—spaces are
    represented by full stops
    Further to this any numbers having non-space characters
    should be summed and returned as the solution.
    """
    game_list = []
    current_location = (0, 0)
    while current_location is not None:
        digit_string, non_space_list, current_location = scan_digit(
            grid, current_location
        )
        if (
            non_space_list is not None
            and len(non_space_list) > 0
            and len(digit_string) > 0
        ):
            game_list.append(int(digit_string))

    return sum(game_list)


def part2(grid):
    """
    Now we need to find the sum of the 'gear ratios' for each string of digits
    that appear adjacent to an asterisk character. For each instance of an
    asterisk, there may be two digit strings adjacent to it. If there are,
    then the gear ratio is the product of the two values. If there is only
    one digit string, then the instance is ignored.
    """
    game_list = []
    current_location = (0, 0)
    ratio_list = dict()
    while current_location is not None:
        digit_string, non_space_list, current_location = scan_digit(
            grid, current_location, only_asterisks=True
        )
        if (
            non_space_list is not None
            and len(non_space_list) > 0
            and len(digit_string) > 0
        ):
            for loc in non_space_list:
                if loc in ratio_list:
                    game_list.append(int(ratio_list[loc]) * int(digit_string))
                    del ratio_list[loc]
                else:
                    ratio_list[loc] = digit_string

    return sum(game_list)


def main():
    loader = LoaderLib(2023)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(3)
    else:
        input_text = dedent(
            """\
            467..114..
            ...*......
            ..35..633.
            ......#...
            617*......
            .....+.58.
            ..592.....
            ......755.
            ...$.*....
            .664.598..
            """
        ).strip("\n")
    grid = Grid().from_text(input_text)

    loader.print_solution("setup", f"{grid.width()} x {grid.height()} ...")
    loader.print_solution(
        1,
        part1(
            grid,
        ),
    )
    loader.print_solution(
        2,
        part2(
            grid,
        ),
    )


if __name__ == "__main__":
    main()
    # --
    # --------------------------------------------------------------------------------
    #  LAP -> 0.004636        |        0.004636 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 140 x 140 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.022959        |        0.027595 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 521515
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.023331        |        0.050926 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 69527306
    # --------------------------------------------------------------------------------
