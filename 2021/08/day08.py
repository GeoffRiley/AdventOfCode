"""
Advent of code 2021
Day 8: Seven Segment Search
"""
from collections import defaultdict, Counter
from typing import List, Tuple

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list

# Map the string of segments to the value of digit they represent.
SEGMENT_DIGIT = {
    'abcdefg': 8,
    'abcdfg': 9,
    'abcefg': 0,
    'abdefg': 6,
    'abdfg': 5,
    'acdeg': 2,
    'acdfg': 3,
    'acf': 7,
    'bcdf': 4,
    'cf': 1,
}

# Map the number of segment repeats in a signal to one or more definite
# segments.  Two instances cannot unique map to a single segment and
# need additional processing to finalise the true identification.
SIGNAL_SEG_COUNT_SEGS = {
    4: 'e',
    6: 'b',
    7: 'dg',
    8: 'ac',
    9: 'f',
}


def part1(lines: List[Tuple[List[str], List[str]]]):
    """For this part we're only interested in checking how many
        of the output representations have a length of 2, 3, 4 or 7
        characters. (These uniquely represent the digits '1', '7', '4'
        and '8' respectively.)
    """
    return sum(len(x) in [2, 3, 4, 7] for _, out in lines for x in out)


def get_mapping(signals: List[str]) -> dict:
    """Given the set of signals we need to find a way to map the wiring
        from the mangled segments to the correct ones.
    """
    # Start off making a count up of the individual segments
    counts = Counter()
    for x in signals:
        counts.update(x)

    # Using these counts we can make initial assignments for target mappings
    mp = defaultdict(str)
    for k, v in counts.items():
        mp[SIGNAL_SEG_COUNT_SEGS[v]] += k

    # sort out (a,c): seg 'a' is never on for the digit 1, two element entry
    ac = mp['ac']
    mp['a'], mp['c'] = ac if ac[0] not in signals[0] else reversed(ac)
    del mp['ac']

    # sort out (d,g): seg 'g' is never on for the digit 4, four element entry
    dg = mp['dg']
    mp['d'], mp['g'] = dg if dg[0] in signals[2] else reversed(dg)
    del mp['dg']

    # At this stage we have a dictionary mapping the good segments to the
    # mangled one; to make the translation table we need to swap them around.
    return str.maketrans({v: k for k, v in mp.items()})


def part2(lines: List[Tuple[List[str], List[str]]]):
    """For each line we can use the signal values to deduce the
        translation map to be used on the output digits.
        The output digits can then be translated to their
        appropriate 7-segment representations ready to be
        totalled up.
    """
    total = 0
    for signal, output in lines:
        translation_map = get_mapping(signal)
        digits = list(''.join(sorted(s.translate(translation_map))) for s in output)
        v = 0
        for d in digits:
            v = v * 10 + SEGMENT_DIGIT[d]
        total += v

    return total


def standardise(arr: List[str], *, sort: bool = False) -> List[str]:
    new_arr = []
    for e in arr:
        new_arr.append(''.join(sorted(e)))
    if sort:
        return sorted(new_arr, key=len)
    else:
        return new_arr


def main():
    loader = LoaderLib(2021)
    input_text = loader.get_aoc_input(8)
    # input_text = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
    # edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
    # fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
    # fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
    # aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
    # fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
    # dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
    # bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
    # egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
    # gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""

    # Each line splits into two parts, the first part can be sorted into
    # increasing lengths, whilst the second part represents actual digits and
    # must not be reordered.
    # In both parts the individual characters may be sorted though.
    lines = [(standardise(data[0].split(), sort=True), standardise(data[1].split()))
             for data in [line.split('|') for line in lines_to_list(input_text)]]

    # assert len(lines) == len(...)
    loader.print_solution('setup', f'{len(lines)} ...')
    loader.print_solution(1, part1(lines))
    loader.print_solution(2, part2(lines))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.010098        |        0.010098 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 200 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.000656        |        0.010754 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 381
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.013525        |        0.024280 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 1023686
    # --------------------------------------------------------------------------------
