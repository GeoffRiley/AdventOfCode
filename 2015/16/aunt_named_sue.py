import re


class MFCSAM(object):
    def __init__(self):
        self.sue_number = None
        self.children = None
        self.cats = None
        self.samoyeds = None
        self.pomeranians = None
        self.akitas = None
        self.vizslas = None
        self.goldfish = None
        self.trees = None
        self.cars = None
        self.perfumes = None

    def parse(self, line: str):
        if not line.startswith('Sue '):
            raise TypeError('Not a "Sue" record: ' + line)
        x = re.match(r'Sue (\d+):', line)
        self.sue_number = int(x.group(1))
        line = line[x.end(1) + 2:]

        for entry in line.split(', '):
            nm, vl = entry.split(': ')
            setattr(self, nm, int(vl))

        return self

    def pctg(self, a, b, mod_lt=False, mod_gt=False):
        if mod_lt:
            return 100 if a < b else 0
        if mod_gt:
            return 100 if a > b else 0
        return 100 if a == b else 0
        # return 100  # (a / b * 100) if b > 0 else 0

    def match(self, other: 'MFCSAM', mods=False) -> float:
        sc = 0.0
        if self.children is not None:
            sc += self.pctg(self.children, other.children)
        if self.cats is not None:
            sc += self.pctg(self.cats, other.cats, mod_gt=mods)
        if self.samoyeds is not None:
            sc += self.pctg(self.samoyeds, other.samoyeds)
        if self.pomeranians is not None:
            sc += self.pctg(self.pomeranians, other.pomeranians, mod_lt=mods)
        if self.akitas is not None:
            sc += self.pctg(self.akitas, other.akitas)
        if self.vizslas is not None:
            sc += self.pctg(self.vizslas, other.vizslas)
        if self.goldfish is not None:
            sc += self.pctg(self.goldfish, other.goldfish, mod_lt=mods)
        if self.trees is not None:
            sc += self.pctg(self.trees, other.trees, mod_gt=mods)
        if self.cars is not None:
            sc += self.pctg(self.cars, other.cars)
        if self.perfumes is not None:
            sc += self.pctg(self.perfumes, other.perfumes)
        return sc


if __name__ == '__main__':
    with open('input') as f:
        sue_text = f.read()
    sue_list = [MFCSAM().parse(line) for line in sue_text.splitlines(keepends=False)]
    unknown_sue = MFCSAM().parse(
        'Sue 999: children: 3, cats: 7, samoyeds: 2, pomeranians: 3, akitas: 0, vizslas: 0, goldfish: 5, trees: 3, '
        'cars: 2, perfumes: 1')

    # Scan the sue_list to find matches for unknown_sue...
    best = -1
    best_score = -1
    for sue in sue_list:
        score = sue.match(unknown_sue)
        if score > best_score:
            best = sue.sue_number
            best_score = score

    print(f'Part 1: {best}')

    # Scan the sue_list to find matches for unknown_sue...
    best = -1
    best_score = -1
    for sue in sue_list:
        score = sue.match(unknown_sue, mods=True)
        if score > best_score:
            best = sue.sue_number
            best_score = score

    print(f'Part 2: {best}')
    # Part 1: 103
    # Part 2: 405
