from itertools import chain, combinations
from typing import Set, List, Iterator, Dict

# Three types of mapping to provide masks of different purposes
# - SET = bits in result to set on; use (mask .or. value)
MAPPING_SET = str.maketrans('X10', '010')
# - RESET = bits in result to clear; use (mask .and. value)
MAPPING_RESET = str.maketrans('X10', '001')
# - FLOAT = bits in result to float; use (mask .eor. value)
#           for each possible combination of floating bits
MAPPING_FLOAT = str.maketrans('X10', '100')


def docking_data_part1(data: str) -> int:
    boot_code: List[Iterator[List[str, str]]] = parse_data(data)
    mem: Dict[int, int] = dict()
    set_mask: int = 0
    reset_mask: int = 0
    for instr, param in boot_code:
        if instr == 'mask':
            set_mask = int(param.translate(MAPPING_SET), 2)
            reset_mask = ~int(param.translate(MAPPING_RESET), 2)
        elif instr.startswith('mem'):
            mem[int(instr[4:-1])] = (int(param) | set_mask) & reset_mask
        else:
            raise SyntaxError(f'Unrecognised instruction: {instr}')

    return sum(mem.values())


def parse_data(data: str) -> List[Iterator[List[str, str]]]:
    return [map(lambda x: x.strip(), line.split(' = '))
            for line in data.strip().splitlines(keepends=False)]


def docking_data_part2(data: str) -> int:
    boot_code: List[Iterator[List[str, str]]] = parse_data(data)
    mem: Dict[int, int] = dict()
    set_mask: int = 0
    float_places: Set[int] = set()
    for instr, param in boot_code:
        if instr == 'mask':
            set_mask = int(param.translate(MAPPING_SET), 2)
            float_mask = int(param.translate(MAPPING_FLOAT), 2)
            float_places = set(j for i in range(36)
                               if (j := 1 << i) & float_mask)
        elif instr.startswith('mem'):
            value = int(param)
            pos = int(instr[4:-1]) | set_mask

            for i in chain.from_iterable(
                    combinations(float_places, length)
                    for length in range(len(float_places) + 1)
            ):
                float_bits = sum(i)
                mem[(pos ^ float_bits)] = value
        else:
            raise SyntaxError(f'Unrecognised instruction: {instr}')

    return sum(mem.values())


if __name__ == '__main__':
    test_text = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""
    assert docking_data_part1(test_text) == 165
    test_text = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""
    assert docking_data_part2(test_text) == 208

    with open('input.txt') as in_file:
        in_text = in_file.read()
        part1 = docking_data_part1(in_text)
        print(f'Part1: {part1}')
        part2 = docking_data_part2(in_text)
        print(f'Part2: {part2}')

    # Part1: 17934269678453
    # Part2: 3440662844064
