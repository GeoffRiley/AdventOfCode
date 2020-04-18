import re
from collections import deque, Counter
from copy import deepcopy
from dataclasses import dataclass
from operator import add
from statistics import mean
from typing import List


@dataclass
class Particle(object):
    id: int
    pos: List[int]
    vec: List[int]
    acc: List[int]

    @property
    def dist(self):
        return sum(abs(x) for x in self.pos)

    @property
    def pos_hash(self):
        return hash(tuple(self.pos))

    def move(self):
        self.vec = list(map(add, self.vec, self.acc))
        self.pos = list(map(add, self.pos, self.vec))


VECTOR_RE = re.compile(r'^p=<([-\d,]+)>,\s+'
                       r' v=<([-\d,]+)>,\s+'
                       r' a=<([-\d,]+)>', re.VERBOSE)


def particle_swarm(particles: List[Particle], part1=True):
    last_close = deque([0 for _ in range(20)], maxlen=150)
    if part1:
        closest_particle = calc_closest(particles)
    else:
        closest_particle = len(particles)
    while mean(last_close) != closest_particle:
        last_close.append(closest_particle)
        move_particles(particles)
        if part1:
            closest_particle = calc_closest(particles)
        else:
            remove_collisions(particles)
            closest_particle = len(particles)
    return closest_particle


def remove_collisions(particles: List[Particle]) -> None:
    collision_collection = Counter(map(lambda p: p.pos_hash, particles))
    for pos, cnt in collision_collection.items():
        if cnt == 1:
            continue
        particle_array = [p for p in particles if p.pos_hash == pos]
        for p in particle_array:
            particles.remove(p)


def move_particles(particles: List[Particle]) -> None:
    for particle in particles:
        particle.move()


def calc_closest(particles: List[Particle]) -> int:
    min_part = min(particles, key=lambda p: p.dist)
    return min_part.id


def parse_particle_list(inp: List[str]) -> List[Particle]:
    particles = []
    for n, line in enumerate(inp):
        pos_s, vec_s, acc_s = (list(map(int, s.split(','))) for s in VECTOR_RE.match(line).groups())
        particles.append(Particle(n, pos_s, vec_s, acc_s))
    return particles


if __name__ == '__main__':
    with open('input.txt') as swarm_file:
        swarm_list = swarm_file.read().splitlines(keepends=False)
        particle_list = parse_particle_list(swarm_list)
        particle_list_2 = deepcopy(particle_list)
        print(f'Day 20, part 1: {particle_swarm(particle_list)}')
        print(f'Day 20, part 2: {particle_swarm(particle_list_2, False)}')
        # Day 20, part 1: 243
        # Day 20, part 2: 648
