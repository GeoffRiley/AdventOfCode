from collections import namedtuple
from copy import deepcopy

Spell = namedtuple('Spell', 'manacost, dmg, hp, armour, mana, turns, entry')

missile = Spell(53, 4, 0, 0, 0, 0, 0)
drain = Spell(73, 2, 2, 0, 0, 0, 1)
shield = Spell(113, 0, 0, 7, 0, 6, 2)
poison = Spell(173, 3, 0, 0, 0, 6, 3)
recharge = Spell(229, 0, 0, 0, 101, 5, 4)

spells = [missile, drain, shield, poison, recharge]

boss_hp_start = 0
boss_dmg_start = 0
player_hp_start = 50
player_mana_start = 500

with open('input') as f:
    boss_stat_text = f.read().splitlines(keepends=False)

for stat in boss_stat_text:
    title, value = stat.split(': ')
    if title.startswith('Hit'):
        boss_hp_start = int(value)
    elif title.startswith('Dam'):
        boss_dmg_start = int(value)
    else:
        raise TypeError(f'Unknown stat type ({title})')


def sim(boss_hp, player_hp, player_mana, active_spells, player_turn, mana_used, part_two=False):
    global min_mana_used

    bossDmg = boss_dmg_start
    play_armour = 0

    if part_two and player_turn:
        player_hp -= 1
        if player_hp <= 0:
            return False

    new_active_spells = []
    for active_spell in active_spells:
        if active_spell[5] >= 0:  # spell effect applies now
            boss_hp -= active_spell[1]
            player_hp += active_spell[2]
            play_armour += active_spell[3]
            player_mana += active_spell[4]

        new_active_spell = (
            active_spell[0], active_spell[1], active_spell[2], active_spell[3], active_spell[4], active_spell[5] - 1,
            active_spell[6])
        if new_active_spell[5] > 0:  # spell carries over
            new_active_spells.append(new_active_spell)

    if boss_hp <= 0:
        global min_mana_used
        if mana_used < min_mana_used:
            min_mana_used = mana_used
        return True

    if mana_used >= min_mana_used:
        return False

    if player_turn:
        for i in range(len(spells)):
            spell = spells[i]
            spell_already_active = False
            for j in range(len(new_active_spells)):
                if new_active_spells[j][6] == spell[6]:
                    spell_already_active = True
                    break

            spell_mana_cost = spell[0]
            if spell_mana_cost <= player_mana and not spell_already_active:
                a = deepcopy(new_active_spells)
                a.append(spell)
                sim(boss_hp, player_hp, player_mana - spell_mana_cost, a, False, mana_used + spell_mana_cost, part_two)
    else:
        player_hp += play_armour - bossDmg if play_armour - bossDmg < 0 else -1
        if player_hp > 0:
            sim(boss_hp, player_hp, player_mana, new_active_spells, True, mana_used, part_two)


def main():
    global min_mana_used

    min_mana_used = 1e30
    sim(boss_hp_start, player_hp_start, player_mana_start, [], True, 0, False)
    print(f'Part 1: {min_mana_used}')
    min_mana_used = 1e30
    sim(boss_hp_start, player_hp_start, player_mana_start, [], True, 0, True)
    print(f'Part 2: {min_mana_used}')


main()

# Part 1: 900
# Part 2: 1216
