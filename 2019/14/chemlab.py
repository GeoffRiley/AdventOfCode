from collections import defaultdict
from math import ceil
from typing import List


class Reagent(object):
    @classmethod
    def factory(cls, reagent_str: str):
        res = []
        for r in reagent_str.split(','):
            res.append(cls(r))
        return res

    def __init__(self, chem: str, qty: int = None):
        if qty is None:
            q, c = chem.split()
            self._qty, self._chem = int(q), c
        else:
            self._qty, self._chem = int(qty), chem

    @property
    def chem(self):
        return self._chem

    @property
    def qty(self):
        return self._qty

    def __repr__(self):
        return f'{self.__class__.__name__}({self.chem} * {self.qty})'


class Reactor(dict):
    def __init__(self):
        super().__init__()
        self.requirements = defaultdict(int)


reaction_list = defaultdict(List[Reagent])
reagent_min_order = defaultdict(int)
reagent_stock = defaultdict(int)
reagent_used = defaultdict(int)


def calc_min_ore(chem: str, req_qty: int):
    # first shift existing stock
    if reagent_stock[chem] > 0:
        s = min(reagent_stock[chem], req_qty)
        reagent_stock[chem] -= s
        req_qty -= s
    if req_qty > 0:
        # if we need more, then a full unit or multiple thereof must be requested
        units = ceil(req_qty / reagent_min_order[chem])
        order = reagent_min_order[chem] * units
        reagent_stock[chem] += order - req_qty
        reagent_used[chem] += order
        # get raw materials to cover
        for r in reaction_list[chem]:
            if r.chem == 'ORE':
                reagent_used[r.chem] += r.qty * units
            else:
                calc_min_ore(r.chem, r.qty * units)


def ore_calc(reaction_equ: str, units: int) -> int:
    reagent_stock.clear()
    reagent_used.clear()
    for reaction in reaction_equ.splitlines(keepends=False):
        reagents, produce = reaction.split('=>')
        chem_min_qty, chem_name = produce.split()
        reaction_list[chem_name] = Reagent.factory(reagents)
        reagent_min_order[chem_name] = int(chem_min_qty)
    calc_min_ore('FUEL', units)
    return reagent_used['ORE']


def max_fuel_for_ore(reaction_equ: str, target: int) -> int:
    est_range = [0, 1]
    while ore_calc(reaction_equ, est_range[1]) < target:
        est_range[0] = est_range[1]
        est_range[1] *= 2
    while est_range[0] + 1 < est_range[1]:
        av = sum(est_range) // 2
        if ore_calc(reaction_equ, av) > target:
            est_range[1] = av
        else:
            est_range[0] = av
    return est_range[0]


if __name__ == '__main__':
    with open('input') as f:
        reaction_str = f.read()
    print(f'PART 1: {ore_calc(reaction_str, 1)}')
    print(f'PART 2: {max_fuel_for_ore(reaction_str, 1000000000000)}')

    # PART 1: 1582325
    # PART 2: 2267486
