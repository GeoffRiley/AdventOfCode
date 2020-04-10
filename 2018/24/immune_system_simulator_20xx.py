"""

System format:

Immune System:
2208 units each with 6238  hit points (immune to slashing)                                         with an attack that does 23  bludgeoning damage at initiative 20
7603 units each with 6395  hit points (weak to radiation)                                          with an attack that does 6   cold        damage at initiative 15
4859 units each with 5904  hit points (weak to fire)                                               with an attack that does 12  cold        damage at initiative 11
1608 units each with 7045  hit points (weak to fire, cold;       immune to bludgeoning, radiation) with an attack that does 31  radiation   damage at initiative 10
39   units each with 4208  hit points                                                              with an attack that does 903 radiation   damage at initiative 7
6969 units each with 9562  hit points (immune to slashing, cold)                                   with an attack that does 13  slashing    damage at initiative 3
2483 units each with 6054  hit points (immune to fire)                                             with an attack that does 20  cold        damage at initiative 19
506  units each with 3336  hit points                                                              with an attack that does 64  radiation   damage at initiative 6
2260 units each with 10174 hit points (weak to fire)                                               with an attack that does 34  slashing    damage at initiative 5
2817 units each with 9549  hit points (immune to cold, fire;     weak to bludgeoning)              with an attack that does 31  cold        damage at initiative 2

Infection:
3650 units each with 25061 hit points (weak to fire, bludgeoning)                                  with an attack that does 11  slashing    damage at initiative 12
508  units each with 48731 hit points (weak to bludgeoning)                                        with an attack that does 172 cold        damage at initiative 13
724  units each with 27385 hit points                                                              with an attack that does 69  radiation   damage at initiative 1
188  units each with 41786 hit points                                                              with an attack that does 416 bludgeoning damage at initiative 4
3045 units each with 36947 hit points (weak to slashing;         immune to fire, bludgeoning)      with an attack that does 24  slashing    damage at initiative 9
7006 units each with 42545 hit points (immune to cold, slashing, fire)                             with an attack that does 9   fire        damage at initiative 16
853  units each with 55723 hit points (weak to cold, fire)                                         with an attack that does 114 bludgeoning damage at initiative 17
3268 units each with 43027 hit points (immune to slashing, fire)                                   with an attack that does 25  slashing    damage at initiative 8
1630 units each with 47273 hit points (weak to cold, bludgeoning)                                  with an attack that does 57  slashing    damage at initiative 14
3383 units each with 12238 hit points                                                              with an attack that does 7   radiation   damage at initiative 18

"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Union, Set

LINE_PARSE = re.compile(r'^(?P<units>\d+) \s units.* '
                        r'with \s (?P<hp>\d+) \s hit\spoints \s '
                        r'(?:\((?P<weakness>[^)]+)\) \s)? '
                        r'with.*does \s (?P<dp>\d+) \s (?P<damtype>\w+) \s damage '
                        r'.*initiative \s (?P<initiative>\d+) '
                        r'$', re.VERBOSE)


@dataclass
class UnitGroup(object):
    unit_count: int
    hit_points: int
    dam_points: int
    dam_type: str
    initiative: int
    immunities: Set[str] = None
    weaknesses: Set[str] = None
    under_attack: bool = False
    _target: Union[UnitGroup, None] = None

    @property
    def effective_power(self) -> int:
        return self.unit_count * self.dam_points

    @property
    def target(self) -> UnitGroup:
        return self._target

    @target.setter
    def target(self, other: Union[UnitGroup, None]):
        self._target = other
        if other is not None:
            other.under_attack = True

    def damage_imparted(self, other: UnitGroup) -> int:
        return self.effective_power * (
            0 if self.dam_type in other.immunities else 2 if self.dam_type in other.weaknesses else 1)

    def attack(self):
        if self.target:
            dam = self.target.damage_imparted(self)
            self.target.unit_count = max(0, self.target.unit_count - dam // self.hit_points)


class Armies(object):
    def __init__(self, _type: str):
        self.groups: List[UnitGroup] = []
        self._type: str = _type

    def reset_attacks(self) -> Armies:
        dead_list = []
        for unit in self.groups:
            if unit.unit_count == 0:
                dead_list.append(unit)
                continue
            unit.under_attack = False
            unit.target = None
        for unit in dead_list:
            self.groups.remove(unit)
        return self

    def add(self, unit: UnitGroup) -> Armies:
        if unit is not None:
            self.groups.append(unit)
        return self

    def show(self) -> Armies:
        print(f'{self._type}:')
        for n, unit in enumerate(sorted(self.groups, key=lambda x: (x.unit_count, x.initiative))):
            print(
                f'Group {n} contains {unit.unit_count} unit{"s" if unit.unit_count != 1 else ""} (init: {unit.initiative})')
        return self

    def match_target(self, other: UnitGroup) -> UnitGroup:
        defenders = sorted([u for u in self.groups if not u.under_attack],
                           key=lambda x: (-x.damage_imparted(other), -x.initiative))
        return defenders[0] if len(defenders) > 0 else None

    @property
    def count(self) -> int:
        return len(self.groups)

    @property
    def unit_count(self) -> int:
        return sum(unit.unit_count for unit in self.groups)

    @property
    def targeting_order(self) -> List[UnitGroup]:
        return sorted(self.groups, key=lambda x: (-x.effective_power, -x.initiative))


def parse_line(line: str) -> Union[UnitGroup, None]:
    match = LINE_PARSE.match(line)
    if match is None:
        return None
    units = int(match.group('units'))
    hit_points = int(match.group('hp'))
    dam_points = int(match.group('dp'))
    dam_type = match.group('damtype')
    initiative = int(match.group('initiative'))
    weak = match.group('weakness') or ''
    immunities = set()
    weaknesses = set()
    for strain in weak.split('; '):
        if strain.startswith('immune to '):
            immunities |= set(strain[len('immune to '):].split(', '))
        elif strain.startswith('weak to '):
            weaknesses |= set(strain[len('weak to '):].split(', '))
    return UnitGroup(unit_count=units, hit_points=hit_points, dam_points=dam_points, dam_type=dam_type,
                     initiative=initiative, immunities=immunities, weaknesses=weaknesses)


def war(immune: Armies, infection: Armies):
    while immune.count > 0 and infection.count > 0:
        immune.reset_attacks()  # .show()
        infection.reset_attacks()  # .show()
        for unit in immune.targeting_order:
            unit.target = infection.match_target(unit)
        for unit in infection.targeting_order:
            unit.target = immune.match_target(unit)
        attack_sequence = sorted(immune.groups + infection.groups, key=lambda x: (-x.initiative))
        for unit in attack_sequence:
            unit.attack()
    return immune.unit_count + infection.unit_count


def immune_system_simulator_20xx(inp):
    immune = Armies('Immune System')
    infection = Armies('Infection')
    current = immune
    for line in inp:
        if len(line.strip()) == 0:
            continue
        if line.startswith('Immune System:'):
            current = immune
            continue
        if line.startswith('Infection:'):
            current = infection
            continue
        current.add(parse_line(line))
    return war(immune, infection)


if __name__ == '__main__':
    with open('input.txt') as rule_file:
        rules = rule_file.read().splitlines(keepends=False)
        print(f'Day 24, part 1: {immune_system_simulator_20xx(rules)}')
