"""
Advent of code 2021
Day 16:
"""
from math import prod

from aoc.binary_feeder import BinaryFeeder
from aoc.loader import LoaderLib


def load_packet(feed: BinaryFeeder):
    start_index = feed.bit_index

    version = feed.get_bits(3)
    p_type = feed.get_bits(3)
    if p_type == 4:
        # literal value
        result = feed.get_literal()
    else:
        # operators
        mode = feed.get_bits(1)
        if mode:
            sub_packet_count = feed.get_bits(11)
            target_index = feed.total_bits
        else:
            sub_packet_count = feed.total_bits
            sub_packet_size = feed.get_bits(15)
            target_index = feed.bit_index + sub_packet_size
        sub_results = []
        while feed.bit_index < target_index and len(sub_results) < sub_packet_count:
            sub_size, sub_ver, sub_type, sub_result = load_packet(feed)
            version += sub_ver
            sub_results.append(sub_result)
        if p_type == 0:
            result = sum(sub_results)
        elif p_type == 1:
            result = prod(sub_results)
        elif p_type == 2:
            result = min(sub_results)
        elif p_type == 3:
            result = max(sub_results)
        elif p_type == 5:
            result = sub_results[0] > sub_results[1]
        elif p_type == 6:
            result = sub_results[0] < sub_results[1]
        elif p_type == 7:
            result = sub_results[0] == sub_results[1]
        else:
            raise ValueError(f'Unrecognised packet type ({p_type})')

    end_index = feed.bit_index

    return end_index - start_index, version, p_type, result


def part1(line: str):
    """A nice recursive interpreter for the bit stream
    """
    feeder = BinaryFeeder(line)
    packet_size, packet_version, packet_type, packet_result = load_packet(feeder)
    return packet_version


def part2(line: str):
    """Yes, it's exactly the same!
    """
    feeder = BinaryFeeder(line)
    packet_size, packet_version, packet_type, packet_result = load_packet(feeder)
    return packet_result


def main():
    loader = LoaderLib(2021)
    input_text = loader.get_aoc_input(16)

    # input_text = "D2FE28"
    # input_text = "C200B40A82"
    # input_text = "38006F45291200"
    # input_text = "8A004A801A8002F478"
    # input_text = "A0016C880162017C3686B18A3D4780"

    # assert len(lines) == len(...)
    loader.print_solution('setup', f'{len(input_text)} ...')
    loader.print_solution(1, part1(input_text))
    loader.print_solution(2, part2(input_text))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.002772        |        0.002772 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 1370 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.015791        |        0.018562 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 877
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.015217        |        0.033779 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 194435634456
    # --------------------------------------------------------------------------------
