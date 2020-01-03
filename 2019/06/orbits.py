from collections import defaultdict
from typing import Dict, List

MAP = '''COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L'''

MAP2 = '''COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN'''


class Orbiter(object):
    def __init__(self, orbiting='', check=0):
        self._orbiting = orbiting
        self._check = check

    @property
    def orbiting(self):
        return self._orbiting

    @property
    def check(self):
        return self._check

    @check.setter
    def check(self, check):
        self._check = check


def set_check(com: str, space: Dict[str, Orbiter]):
    new_check = space[com].check + 1
    for k, v in space.items():
        if v.orbiting == com:
            v.check = new_check
            set_check(k, space)


def get_path(space: Dict[str, Orbiter], target: str) -> List[str]:
    end = space[target]
    path = []
    while end.orbiting != '':
        path.append(end.orbiting)
        end = space[end.orbiting]
    return path[::-1]


def make_map(map: str) -> Dict[str, Orbiter]:
    space = defaultdict(Orbiter)
    for line in map.splitlines(keepends=False):
        centre, orbiter = line.split(')')
        if centre not in space.keys():
            space[centre] = Orbiter('', 0)
        space[orbiter] = Orbiter(centre, 0)
    com = [k for k, v in space.items() if v.orbiting == ''][0]
    set_check(com, space)
    return space


def orbit_count(map: str = MAP, element: str = None):
    map_d = make_map(map)
    return map_d[element].check


def indirect_orbits(map: str = MAP):
    map_d = make_map(map)
    return sum(v.check for _, v in map_d.items())


def orbit_transfer_count(map: str = MAP2, src='YOU', target='SAN'):
    map_d = make_map(map)
    path_src = get_path(map_d, src)
    path_target = get_path(map_d, target)
    while path_src[:1] == path_target[:1]:
        path_src.pop(0)
        path_target.pop(0)
    return len(path_src) + len(path_target)


if __name__ == '__main__':
    with open('input') as f:
        map = f.read()
    print(f'Indirect orbits = {indirect_orbits(map)}')
    print(f'Orbits from YOU to SAN = {orbit_transfer_count(map, "YOU", "SAN")}')
