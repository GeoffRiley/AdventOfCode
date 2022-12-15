"""
Advent of code 2022
Day 15: Beacon Exclusion Zone
"""
import math
from textwrap import dedent
from typing import List, Dict, Tuple

from aoc.loader import LoaderLib
from aoc.maths import manhattan_distance
from aoc.utility import lines_to_list, extract_ints

AIR = 0
SENSOR = 1
BEACON = 2
COVERED = 4


def part1(survey: List[Dict[str, Tuple[int, int]]], measure_line) -> int:
    """
    :param survey:
    :param measure_line:
    """
    # keep a tally of where the sensors are and their ranges
    sensors = set()
    # keep a tally of where the known beacons are
    beacons = set()
    # we're only checking a row, so track the max and min x values
    max_x, min_x = -math.inf, math.inf
    for plot in survey:
        dist = manhattan_distance(plot['sensor'], plot['beacon'])
        sensors.add((tuple(plot['sensor']), dist))
        beacons.add(tuple(plot['beacon']))
        max_x = max(max_x, plot['sensor'][0] + dist)
        min_x = min(min_x, plot['sensor'][0] - dist)

    def in_sensor_range(tp: tuple) -> bool:
        for sn, r in sensors:
            mh = manhattan_distance(sn, tp)
            if mh <= r:
                return True
        return False

    no_beacon = 0
    for x in range(min_x, max_x + 1):
        test_point = (x, measure_line)
        if in_sensor_range(test_point) and test_point not in beacons:
            no_beacon += 1

    return no_beacon


def part2(survey: List[Dict[str, Tuple[int, int]]], max_search) -> int:
    """
    We need to find a spot that is outside all the sensor ranges
    If there is only one spot, then it must be next to one or more
    sensor areas… therefore it will have a manhattan distance one greater
    than the beacon range discovered.
    :param survey:
    :param max_search:
    """
    # keep a tally of where the sensors are and their ranges
    sensors = set()
    # keep a tally of where the known beacons are
    beacons = set()

    for plot in survey:
        dist = manhattan_distance(plot['sensor'], plot['beacon'])
        sensors.add((plot['sensor'], dist))
        beacons.add(plot['beacon'])

    def in_sensor_range(tp: tuple) -> bool:
        for sn, r in sensors:
            mh = manhattan_distance(sn, tp)
            if mh <= r:
                return True
        return False

    # sector multipliers
    sector_pointers = [
        (-1, -1),
        (-1, 1),
        (1, -1),
        (1, 1)
    ]
    answer = 0
    for (sx, sy), sd in sensors:
        # We're going to look at everywhere that is sd+1 distance from (sx, sy)
        for dx in range(sd + 2):
            dy = sd - dx + 1
            # check pn all four sectors…
            for mx, my in sector_pointers:
                cx, cy = sx + (dx * mx), sy + (dy * my)
                if not (0 <= cx <= max_search) or not (0 <= cy <= max_search):
                    continue
                if not in_sensor_range((cx, cy)):
                    answer = cx * 4_000_000 + cy
                    print(answer)

    return answer


def main():
    loader = LoaderLib(2022)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(15)
        measure_line = 2_000_000
        max_search = 4_000_000
    else:
        # input_text = (Path.cwd() / 'testdata.txt').read_text().strip('\n')
        input_text = dedent('''\
            Sensor at x=2, y=18: closest beacon is at x=-2, y=15
            Sensor at x=9, y=16: closest beacon is at x=10, y=16
            Sensor at x=13, y=2: closest beacon is at x=15, y=3
            Sensor at x=12, y=14: closest beacon is at x=10, y=16
            Sensor at x=10, y=20: closest beacon is at x=10, y=16
            Sensor at x=14, y=17: closest beacon is at x=10, y=16
            Sensor at x=8, y=7: closest beacon is at x=2, y=10
            Sensor at x=2, y=0: closest beacon is at x=2, y=10
            Sensor at x=0, y=11: closest beacon is at x=2, y=10
            Sensor at x=20, y=14: closest beacon is at x=25, y=17
            Sensor at x=17, y=20: closest beacon is at x=21, y=22
            Sensor at x=16, y=7: closest beacon is at x=15, y=3
            Sensor at x=14, y=3: closest beacon is at x=15, y=3
            Sensor at x=20, y=1: closest beacon is at x=15, y=3
        ''').strip('\n')
        measure_line = 10
        max_search = 20

    survey = []
    for line in lines_to_list(input_text):
        parts = line.split(':')
        survey.append(
            dict(sensor=tuple(extract_ints(parts[0], True)), beacon=tuple(extract_ints(parts[1], True)))
        )

    # assert len(lines) == len(...)
    loader.print_solution('setup', f'{len(survey)} ...')
    loader.print_solution(1, part1(survey, measure_line))
    loader.print_solution(2, part2(survey, max_search))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.004530        |        0.004530 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 38 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 164.259245      |      164.263775 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 4886370
    # --------------------------------------------------------------------------------
    #
    # 11374534948438
    # 11374534948438
    # 11374534948438
    # 11374534948438
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 1613.880357     |     1778.144132 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 11374534948438
    # --------------------------------------------------------------------------------
