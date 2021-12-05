"""
Advent of code 2021
Day 5: Hydrothermal Venture
"""
from collections import Counter
from typing import List

from shapely.geometry import LineString

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list, extract_ints, pairwise


def part1(segments: List[LineString]):
    """We're going to uncover all positions in 2D space where the given
    segments overlap.
    As we're only considering horizontal and vertical segments for this first
    part the sequence of x and y values are irrelevant, so it is adequate to
    use the 'bounds' property---no need to test for the highest of the varying
    coordinate.
    """
    grid = Counter()
    for seg in segments:
        x1, y1, x2, y2 = map(int, seg.bounds)
        if x1 == x2:
            grid.update([(x1, y) for y in range(y1, y2 + 1)])
        elif y1 == y2:
            grid.update([(x, y1) for x in range(x1, x2 + 1)])
        else:
            pass

    c = sum(v > 1 for v in grid.values())
    return c, f'grid contains {len(grid)} items'
    # 5147


def part2(segments: List[LineString]):
    """For part 2 it is necessary to consider all the diagonal segments too.
    It is important to use the actual points so that the negative gradients
    may be identified as well as the positive ones.
    Using the `bounds` method is out and the `coords` method must be used.
    This normally returns List[Tuple[float, float], Tuple[float, float]] so
    a comprehension is used to convert to a pair of int tuples that can be
    assigned via the standard tuple unpacking.
    As our coordinates are no longer sorted it is necessary to check that the
    lines are projected in the right order.
    """
    grid = Counter()
    for seg in segments:
        (x1, y1), (x2, y2) = [(int(c[0]), int(c[1])) for c in seg.coords]
        if x1 == x2:
            y1, y2 = min(y1, y2), max(y1, y2)
            grid.update([(x1, y) for y in range(y1, y2 + 1)])
        elif y1 == y2:
            x1, x2 = min(x1, x2), max(x1, x2)
            grid.update([(x, y1) for x in range(x1, x2 + 1)])
        else:
            assert abs((x1 - x2) / (y1 - y2)) == 1
            # There are four ways a diagonal can go, so we must test
            # for each one separately.
            if x1 < x2:
                if y1 < y2:
                    grid.update([(x1 + i, y1 + i) for i in range(x2 - x1 + 1)])
                else:
                    grid.update([(x1 + i, y1 - i) for i in range(x2 - x1 + 1)])
            else:
                if y1 < y2:
                    grid.update([(x1 - i, y1 + i) for i in range(x1 - x2 + 1)])
                else:
                    grid.update([(x1 - i, y1 - i) for i in range(x1 - x2 + 1)])

    c = sum(v > 1 for v in grid.values())

    return c, f'grid contains {len(grid)} items'


def main():
    loader = LoaderLib(2021)
    input_text = loader.get_aoc_input(5)
    #     input_text = """0,9 -> 5,9
    # 8,0 -> 0,8
    # 9,4 -> 3,4
    # 2,2 -> 2,1
    # 7,0 -> 7,4
    # 6,4 -> 2,0
    # 0,9 -> 2,9
    # 3,4 -> 1,4
    # 0,0 -> 8,8
    # 5,5 -> 8,2"""
    lines = lines_to_list(input_text)

    segments = [LineString(pairwise(extract_ints(line))) for line in lines]

    assert len(lines) == len(segments)
    loader.print_solution('setup', f'{len(segments)} segments loaded')
    loader.print_solution(1, part1(segments))
    loader.print_solution(2, part2(segments))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.023525        |        0.023525 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 500 segments loaded
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.192453        |        0.215978 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : (5147, 'grid contains 106688 items')
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.268647        |        0.484625 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : (16925, 'grid contains 168997 items')
    # --------------------------------------------------------------------------------
