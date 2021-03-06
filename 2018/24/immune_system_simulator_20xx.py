from __future__ import annotations

import re
from copy import deepcopy
from dataclasses import dataclass
from typing import List, Union, Set

DEBUG = False
LINE_PARSE = re.compile(r'^(?P<units>\d+) \s units.* '
                        r'with \s (?P<hp>\d+) \s hit\spoints \s '
                        r'(?:\((?P<weakness>[^)]+)\) \s)? '
                        r'with.*does \s (?P<dp>\d+) \s (?P<damtype>\w+) \s damage '
                        r'.*initiative \s (?P<initiative>\d+) '
                        r'$', re.VERBOSE)


def log(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


@dataclass
class UnitGroup(object):
    unit_count: int
    hit_points: int
    dam_points: int
    dam_type: str
    initiative: int
    id: int = 0
    trait: str = ''
    immunities: Set[str] = None
    weaknesses: Set[str] = None
    under_attack: bool = False
    _target: Union[UnitGroup, None] = None
    _boost: int = 0

    @property
    def boost(self):
        return self._boost

    @boost.setter
    def boost(self, value: int):
        self._boost = value

    @property
    def effective_power(self) -> int:
        return self.unit_count * (self.dam_points + self.boost)

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
            dam = self.damage_imparted(self.target)
            kills = min(dam // self.target.hit_points, self.target.unit_count)
            log(f'{self.trait} group {self.id} attacks defending group {self.target.id}, '
                f'killing {kills} units, leaving {max(0, self.target.unit_count - kills)} units')
            self.target.unit_count = max(0, self.target.unit_count - kills)
            return kills
        return 0


class Armies(object):
    def __init__(self, trait: str):
        self.groups: List[UnitGroup] = []
        self.trait: str = trait

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
            unit.id = len(self.groups)
            unit.trait = self.trait
        return self

    def show(self) -> Armies:
        if DEBUG:
            print(f'{self.trait}:')
            for unit in sorted(self.groups, key=lambda x: (x.unit_count, x.initiative)):
                print(
                    f'Group {unit.id} contains {unit.unit_count} unit{"s" if unit.unit_count != 1 else ""} '
                    f'(init: {unit.initiative})')
        return self

    def find_defender(self, attacker: UnitGroup) -> UnitGroup:
        defenders = [u for u in self.groups if not u.under_attack]
        best_match = []
        highest = 1
        for defender in defenders:
            damage = attacker.damage_imparted(defender)
            if damage == highest:
                best_match.append(defender)
            elif damage > highest:
                best_match.clear()
                best_match.append(defender)
                highest = damage
            log(f'{attacker.trait} group {attacker.id} would deal '
                f'{defender.trait} group {defender.id} {damage} damage '
                f'[Effective power:Init - {defender.effective_power}:{defender.initiative}]')
        if len(best_match) == 0:
            best_match = None
        elif len(best_match) == 1:
            best_match = best_match[0]
        else:
            best_match = max(best_match, key=lambda x: (x.effective_power, x.initiative))
        log(f'==> {attacker.trait} group {attacker.id} will attack defender '
            f'{best_match.id if (best_match is not None) else "none"}')
        return best_match

    @property
    def count(self) -> int:
        return len(self.groups)

    @property
    def unit_count(self) -> int:
        return sum(unit.unit_count for unit in self.groups)

    @property
    def targeting_order(self) -> List[UnitGroup]:
        return sorted(self.groups, key=lambda x: (x.effective_power, x.initiative), reverse=True)

    def boost(self, boost):
        for unit in self.groups:
            unit.boost = boost


def parse_line(line: str) -> Union[UnitGroup, None]:
    match = LINE_PARSE.match(line)
    if match is None:
        return None
    units = int(match.group('units'))
    hit_points = int(match.group('hp'))
    dam_points = int(match.group('dp'))
    dam_type = match.group('damtype')
    initiative = int(match.group('initiative'))
    modifiers = match.group('weakness') or ''
    immunities = set()
    weaknesses = set()
    for modifier in modifiers.split('; '):
        if modifier.startswith('immune to '):
            immunities |= set(modifier[len('immune to '):].split(', '))
        elif modifier.startswith('weak to '):
            weaknesses |= set(modifier[len('weak to '):].split(', '))
    return UnitGroup(unit_count=units, hit_points=hit_points, dam_points=dam_points, dam_type=dam_type,
                     initiative=initiative, immunities=immunities, weaknesses=weaknesses)


def war(immune: Armies, infection: Armies):
    while immune.count > 0 and infection.count > 0:
        made_a_kill = False
        log('Targeting:')
        for unit in infection.targeting_order:
            unit.target = immune.find_defender(unit)
        for unit in immune.targeting_order:
            unit.target = infection.find_defender(unit)
        log('Attacking:')
        attack_sequence = sorted(immune.groups + infection.groups, key=lambda x: (-x.initiative))
        for unit in attack_sequence:
            if unit.attack() > 0:
                made_a_kill = True
        log('')
        if not made_a_kill:
            log(f'Bail on stuck {immune.unit_count, infection.unit_count}')
            break
        immune.reset_attacks().show()
        infection.reset_attacks().show()
    return immune.unit_count, infection.unit_count


def immune_system_simulator_20xx(inp, boost_immune=False):
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
    if boost_immune:
        boost = 1
        while True:
            im_copy = deepcopy(immune)
            im_copy.boost(boost)
            in_copy = deepcopy(infection)
            result = war(im_copy, in_copy)
            log(f'Boost {boost} -> {result}')
            if result[1] == 0:
                return result[0]
            boost += 1
    else:
        return max(war(immune, infection))


if __name__ == '__main__':
    if DEBUG:
        rules = """Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
""".splitlines(keepends=False)
        print(f'Test data: {immune_system_simulator_20xx(rules, True)}')
    else:
        with open('input.txt') as rule_file:
            rules = rule_file.read().splitlines(keepends=False)
            print(f'Day 24, part 1: {immune_system_simulator_20xx(rules)}')
            print(f'Day 24, part 2: {immune_system_simulator_20xx(rules, True)}')
            # Day 24, part 1: 21199
            # Day 24, part 2: 5761
