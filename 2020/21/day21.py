from typing import List, Set, Tuple, Dict


def sort_out_ingredients(data: str) -> Tuple[List[List[List[str]]], dict, Set[str]]:
    recipes: List[List[List[str]]] = [[j.split()
                                       for j in i.strip(')').replace(',', '').split(' (contains ')]
                                      for i in data.splitlines(keepends=False)]
    ingredients: Set[str] = {_i for i, _ in recipes for _i in i}
    allergens: Set[str] = {_a for _, a in recipes for _a in a}
    allergy: Dict[str, Set[str]] = {
        a: ingredients.intersection(
            *[set(i)
              for i, _a in recipes if a in _a
              ]
        ) for a in allergens
    }
    dangerous_ingredients: Set[str] = {a for _a in allergy for a in allergy[_a]}
    safe_ingredients: Set[str] = ingredients.difference(dangerous_ingredients)
    return recipes, allergy, safe_ingredients


def allergen_assessment_part1(data: str) -> int:
    recipes: List[List[List[str]]]
    safe_ingredients: Set[str]
    recipes, _, safe_ingredients = sort_out_ingredients(data)
    return sum(1 for i in safe_ingredients for _i, a in recipes if i in _i)


def allergen_assessment_part2(data: str) -> str:
    recipes, allergy, _ = sort_out_ingredients(data)
    result = dict()
    while len(allergy) > 0:
        old_allergy = allergy.copy()
        for a in old_allergy:
            allergy[a] = allergy[a].difference(result.keys())
            if len(allergy[a]) == 1:
                result[allergy[a].pop()] = a
                del allergy[a]
    return ','.join(sorted(result.keys(), key=lambda x: result[x]))


if __name__ == '__main__':
    test_text = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""
    assert allergen_assessment_part1(test_text) == 5
    assert allergen_assessment_part2(test_text) == 'mxmxvkd,sqjhc,fvjkl'

    with open('input.txt') as in_file:
        in_text = in_file.read()
        part1 = allergen_assessment_part1(in_text)
        print(f'Part1: {part1}')
        part2 = allergen_assessment_part2(in_text)
        print(f'Part2: {part2}')

    # Part1: 1685
    # Part2: ntft,nhx,kfxr,xmhsbd,rrjb,xzhxj,chbtp,cqvc
