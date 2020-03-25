import re
from collections import UserList
from math import log10

VECTOR_MATCH = re.compile(r'^ position=< (?P<position> \s* [-+]? \d+,\s* [-+]? \d+) >'
                          r'\s velocity=< (?P<velocity> \s* [-+]? \d+,\s* [-+]? \d+) >$', re.VERBOSE)


class Star(object):
    def __init__(self, vec_str: str):
        matches = VECTOR_MATCH.match(vec_str)
        self.position = [int(i) for i in matches.group('position').split(',')]
        self.velocity = [int(i) for i in matches.group('velocity').split(',')]
        self._multiplier = 1

    def fwd(self):
        self.position[0] += self.velocity[0] * self._multiplier
        self.position[1] += self.velocity[1] * self._multiplier

    def rewind(self):
        self.position[0] -= self.velocity[0] * self._multiplier
        self.position[1] -= self.velocity[1] * self._multiplier

    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]

    @property
    def multiplier(self):
        return self._multiplier

    @multiplier.setter
    def multiplier(self, value):
        self._multiplier = value


class Constellation(UserList):
    def __init__(self, lst=None):
        if lst is None:
            lst = []
        super().__init__(lst)
        self.multiplier = 1
        self.motion = 0

    def fwd(self):
        for star in self.data:
            star.fwd()
        self.motion += self.multiplier

    def rewind(self):
        for star in self.data:
            star.rewind()
        self.motion -= self.multiplier

    def update_multiplier(self, set_val=None):
        if set_val is None:
            lg = min(round(log10(self.span_x)), round(log10(self.span_y)))
        else:
            lg = set_val
        if lg == 0:
            lg = 1
        new_mult = 2 ** (lg - 1)
        if new_mult != self.multiplier:
            self.multiplier = new_mult
            for star in self.data:
                star.multiplier = new_mult

    @property
    def max_x(self):
        return max(self.data, key=lambda v: v.x).x

    @property
    def max_y(self):
        return max(self.data, key=lambda v: v.y).y

    @property
    def min_x(self):
        return min(self.data, key=lambda v: v.x).x

    @property
    def min_y(self):
        return min(self.data, key=lambda v: v.y).y

    @property
    def span_x(self):
        return self.max_x - self.min_x

    @property
    def span_y(self):
        return self.max_y - self.min_y

    def image(self):
        w, h = self.span_x, self.span_y
        m_x, m_y = self.min_x, self.min_y
        img = [[' ' for _ in range(w + 1)] for _ in range(h + 1)]
        for star in self.data:
            x, y = star.x - m_x, star.y - m_y
            img[abs(y)][abs(x)] = '#'
        return '\n'.join(''.join(line) for line in img)


def the_stars_align(inp):
    stars = Constellation(Star(line) for line in inp)
    span_x = stars.span_x
    span_y = stars.span_y
    for i in range(10000):
        stars.update_multiplier()
        stars.fwd()
        if span_x < stars.span_x or span_y < stars.span_y:
            stars.rewind()
            break
        span_x = stars.span_x
        span_y = stars.span_y
    print(stars.image())
    return stars.motion


if __name__ == '__main__':
    with open('input.txt') as vector_file:
        vector_list = vector_file.read().splitlines(keepends=False)
        print('Day 10, part 1:')
        print(f'Day 10, part 2: {the_stars_align(vector_list)}')
        # Day 10, part 1:
        #
        #   ##    #####    ####   #    #     ###  #####   #    #  ######
        #  #  #   #    #  #    #  #    #      #   #    #  #    #  #
        # #    #  #    #  #        #  #       #   #    #   #  #   #
        # #    #  #    #  #        #  #       #   #    #   #  #   #
        # #    #  #####   #         ##        #   #####     ##    #####
        # ######  #    #  #  ###    ##        #   #    #    ##    #
        # #    #  #    #  #    #   #  #       #   #    #   #  #   #
        # #    #  #    #  #    #   #  #   #   #   #    #   #  #   #
        # #    #  #    #  #   ##  #    #  #   #   #    #  #    #  #
        # #    #  #####    ### #  #    #   ###    #####   #    #  #
        #
        # Day 10, part 2: 10619
