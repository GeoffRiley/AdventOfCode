"""
Advent of code 2022
Day 09: Rope Bridge
"""
from typing import List

from aoc.geometry import Point
from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


# Movements possible:
# Entry condition:  Exit condition:
# .....             .....
# .....             .....
# ..H..             ..H..   Head on Tail: no change
# .....             .....
# .....             .....
#
# .....             .....
# .ttt.             .ttt.
# .tHt.             .tHt.   Tail next to Head: no change
# .ttt.             .ttt.
# .....             .....
#
# ..1..             .....
# .....             ..1..
# 2.H.3             .2H3.   One step above, below or aside:
# .....             ..4..   takes one step in
# ..4..             .....
#
# .1.1.             .....
# 2...3             ..1..
# ..H..             .2H3.   Knights move away:
# 2...3             ..4..   take a diagonal step in
#
# 1...2             .....
# .....             .1.2.
# ..H..             ..H..   Two diagonals away:
# .....             .3.4.   take a diagonal step in
# 3...4             .....


class FollowPoint(Point):
    def move_towards(self, other: Point) -> 'FollowPoint':
        if self.x > other.x:
            self.x -= 1
        elif self.x < other.x:
            self.x += 1
        if self.y > other.y:
            self.y -= 1
        elif self.y < other.y:
            self.y += 1
        return self

    def distance(self, other: Point) -> int:
        """Calculate the rough distance between points"""
        return max(abs(self.x - other.x), abs(self.y - other.y))


def part1(lines: List[str]) -> int:
    """
    Directions are like:
        R 4
        U 4
        L 3
        D 1
        R 4
        D 1
        L 5
        R 2
    these are movements of the head… the tail must always follow
    (distance < 1)
    Head and tail start at (0,0), how many distinct places does the
    tail occupy?
    """
    rule_disp = {'R': Point(1, 0), 'L': Point(-1, 0), 'U': Point(0, 1), 'D': Point(0, -1)}
    tail_record = set()
    head = Point(0, 0)
    tail = FollowPoint(0, 0)
    tail_record.add(tuple(tail))
    for line in lines:
        rule, dist = line.split()
        for _ in range(int(dist)):
            head += rule_disp[rule]
            if tail.distance(head) > 1:
                tail.move_towards(head)
                tail_record.add(tuple(tail))

    return len(tail_record)


def part2(lines: List[str]) -> int:
    """
    Now we have ten knots following each other
    We still need to keep track of the places that
    the tail has been to, but there are eight more
    knots that go between the head and that tail.
    """
    rule_disp = {'R': Point(1, 0), 'L': Point(-1, 0), 'U': Point(0, 1), 'D': Point(0, -1)}
    tail_record = set()
    # Use an array of knots
    knots = [FollowPoint(0, 0) for _ in range(10)]
    tail_record.add(tuple(knots[-1]))
    for line in lines:
        rule, dist = line.split()
        for _ in range(int(dist)):
            knots[0] += rule_disp[rule]
            for knot_h, knot_t in zip(knots[:-1], knots[1:]):
                if knot_t.distance(knot_h) > 1:
                    knot_t.move_towards(knot_h)
            tail_record.add(tuple(knots[-1]))

    return len(tail_record)


def main():
    loader = LoaderLib(2022)
    input_text = loader.get_aoc_input(9)

    # input_text = dedent('''\
    #     R 4
    #     U 4
    #     L 3
    #     D 1
    #     R 4
    #     D 1
    #     L 5
    #     R 2
    # ''').strip('\n')

    lines = lines_to_list(input_text)

    loader.print_solution('setup', f'{len(lines)} ...')
    loader.print_solution(1, part1(lines))
    loader.print_solution(2, part2(lines))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.003048        |        0.003048 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 2000 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.135392        |        0.138440 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 6057
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.640911        |        0.779352 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 2514
    # --------------------------------------------------------------------------------
