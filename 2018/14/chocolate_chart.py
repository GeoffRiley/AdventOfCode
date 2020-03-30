from collections import deque
from itertools import islice


def chocolate_chart_part_1(inp):
    recipes = deque([3, 7])
    elf = [0, 1]
    while len(recipes) < inp + 10:
        old_recipes = [recipes[elf[0]], recipes[elf[1]]]
        new_recipe = old_recipes[0] + old_recipes[1]
        recipes.extend(map(int, [c for c in str(new_recipe).strip()]))
        elf = [(i + j + 1) % len(recipes) for i, j in zip(elf, old_recipes)]
    return ''.join(map(str, islice(recipes, inp, inp + 10)))


def chocolate_chart_part_2(inp):
    recipes = '37'
    elf = [0, 1]
    while inp not in recipes[-8:]:
        old_recipes = [int(recipes[elf[0]]), int(recipes[elf[1]])]
        new_recipe = old_recipes[0] + old_recipes[1]
        recipes += str(new_recipe).strip()
        elf[0] = (elf[0] + old_recipes[0] + 1) % len(recipes)
        elf[1] = (elf[1] + old_recipes[1] + 1) % len(recipes)
        # elf = [(i + j + 1) % len(recipes) for i, j in zip(elf, old_recipes)]
    return recipes.index(inp)


if __name__ == '__main__':
    # print(f'Day 14, part 1: {chocolate_chart_part_1(77201)}')
    print(f'Day 14, part 2: {chocolate_chart_part_2("077201")}')
    # Day 14, part 1: 9211134315
    # Day 14, part 2: 20357548
