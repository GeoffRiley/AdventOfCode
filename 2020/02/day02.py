from typing import Tuple


def process_line(line: str) -> Tuple[int, int, str, str]:
    parts, pwd = line.split(':')
    rng, letter = parts.split()
    lo, hi = map(int, rng.split('-'))
    return lo, hi, letter, pwd


def verify_passwords_part1(text: str) -> int:
    password_list = map(process_line, text.splitlines(keepends=False))
    result = sum(lo <= pwd.count(letter) <= hi
                 for lo, hi, letter, pwd in password_list)
    return result


def verify_passwords_part2(text: str) -> int:
    password_list = map(process_line, text.splitlines(keepends=False))
    result = sum((pwd[lo] == letter) ^ (pwd[hi] == letter)
                 for lo, hi, letter, pwd in password_list)
    return result


if __name__ == '__main__':
    with open('input.txt') as in_file:
        example = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc"""
        assert verify_passwords_part1(example) == 2
        assert verify_passwords_part2(example) == 1

        original = in_file.read()
        part1 = verify_passwords_part1(original)
        print(f'Part1: {part1}')
        part2 = verify_passwords_part2(original)
        print(f'Part2: {part2}')

        # Part1: 528
        # Part2: 497
