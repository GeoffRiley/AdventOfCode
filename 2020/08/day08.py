from typing import Tuple, List


def parse_instruction(line: str) -> Tuple[str, int]:
    params = line.split()
    return params[0], int(params[1])


def run_code(code: List[str]) -> Tuple[int, bool]:
    ip = 0
    acc = 0
    history = set()
    code_end = len(code)
    while ip not in history and ip < code_end:
        history.add(ip)
        inst, op = parse_instruction(code[ip])
        if inst == 'acc':
            acc += op
        elif inst == 'jmp':
            ip += op
            continue
        elif inst == 'nop':
            pass
        ip += 1
    return acc, ip >= code_end


def handheld_halting_part1(data: str) -> int:
    code = data.splitlines(keepends=False)
    return run_code(code)[0]


def handheld_halting_part2(data: str) -> int:
    code = data.splitlines(keepends=False)
    swapsies = {'nop': 'jmp', 'jmp': 'nop'}
    for n in range(len(code)):
        old_line = code[n]
        inst, op = parse_instruction(old_line)
        if inst not in swapsies:
            continue
        code[n] = f'{swapsies[inst]} {op}'
        acc, flag = run_code(code)
        code[n] = old_line
        if flag:
            return acc


if __name__ == '__main__':
    test_text = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""
    assert handheld_halting_part1(test_text) == 5
    assert handheld_halting_part2(test_text) == 8

    with open('input.txt') as in_file:
        in_text = in_file.read()
        part1 = handheld_halting_part1(in_text)
        print(f'Part1: {part1}')
        part2 = handheld_halting_part2(in_text)
        print(f'Part2: {part2}')

    # Part1: 1553
    # Part2: 1877
