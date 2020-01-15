import re
from itertools import chain

LEVELS = {
    'first': 0,
    'second': 1,
    'third': 2,
    'fourth': 3
}

MAX_BITS = 64

BIT_VALUES = {
    x: (1 << x) for x in range(MAX_BITS)
}

LIFT_BIT = 0
CHIP_BIT = 1
GENERATOR_BIT = 2
LIFT_MASK = BIT_VALUES[LIFT_BIT]
GENERATOR_MASK = sum(BIT_VALUES[x] for x in range(GENERATOR_BIT, MAX_BITS, 2))
CHIP_MASK = sum(BIT_VALUES[x] for x in range(CHIP_BIT, MAX_BITS, 2))


def parse(arrangement: str):
    """
    Accepting a textural description of microchip and generator locations
    this routine will reduce the information into a set of four integers
    returned in a list.

    Return value is a list of four integers representing the contents of
    each of four floors in a bit pattern. For each integer if a bit is set
    then that object is present:

    0b0zzyyxxwwvvuuttL
    Where:
        L: lift location
        tt: first gen and chip location
        uu: second gen and chip location
        vv: third gen and chip location
        ww: fourth gen and chip location
        xx: fifth gen and chip location
        yy: sixth gen and chip location
        zz: seventh gen and chip location
    Each object can only exist on a single floor at any one time.

    :param arrangement: str
    :return: list
    """
    chips = {}
    gens = {}
    names = {}
    for line in arrangement.splitlines(keepends=False):
        floor = re.search(r'The (\w+) floor', line).groups()[0]
        elements = re.findall(r'a (\S+ (?:microchip|generator))', line)
        floor = LEVELS[floor]
        e: str
        for e in elements:
            parts = e.split()
            if parts[-1] == 'microchip':
                # remove the '-compatible'
                chip = parts[0].split('-')[0]
                if chip not in names:
                    names[chip] = max(chain([0], names.values())) + 1
                chips[names[chip]] = floor
            else:
                gen = parts[0]
                if gen not in names:
                    names[gen] = max(chain([0], names.values())) + 1
                gens[names[gen]] = floor

    res = [0, 0, 0, 0]
    # list on floor 0
    res[0] ^= 1
    # go through the chips and put them on the right floor
    for c, f in chips.items():
        res[f] ^= 1 << (c * 2 - 1)
    # go through the gens and put them on the right floor
    for g, f in gens.items():
        res[f] ^= 1 << (g * 2)
    return res


def lifts_assemble(arrange_list: list):
    pass


if __name__ == '__main__':
    with open('input') as f:
        arr = f.read()
    arrange = parse(arr)
    print(f'Part 1: {lifts_assemble(arrange)}')
    # Part 1: 33
    arrange = parse(arr)
    # arrange['first'].extend(['elerium generator',
    #                          'elerium-compatible microchip',
    #                          'dilithium generator',
    #                          'dilithium-compatible microchip'])
    arrange[0] ^= 0b1111 << (6 * 2 - 1)
    print(f'Part 2: {lifts_assemble(arrange)}')
    # Part 2: 57
