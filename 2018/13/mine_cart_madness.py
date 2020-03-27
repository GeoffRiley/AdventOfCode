from collections import defaultdict
from dataclasses import dataclass
from itertools import cycle
from typing import List

NORTH = '^'
SOUTH = 'v'
EAST = '>'
WEST = '<'
DIRECTIONS = (NORTH, SOUTH, EAST, WEST)
DIR_NAMES = {NORTH: 'NORTH', WEST: 'WEST', SOUTH: 'SOUTH', EAST: 'EAST'}
LEFT = {NORTH: WEST, WEST: SOUTH, SOUTH: EAST, EAST: NORTH}
FORWARD = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}
RIGHT = {NORTH: EAST, EAST: SOUTH, SOUTH: WEST, WEST: NORTH}
VECTOR = {NORTH: -1j, EAST: 1, SOUTH: 1j, WEST: -1}
VEC_DIR = dict((v, k) for k, v in VECTOR.items())
TRACK_VERTICAL = '|'
TRACK_HORIZONTAL = '-'
TRACK_REGULAR = (TRACK_VERTICAL, TRACK_HORIZONTAL)
TRACK_CORNER_TL_BR = '/'
TRACK_CORNER_TR_BL = '\\'  # has to be 'quoted'
TRACK_CROSSING = '+'
TRACK_CRITICALS = (TRACK_CORNER_TL_BR, TRACK_CORNER_TR_BL, TRACK_CROSSING)
DIR_REPLACEMENT = {NORTH: TRACK_VERTICAL, SOUTH: TRACK_VERTICAL, WEST: TRACK_HORIZONTAL, EAST: TRACK_HORIZONTAL}


@dataclass
class Cart(object):
    x: int = 0
    y: int = 0
    dir: str = NORTH

    def __post_init__(self):
        self._pos = self.x + self.y * 1j
        self._d = VECTOR[self.dir]
        self._turn = cycle([-1j, 1, 1j])

    def forward(self):
        self._pos += self._d
        self.x = int(self._pos.real)
        self.y = int(self._pos.imag)
        return self

    def turn(self, track_piece):
        if track_piece == TRACK_CROSSING:
            self._d *= next(self._turn)
        elif track_piece in TRACK_CRITICALS:
            self._d *= 1j * (2 * ((track_piece == '\\') ^ (self._d.real == 0)) - 1)
        self.dir = VEC_DIR[self._d]
        return self

    @property
    def pos(self):
        return self.x, self.y

    @property
    def posi(self):
        return self._pos

    @property
    def as_tuple(self):
        return self.x, self.y, self.dir

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x},{self.y},'{self.dir}')"

    def __str__(self):
        return f'({self.x},{self.y},{DIR_NAMES[self.dir]})'

    def __lt__(self, other):
        usx, usy = self.pos
        themx, themy = other.pos
        if usy == themy:
            return usx < themx
        return usy < themy

    def copy(self):
        new_cart = Cart(self.x, self.y, self.dir)
        return new_cart


class Track(object):
    def __init__(self, track_map: List[str]):
        self._track_map = track_map
        self._carts = []
        self._tracks = defaultdict(lambda: ' ')
        for y, row in enumerate(track_map):
            for x, c in enumerate(row):
                track_pos = x + y * 1j
                if c in DIRECTIONS:
                    self._carts.append(Cart(x, y, c))
                    self._tracks[track_pos] = DIR_REPLACEMENT[c]
                elif c in TRACK_CRITICALS:
                    self._tracks[track_pos] = c
                elif c in TRACK_REGULAR:
                    self._tracks[track_pos] = c

    def tick(self):
        collision = False
        collision_list = []
        s_carts = sorted(self._carts)
        for cart in s_carts:
            if cart not in self._carts:
                continue
            cart.forward()
            loc_check = self._tracks[cart.posi]
            if loc_check == ' ':
                print(f"Cart off the tracks: {cart} '{loc_check}'")
            cart.turn(loc_check)
            bang = [c for c in self._carts if c.posi == cart.posi]
            if len(bang) > 1:
                collision = True
                collision_list.append(cart.pos)
                for c in bang:
                    self._carts.remove(c)
        return collision, collision_list


def mine_cart_madness_part_1(inp):
    track = Track(inp)
    while True:
        collision, col_list = track.tick()
        if collision:
            return str(col_list[0]).replace(' ', '')


def mine_cart_madness_part_2(inp):
    track = Track(inp)
    while len(track._carts) > 1:
        track.tick()
    return str(track._carts[0].pos).replace(' ', '')


if __name__ == '__main__':
    with open('input.txt') as track_file:
        track_lines = track_file.read().splitlines(keepends=False)
        print(f'Day 13, part 1: {mine_cart_madness_part_1(track_lines)}')
        print(f'Day 13, part 2: {mine_cart_madness_part_2(track_lines)}')
        # Day 13, part 1: [(117, 62)]
        # Day 13, part 2: (69,67)
