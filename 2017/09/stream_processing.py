from typing import Union


def scrub(stream: str, part1=True) -> Union[str, int]:
    clean = ''
    ignore = 0
    in_garbage = False
    garbage_count = 0
    for c in stream:
        if ignore > 0:
            ignore -= 1
            continue
        if c == '!':
            ignore = 1
            continue
        if in_garbage:
            if c == '>':
                in_garbage = False
            else:
                garbage_count += 1
            continue
        if c == '<':
            in_garbage = True
            continue
        clean += c
    if part1:
        return clean
    else:
        return garbage_count


def stream_processing(inp):
    total = 0
    clean = scrub(inp)
    depth = 0
    for c in clean:
        if c == '{':
            depth += 1
            total += depth
            continue
        if c == '}':
            depth -= 1
    return total


if __name__ == '__main__':
    assert scrub('<>') == ''
    assert scrub('<random characters>') == ''
    assert scrub('<<<<>') == ''
    assert scrub('<{!>}>') == ''
    assert scrub('<!!>') == ''
    assert scrub('<!!!>>') == ''
    assert scrub('<{o"i!a,<{i<a>') == ''
    assert scrub('{<>}') == '{}'
    assert scrub('{<{},{},{{}}>}') == '{}'
    assert scrub('{{<!>},{<!>},{<!>},{<a>}}') == '{{}}'

    assert scrub('<>', False) == 0
    assert scrub('<random characters>', False) == 17
    assert scrub('<<<<>', False) == 3
    assert scrub('<{!>}>', False) == 2
    assert scrub('<!!>', False) == 0
    assert scrub('<!!!>>', False) == 0
    assert scrub('<{o"i!a,<{i<a>', False) == 10

    with open('input.txt') as stream_file:
        stream_string = stream_file.read().strip()
        print(f'Day 9, part 1: {stream_processing(stream_string)}')
        print(f'Day 9, part 2: {scrub(stream_string, False)}')
        # Day 9, part 1: 10616
        # Day 9, part 2: 5101
