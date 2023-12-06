"""
Advent of code 2023
Day 06: Wait For It
"""
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


def part1(lines):
    """
    We off to the races… well, boat racing anyway.
    Our input is a pair of lists of integers.
    The first list is the maximum time for each race, in milliseconds.
    The second list is the record distance covered by a similar boat in that
    time, in millimeters.
    The boat is energised by pushing a button. When the button is released,
    the boat starts to move. The longer the button is held, the faster the
    boat goes. The boat's speed is measured in millimeters per millisecond.
    We must calculate the number of mmoves that will break the record for
    distance travelled.
    """
    races = []

    for line in lines:
        line = list(map(int, line.split()[1:]))
        if len(races) == 0:
            races = [[num] for num in line]
            # line = [[num] for num in line]
            # races += line
        else:
            for i, time in enumerate(line):
                races[i].append(time)

    race_multiplier = 1

    # We now work through the races, calculating the distance covered
    # by each speed and comparing it to the record distance. Totalling
    # up the winning speeds gives us a partial solution that can be
    # multiplied together to get the final solution.
    for race in races:
        record_breakers = 0
        for speed in range(1, race[0]):
            distance = (race[0] - speed) * speed
            if distance > race[1]:
                record_breakers += 1

        race_multiplier *= record_breakers

    return race_multiplier


def part2(lines):
    """
    Surprise! The tickets are misprinted. There shouldm't be any spaces in
    the input. We can fix that easily enough. Oh, but look at the size of
    the resulting numbers.
    """
    tmp = []
    for i, line in enumerate(lines):
        tmp += [int("".join(line.split()[1:]))]
    time_allowed, distance_record = tmp

    # We can't just brute force this one. The numbers are too big.
    # We need to find the range of speeds that will break the record.
    # We can do this by finding the speed that will break the record
    # at the start and the speed that will break the record at the end.
    # The range of speeds that will break the record is between those
    # two speeds.
    left = 1
    for speed in range(1, time_allowed - 1):
        distance = (time_allowed - speed) * speed
        if distance > distance_record:
            left = speed
            break

    # The right side is a little trickier. We have to start at the
    # end and work backwards. We need to find the speed that will break
    # the record at the end and then work backwards until we find the
    # speed that will break the record at the start.
    right = time_allowed - 1
    for speed in range(time_allowed - 1, left, -1):
        distance = (time_allowed - speed) * speed
        if distance > distance_record:
            right = speed
            break

    return right - left + 1


def main():
    loader = LoaderLib(2023)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(6)
    else:
        input_text = dedent(
            """\
            Time:      7  15   30
            Distance:  9  40  200
            """
        ).strip("\n")
    lines = lines_to_list(input_text)

    loader.print_solution("setup", f"{len(lines)} ...")
    loader.print_solution(
        1,
        part1(
            lines,
        ),
    )
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
    # LAP -> 0.000118        |        0.000118 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : 2 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    # LAP -> 0.000088        |        0.000205 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 4568778
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    # LAP -> 0.604248        |        0.604453 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 2   : 28973936
    # --------------------------------------------------------------------------------
