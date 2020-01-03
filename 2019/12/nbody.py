from collections import defaultdict
from dataclasses import dataclass
from itertools import permutations
from math import gcd


@dataclass
class Point3D(object):
    x: int = 0
    y: int = 0
    z: int = 0

    def copy(self):
        return Point3D(self.x, self.y, self.z)

    def __add__(self, other):
        return Point3D(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __sub__(self, other):
        return Point3D(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def __str__(self):
        return f'<x={self.x:3}, y={self.y:3}, z={self.z:3}>'


def parse_point(s: str) -> Point3D:
    s = s.strip().lstrip('<').rstrip('>')
    x, y, z = [int(v.split('=')[1]) for v in s.split(',')]
    return Point3D(x, y, z)


class Particle(object):
    def __init__(self, point: Point3D = None):
        if point is None:
            self.point = Point3D()
        else:
            self.point = point
        self.velocity = Point3D()
        self.original_point = self.point.copy()

    def reset(self):
        self.point = self.original_point.copy()
        self.velocity = Point3D()

    @staticmethod
    def _tri_state_compare(val):
        return -1 if val < 0 else 0 if val == 0 else 1

    def gravity_effect(self, other):
        return Point3D(
            Particle._tri_state_compare(other.point.x - self.point.x),
            Particle._tri_state_compare(other.point.y - self.point.y),
            Particle._tri_state_compare(other.point.z - self.point.z)
        )

    def apply_velocity(self):
        self.point += self.velocity

    @property
    def pot(self) -> int:
        p = self.point
        return abs(p.x) + abs(p.y) + abs(p.z)

    @property
    def kin(self) -> int:
        v = self.velocity
        return abs(v.x) + abs(v.y) + abs(v.z)

    @property
    def energy(self) -> int:
        return self.pot * self.kin

    @property
    def at_home(self):
        return self.original_point == self.point

    def __str__(self):
        return f'pos={self.point} vel={self.velocity}'


class Moons(object):
    def __init__(self, moon_text: str = None):
        self.step_count = 0
        self.moons = defaultdict(Particle)
        if moon_text is not None:
            self.moons.update(
                {n: Particle(parse_point(line)) for n, line in enumerate(moon_text.splitlines(keepends=False))})

    def reset(self):
        self.step_count = 0
        for m in self.moons.values():
            m.reset()

    def apply_gravity(self):
        a: Particle
        b: Particle
        for a, b in permutations(self.moons.values(), 2):
            e = a.gravity_effect(b)
            a.velocity += e

    def apply_velocity(self):
        self.step_count += 1
        moon: Particle
        for moon in self.moons.values():
            moon.apply_velocity()

    @property
    def total_energy(self):
        return sum(m.energy for m in self.moons.values())

    def __str__(self):
        return '\n'.join(str(m) for m in self.moons.values())

    def hash_axis(self, the_axis: str):
        if the_axis == 'x':
            return '.'.join(f'{m.point.x}.{m.velocity.x}' for m in self.moons.values())
        elif the_axis == 'y':
            return '.'.join(f'{m.point.y}.{m.velocity.y}' for m in self.moons.values())
        else:
            return '.'.join(f'{m.point.z}.{m.velocity.z}' for m in cluster.moons.values())


def calc_lowest_common_multiple(num_list: iter):
    lcm = num_list[0]
    for b in num_list[1:]:
        lcm = abs(lcm * b) // gcd(lcm, b)
    return lcm


if __name__ == '__main__':
    with open('input') as f:
        moon_str = f.read()
    cluster = Moons(moon_str)
    print('Part 1')
    print(f'Starting set:\n{cluster}')
    for i in range(1000):
        cluster.apply_gravity()
        cluster.apply_velocity()
    print(f'After {cluster.step_count} steps:\n{cluster}\n-- energy={cluster.total_energy} --')
    '''
    After 1000 steps:
    pos=<x=  9, y= 55, z= 20> vel=<x=-20, y=  2, z=-14>
    pos=<x=-63, y=-15, z=-61> vel=<x=  6, y= 15, z=  1>
    pos=<x=-12, y= 19, z= 33> vel=<x=  8, y=  0, z=  3>
    pos=<x= 47, y=-57, z= 19> vel=<x=  6, y=-17, z= 10>
    -- energy=10845 --
    '''
    print('Part 2')
    cluster.reset()
    done = False
    repeat_at = {'x': None, 'y': None, 'z': None}
    history = defaultdict(set)
    for axis in ['x', 'y', 'z']:
        history[axis].add(cluster.hash_axis(axis))
    print(f'After {cluster.step_count} steps:\n{cluster}\n-- energy={cluster.total_energy} --')
    while not done:
        cluster.apply_gravity()
        cluster.apply_velocity()
        if repeat_at['x'] is None:
            h = cluster.hash_axis('x')
            if h in history['x']:
                repeat_at['x'] = cluster.step_count
                print(f'x repeated at {repeat_at["x"]}')
                print(f'After {cluster.step_count} steps:\n{cluster}\n-- energy={cluster.total_energy} --')
            else:
                history['x'].add(h)
        if repeat_at['y'] is None:
            h = cluster.hash_axis('y')
            if h in history['y']:
                repeat_at['y'] = cluster.step_count
                print(f'y repeated at {repeat_at["y"]}')
                print(f'After {cluster.step_count} steps:\n{cluster}\n-- energy={cluster.total_energy} --')
            else:
                history['y'].add(h)
        if repeat_at['z'] is None:
            h = cluster.hash_axis('z')
            if h in history['z']:
                repeat_at['z'] = cluster.step_count
                print(f'z repeated at {repeat_at["z"]}')
                print(f'After {cluster.step_count} steps:\n{cluster}\n-- energy={cluster.total_energy} --')
            else:
                history['z'].add(h)
        done = all(r is not None for r in repeat_at.values())
    print(f'Repetitions on individual axes: {"; ".join(k + "=" + str(v) for k, v in repeat_at.items())}')
    rx, ry, rz = [v for v in repeat_at.values()]
    lcm = calc_lowest_common_multiple([rx, ry, rz])
    print(f'Lowest common repeat is at {lcm}')
    '''
    Repetitions on individual axes: x=186028; y=231614; z=102356
    Lowest common repeat is at 551272644867044
    '''
