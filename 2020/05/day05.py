BIN_TRANS = ''.maketrans('FBLR', '0101')


def binary_decode(pss: str) -> int:
    return int(pss.translate(BIN_TRANS), 2)


def binary_boarding_part1(data: str) -> int:
    passes = data.splitlines(keepends=False)
    max_seat_number = 0
    for pss in passes:
        seat = binary_decode(pss)
        if seat > max_seat_number:
            max_seat_number = seat
    return max_seat_number


def binary_boarding_part2(data: str) -> int:
    seat_ids = set(map(binary_decode, data.splitlines(keepends=False)))
    seat_list = set(n for n in range(min(seat_ids), max(seat_ids) + 1))
    remaining_seats = seat_list - seat_ids
    for seat in remaining_seats:
        if seat + 1 not in remaining_seats:
            return seat
    raise ValueError('No seat found')


if __name__ == '__main__':
    assert binary_decode('FBFBBFFRLR') == 357
    assert binary_decode('BFFFBBFRRR') == 567
    assert binary_decode('FFFBBBFRRR') == 119
    assert binary_decode('BBFFBBFRLL') == 820
    example_data = '''FBFBBFFRLR
BFFFBBFRRR
FFFBBBFRRR
BBFFBBFRLL'''
    assert binary_boarding_part1(example_data) == 820

    with open('input.txt') as in_file:
        in_text = in_file.read()
        part1 = binary_boarding_part1(in_text)
        print(f'Part1: {part1}')
        part2 = binary_boarding_part2(in_text)
        print(f'Part2: {part2}')

    # Part1: 813
    # Part2: 612
