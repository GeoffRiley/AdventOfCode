"""
Advent of code 2021
Day 14: Extended Polymerization
"""
from collections import Counter

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


def part1(template: str, insertions: dict):
    """For part 1 plain string expansion can be used; each pass builds a longer
        string, rapidly increasing by len(n(x+1)) <- (len(n(x))*2 - 1)
    """
    for _ in range(10):
        new_template = template[0]
        for a, b in zip(template[:-1], template[1:]):
            new_template += insertions.get(a + b, '') + b
        template = new_template

    counts = Counter(template)
    return counts.most_common()[0][1] - counts.most_common()[-1][1]


def part2(template: str, insertions: dict):
    """Part 2 cannot possibly work in the same way as part 1, the increasing
        length of string quickly reaches a point where memory management gets
        to be the controlling factor.
        Instead, we know that there are a fixed number of permutations of the
        string pairs; each string pair combines to make two new string pairs
        in a predictable manner. Due to this we can just keep a count of how
        many of each pair is being used, finally totalling the first part of
        each pair will give an overall use of all the letters—except for the
        final letter that needs to be accounted for separately.
        [Totally just first part of each pair because the second part is
        repeated by the following pair as its first part!]
    """
    counts = Counter(a + b for a, b in zip(template[:-1], template[1:]))

    for _ in range(40):
        new_count = Counter()
        for ab, cnt in counts.items():
            a, c = list(ab)
            b = insertions[ab]
            new_count[a + b] += cnt
            new_count[b + c] += cnt

        counts = new_count

    letter_count = Counter()
    for ab, cnt in counts.items():
        letter_count[ab[0]] += cnt
    letter_count[template[-1]] += 1

    return letter_count.most_common()[0][1] - letter_count.most_common()[-1][1]


def main():
    loader = LoaderLib(2021)
    input_text = loader.get_aoc_input(14)

    #     input_text = """NNCB
    #
    # CH -> B
    # HH -> N
    # CB -> H
    # NH -> C
    # HB -> C
    # HC -> B
    # HN -> C
    # NN -> C
    # BH -> H
    # NC -> B
    # NB -> B
    # BN -> B
    # BB -> N
    # BC -> B
    # CC -> N
    # CN -> C"""

    template, _, *lines = lines_to_list(input_text)

    insertions = dict()
    for line in lines:
        k, v = line.split(' -> ')
        insertions[k] = v

    loader.print_solution('setup', f'template: {template}, # of rule lines: {len(lines)}')
    loader.print_solution(1, part1(template, insertions))
    loader.print_solution(2, part2(template, insertions))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.005058        |        0.005058 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : template: VHCKBFOVCHHKOHBPNCKO, # of rule lines: 100
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.023598        |        0.028655 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 2587
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.010197        |        0.038853 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 3318837563123
    # --------------------------------------------------------------------------------
