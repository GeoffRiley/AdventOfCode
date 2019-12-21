# Sugar: capacity 3, durability 0, flavor 0, texture -3, calories 2
# Sprinkles: capacity -3, durability 3, flavor 0, texture 0, calories 9
# Candy: capacity -1, durability 0, flavor 4, texture 0, calories 1
# Chocolate: capacity 0, durability 0, flavor -2, texture 2, calories 8
import re
from collections import namedtuple

matcher = re.compile(r'^(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)')

Ingredients = namedtuple('Ingredients', 'capacity, durability, flavor, texture, calories')


def create_a_cookie(ingredients_text: str, max_cals: int = None) -> int:
    ingredients = []
    for line in ingredients_text.splitlines(keepends=False):
        sel = matcher.match(line)
        if sel is None:
            raise TypeError(f'Unrecognised ingredient {line}')
        grps = sel.groups()
        ingredients.append(Ingredients(int(grps[1]), int(grps[2]), int(grps[3]), int(grps[4]), int(grps[5])))

    tot = 0
    for a in range(101):
        for b in range(101 - a):
            for c in range(101 - a - b):
                d = 100 - a - b - c
                cap = max(0,
                          a * ingredients[0].capacity + b * ingredients[1].capacity + c * ingredients[2].capacity + d *
                          ingredients[3].capacity)
                dur = max(0, a * ingredients[0].durability + b * ingredients[1].durability + c * ingredients[
                    2].durability + d * ingredients[3].durability)
                fla = max(0, a * ingredients[0].flavor + b * ingredients[1].flavor + c * ingredients[2].flavor + d *
                          ingredients[3].flavor)
                tex = max(0, a * ingredients[0].texture + b * ingredients[1].texture + c * ingredients[2].texture + d *
                          ingredients[3].texture)
                cal = max(0,
                          a * ingredients[0].calories + b * ingredients[1].calories + c * ingredients[2].calories + d *
                          ingredients[3].calories)
                if max_cals is None or cal == max_cals:
                    new_tot = cap * dur * fla * tex
                    tot = max(tot, new_tot)

    return tot


if __name__ == '__main__':
    with open('input') as f:
        ings = f.read()
    print(f'Part 1: {create_a_cookie(ings)}')
    # Part 1: 222870
    print(f'Part 2: {create_a_cookie(ings, max_cals=500)}')
