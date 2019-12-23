from collections import namedtuple
from itertools import combinations

ShopProduct = namedtuple('ShopProduct', 'name, cost, damage, armor')

Weapons = [  # Name Cost  Damage  Armor
    ShopProduct('Dagger', 8, 4, 0),
    ShopProduct('Shortsword', 10, 5, 0),
    ShopProduct('Warhammer', 25, 6, 0),
    ShopProduct('Longsword', 40, 7, 0),
    ShopProduct('Greataxe', 74, 8, 0),
]
Armor = [  # Name Cost  Damage  Armor
    ShopProduct('Leather', 13, 0, 1),
    ShopProduct('Chainmail', 31, 0, 2),
    ShopProduct('Splintmail', 53, 0, 3),
    ShopProduct('Bandedmail', 75, 0, 4),
    ShopProduct('Platemail', 102, 0, 5),
    ShopProduct('No armor', 0, 0, 0),
]
Rings = [  # Name Cost  Damage  Armor
    ShopProduct('Damage +1', 25, 1, 0),
    ShopProduct('Damage +2', 50, 2, 0),
    ShopProduct('Damage +3', 100, 3, 0),
    ShopProduct('No dam ring', 0, 0, 0),
    ShopProduct('Defense +1', 20, 0, 1),
    ShopProduct('Defense +2', 40, 0, 2),
    ShopProduct('Defense +3', 80, 0, 3),
    ShopProduct('No def ring', 0, 0, 0),
]

PlayerStat = namedtuple('PlayerStat', 'hp, damage, armor')

with open('input') as f:
    boss_stat_text = f.read().splitlines(keepends=False)

hp = damage = armor = 0
for stat in boss_stat_text:
    title, value = stat.split(': ')
    if title.startswith('Hit'):
        hp = int(value)
    elif title.startswith('Dam'):
        damage = int(value)
    elif title.startswith('Arm'):
        armor = int(value)
    else:
        raise TypeError(f'Unknown stat type ({title})')

boss_stat = PlayerStat(hp, damage, armor)
my_hp = 100


def simulate(player_stat: PlayerStat) -> bool:
    b = boss_stat.hp
    p = player_stat.hp
    while True:
        b -= max(player_stat.damage - boss_stat.armor, 1)
        if b <= 0:
            return True
        p -= max(boss_stat.damage - player_stat.armor, 1)
        if p <= 0:
            return False


min_cost = 1e30
min_setup = []
for weapon in Weapons:
    for armor in Armor:
        for ring1, ring2 in combinations(Rings, 2):
            cost = weapon.cost + armor.cost + ring1.cost + ring2.cost
            dam = weapon.damage + armor.damage + ring1.damage + ring2.damage
            arm = weapon.armor + armor.armor + ring1.armor + ring2.armor
            if simulate(PlayerStat(my_hp, dam, arm)):
                min_cost = min(min_cost, cost)
print(f'Part 1: {min_cost}')

max_cost = -1e30
max_setup = []
for weapon in Weapons:
    for armor in Armor:
        for ring1, ring2 in combinations(Rings, 2):
            cost = weapon.cost + armor.cost + ring1.cost + ring2.cost
            dam = weapon.damage + armor.damage + ring1.damage + ring2.damage
            arm = weapon.armor + armor.armor + ring1.armor + ring2.armor
            if not simulate(PlayerStat(my_hp, dam, arm)):
                max_cost = max(max_cost, cost)
print(f'Part 2: {max_cost}')
