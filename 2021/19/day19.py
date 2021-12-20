"""
Advent of code 2021
Day 19: Beacon Scanner
"""
from collections import Counter, deque
from typing import List, Any, Dict

import numpy as np
from numpy import ndarray
from scipy.spatial.transform import Rotation

from aoc.loader import LoaderLib
from aoc.utility import to_list_int

ROTATIONS = [
    Rotation.from_euler(ax, [r1, r2], degrees=True)
    for ax in ['ZX', 'YX']
    for r1 in [0, 90, 180, 270]
    for r2 in [0, 90, 180, 270]
]


def rotation_gen(scanner_list):
    for r in ROTATIONS:
        yield np.round(r.apply(scanner_list)).astype(int)


def part1(scanners: Dict[int, ndarray], loader):
    """
    The `scanners` dictionary passed gives a list of detected
    beacons within the range of each scanner.  The orientation
    of each scanner is unknown though.

    We must attempt to match the triangulations of each scanners'
    results in different orientations until at least 12 matches are
    found within a scanner range.  If 12 matches have been located,
    then it is assumed that all the beacons within that range are
    now correctly oriented and can be added to the list of beacons
    being used to perform the matches.
    """
    # We keep a list of beacons that have been identified (initially
    # it is assumed that scanner[0] is the root for our co-ordinate
    # system).
    beacons = set(tuple(x) for x in scanners[0].astype(int))
    # We keep a tally on the scanners that have not been identified
    # due to being of unknown orientation.  This list will gradually
    # empty as more scanner orientations are uncovered.
    unsatisfied = deque(v for k, v in scanners.items() if k != 0)
    # We gather the positional list of all the scanner relative to
    # the first scanner at co-ordinates (0, 0, 0)
    scanner_positions = list(np.array([0, 0, 0]))

    while unsatisfied:
        # Popping an unsatisfied scanner set off the deque lets us
        # pick up the working sets one at a time with the aim of
        # identifying the correct orientation.
        working = unsatisfied.pop()

        # Rotate the working set around the various axis to seek a match with the
        # known beacon positions
        for rotation in rotation_gen(working):
            c = Counter()
            for beacon in beacons:
                # Working with the already identified beacons, we can
                # find the displacement from any suggested beacons:
                # if there is a match then the displacement will be
                # equal and help to suggest the co-ordinate of the scanner
                # in this sector.
                c.update(tuple(x) for x in (rotation - np.array(beacon, dtype=int)))
            # See if there are 12 beacons that match a single scanner co-ordinate
            # then we assume that all the beacons are orientated correctly and that
            # we have identified the scanner for this sector.
            [(coord, count)] = c.most_common(1)
            if count >= 12:
                # ...if so, we can add all the beacons in this rotation and record
                # that this scanner has been fixed in position.
                beacons |= set(tuple(x) for x in rotation - np.array(coord, dtype=int))
                scanner_positions.append(np.array(coord, dtype=int))
                break
        else:
            # Couldn't find 12 matches?  Return this set, to be attempted again
            # when more points have been confirmed.
            unsatisfied.appendleft(working)

    # Save the scanner positions for part 2!
    loader.cache_data(19, 'positions', scanner_positions)

    return len(beacons)


def part2(loader):
    """
    """
    # Grab the saved scanner positions ready to work out the largest manhattan distance
    # between two scanners.
    scanner_positions = loader.retrieve_data(19, 'positions')

    # The manhattan distances are being calculated by summing the (x, y, z) differences
    # between any two scanners.
    return max(np.abs(x - y).sum() for x in scanner_positions for y in scanner_positions)


def main():
    loader = LoaderLib(2021)
    input_text = loader.get_aoc_input(19)

    # with open('example.txt', 'r') as f:
    #     input_text = f.read()

    scanner_lines: List[List[Any]] = [sc.splitlines(keepends=False) for sc in input_text.split('\n\n')]

    scanners = dict()
    for sc in scanner_lines:
        k, *lines = sc
        scanners[int(k.strip('- scaner'))] = np.array([np.array(to_list_int(line)) for line in lines])

    loader.print_solution(
        'setup',
        f'{len(scanners)} scanners detected'
    )
    loader.print_solution(1, part1(scanners, loader))
    loader.print_solution(2, part2(loader))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.017036        |        0.017036 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 40 scanners detected
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 55.422481       |       55.439517 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 451
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.044912        |       55.484429 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 13184
    # --------------------------------------------------------------------------------
