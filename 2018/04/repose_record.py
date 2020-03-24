import re

# [1518-05-18 00:01] Guard #1171 begins shift
from collections import defaultdict

LINE_RE = re.compile(r'^ \[ (?P<date> \d+ - \d+ - \d+ ) \s'
                     r'(?P<hour> \d+ ) : (?P<minute> \d+ ) \] \s'
                     r'(?P<note> .+ ) $', re.VERBOSE)


def make_guard_list(inp):
    lines = sorted(inp)
    current_guard = 0
    sleep_start = None
    sleep_end = None
    guards = defaultdict(lambda: defaultdict(int))
    for line in lines:
        res = LINE_RE.match(line)
        note = res.group('note')
        if note.startswith('Guard '):
            current_guard = int(note[7:].split()[0])
        elif note.startswith('falls '):
            sleep_start = int(res.group('minute'))
        elif note.startswith('wakes '):
            if sleep_start is None:
                print(f'wake without sleep at {res.group("date")} {res.group("hour")}:{res.group("minute")}')
                continue
            sleep_end = int(res.group('minute'))
            for minute in range(sleep_start, sleep_end):
                guards[current_guard][minute] += 1
        else:
            print(f'Unrecognised input line: {line}')
    return guards


def repose_record_part_1(inp):
    guards = make_guard_list(inp)
    sleepiest_guards = sorted(guards.items(), key=lambda x: -sum(x[1].values()))[0]
    return max(sleepiest_guards[1], key=lambda x: sleepiest_guards[1][x]) * sleepiest_guards[0]


def repose_record_part_2(inp):
    guards = make_guard_list(inp)
    sleepiest_guards = sorted(guards.items(), key=lambda x: -max(x[1].values()))[0]
    return max(sleepiest_guards[1], key=lambda x: sleepiest_guards[1][x]) * sleepiest_guards[0]


if __name__ == '__main__':
    with open('input.txt') as repose_file:
        repose_strings = repose_file.read().splitlines(keepends=False)
        print(f'Day 4, part 1: {repose_record_part_1(repose_strings)}')
        print(f'Day 4, part 2: {repose_record_part_2(repose_strings)}')
        # Day 4, part 1: 106710
        # Day 4, part 2: 10491
