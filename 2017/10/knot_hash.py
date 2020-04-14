from functools import reduce
from operator import xor

STD_SUFFIX = [17, 31, 73, 47, 23]


def knot_hash(inp, array_length=256):
    knot_array = [a for a in range(array_length)]
    knot_lengths = list(map(int, inp.split(',')))
    current_position = 0
    skip_size = 0
    tie_the_knot(array_length, knot_lengths, current_position, skip_size, knot_array)
    return knot_array[0] * knot_array[1]


def knot_hash_str(inp, array_length=256):
    knot_array = [a for a in range(array_length)]
    knot_lengths = list(map(ord, inp)) + STD_SUFFIX
    current_position = 0
    skip_size = 0
    for _ in range(64):
        current_position, skip_size = tie_the_knot(array_length, knot_lengths, current_position, skip_size, knot_array)
    dense_hashes = []
    for i in range(16):
        dense_hashes.append(reduce(xor, knot_array[i * 16:i * 16 + 16]))
    return ''.join([f'{v:02x}' for v in dense_hashes])


def tie_the_knot(array_length, knot_lengths, current_position, skip_size, knot_array):
    for length in knot_lengths:
        slice_end = current_position + length
        if slice_end < array_length:
            knot_array[current_position:slice_end] = reversed(knot_array[current_position:slice_end])
        else:
            work_str = list(reversed(knot_array[current_position:] + knot_array[:slice_end - array_length]))
            slice_mid = array_length - current_position
            knot_array[current_position:] = work_str[:slice_mid]
            knot_array[:slice_end - array_length] = work_str[slice_mid:]

        current_position += length + skip_size
        while current_position > array_length:
            current_position -= array_length
        skip_size += 1
    return current_position, skip_size


if __name__ == '__main__':
    with open('input.txt') as knot_file:
        knot_params = knot_file.read().strip()
        print(f'Day 10, part 1: {knot_hash(knot_params)}')
        print(f'Day 10, part 2: {knot_hash_str(knot_params)}')
        # Day 10, part 1: 15990
        # Day 10, part 2: 90adb097dd55dea8305c900372258ac6
