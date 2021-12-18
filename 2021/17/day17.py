"""
Advent of code 2021
Day 17: Trick Shot
"""

from aoc.geometry import Rectangle
from aoc.loader import LoaderLib
from aoc.maths import sign


class Status:
    KEEP_GOING = 0
    WORKS = 1
    OVERSHOT = 2


class Probe:
    def __init__(self, vel_x, vel_y):
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.x = 0
        self.y = 0
        self.max_y = 0
        self.current_step = 0

    def make_move(self):
        self.x, self.vel_x = self.move_x(self.x, self.vel_x)
        self.y, self.vel_y = self.move_y(self.y, self.vel_y)
        self.current_step += 1
        if self.y > self.max_y:
            self.max_y = self.y

    def check(self, target):
        # if target.pt_in_rect(Point(self.x, self.y)):
        if (target.left <= self.x <= target.right) \
                and (target.bottom <= self.y <= target.top):
            return Status.WORKS
        if (self.x > target.right) or (self.y < target.bottom):
            return Status.OVERSHOT
        return Status.KEEP_GOING

    def try_probe(self, target):
        while True:
            self.make_move()
            result = self.check(target)
            if result == Status.OVERSHOT:
                return False,
            elif result == Status.WORKS:
                return True, self.max_y, self.current_step

    @staticmethod
    def move_x(pos_x: int, vel_x: int):
        pos_x += vel_x
        if vel_x:
            vel_x -= sign(vel_x)
        return pos_x, vel_x

    @staticmethod
    def move_y(pos_y: int, vel_y: int):
        pos_y += vel_y
        vel_y -= 1
        return pos_y, vel_y


def find_valid_x(target_x_min: int, target_x_max: int):
    valid = set()
    for vel_x in range(0, target_x_max + 1):
        init_vel_x = vel_x
        pos_x = 0
        step = 0
        while pos_x < target_x_max:
            step += 1
            pos_x, vel_x = Probe.move_x(pos_x, vel_x)
            if (pos_x >= target_x_min) and (pos_x <= target_x_max):
                valid.add(init_vel_x)
            if vel_x == 0:
                break
    return list(valid)


def find_valid_y(target_y_min: int, target_y_max: int):
    valid = set()
    for vel_y in range(target_y_min, abs(target_y_min) + 1):
        step = 0
        init_vel_y = vel_y
        pos_y = 0
        while pos_y > target_y_min:
            step += 1
            pos_y, vel_y = Probe.move_y(pos_y, vel_y)
            if (pos_y <= target_y_max) and (pos_y >= target_y_min):
                valid.add(init_vel_y)
    return list(valid)


def try_probes(target, valid_x, valid_y):
    max_range = 0
    total = 0
    for vel_y in valid_y:
        for vel_x in valid_x:
            probe = Probe(vel_x, vel_y)
            result = probe.try_probe(target)
            if result[0]:
                total += 1
                if result[1] > max_range:
                    max_range = result[1]
    return max_range, total


def part1(target: Rectangle):
    """
    """
    valid_x = find_valid_x(target.left, target.right)
    valid_y = find_valid_y(target.bottom, target.right)
    results = try_probes(target, valid_x, valid_y)

    return results[0]


def part2(target: Rectangle):
    """
    """
    valid_x = find_valid_x(target.left, target.right)
    valid_y = find_valid_y(target.bottom, target.right)
    results = try_probes(target, valid_x, valid_y)

    return results[1]


def main():
    loader = LoaderLib(2021)
    input_text = loader.get_aoc_input(17)

    # input_text = "target area: x=20..30, y=-10..-5"

    ranges: dict = {
        k: tuple(map(int, v.split('..'))) for k, v in (
            rng.split('=')
            for rng in input_text.removeprefix('target area: ').split(', ')
        )
    }
    # lines = lines_to_list(input_text)
    target: Rectangle = Rectangle(
        ranges['x'][0],
        ranges['y'][1],
        ranges['x'][1],
        ranges['y'][0]
    )

    valid_x = find_valid_x(target.left, target.right)
    valid_y = find_valid_y(target.bottom, target.right)
    results = try_probes(target, valid_x, valid_y)

    # assert len(lines) == len(...)
    loader.print_solution('setup', f'{len(ranges)} ...')
    loader.print_solution(1, part1(target))
    loader.print_solution(2, part2(target))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.026656        |        0.026656 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 2 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 1.613503        |        1.640159 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 19503
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 1.694415        |        3.334573 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 5200
    # --------------------------------------------------------------------------------
