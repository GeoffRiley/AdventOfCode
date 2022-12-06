"""
Advent of code 2022
Day 06: Tuning Trouble
"""
from aoc.loader import LoaderLib


def seek_packet_header(line: str, head_len: int = 4) -> int:
    """
    Find the end of the transmission header of length 'head_len' within
    the data stream 'line'

    :param line: Data stream
    :param head_len: Identifying length of unique header
    :return: int
    """
    for n in range(len(line) - head_len):
        if len(set(line[n:n + head_len])) == head_len:
            return n + head_len
    return NotImplemented


def part1(line: str) -> int:
    """
    given a string "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
    find the end of a four character unique sequence… "jpqm"
    and return the end position… 7
    """
    return seek_packet_header(line)


def part2(line: str) -> int:
    """
    given a string "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
    find the end of a fourteen character unique sequence… "pqmgbljsphdztn"
    and return the end position… 19
    """
    return seek_packet_header(line, 14)


def main():
    loader = LoaderLib(2022)
    input_text, target = loader.get_aoc_input(6), None

    # input_text, target = 'mjqjpqmgbljsphdztnvjfqwrcgsmlb', (7, 19)
    # input_text, target = 'bvwbjplbgvbhsrlpgdmjqwftvncz', (5, 23)
    # input_text, target = 'nppdvjthqldpwncqszvftbrmjlhg', (6, 23)
    # input_text, target = 'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', (10, 29)
    # input_text, target = 'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', (11, 26)

    loader.print_solution('setup', f'{len(input_text)} ...')
    loader.print_solution(1, part1(input_text))
    loader.print_solution(2, part2(input_text))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.003153        |        0.003153 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 4095 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.002949        |        0.006102 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 1538
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.005988        |        0.012090 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 2315
    # --------------------------------------------------------------------------------
