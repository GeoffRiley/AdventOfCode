from typing import List, Tuple

NORTH = 1 + 0j
EAST = 0 + 1j
SOUTH = -1 + 0j
WEST = 0 - 1j

VECTOR = {
    'N': NORTH,
    'S': SOUTH,
    'E': EAST,
    'W': WEST,
}

ROTATIONS = {
    NORTH: (NORTH, WEST, SOUTH, EAST),
    WEST: (WEST, SOUTH, EAST, NORTH),
    SOUTH: (SOUTH, EAST, NORTH, WEST),
    EAST: (EAST, NORTH, WEST, SOUTH),
}


def complex_to_manhattan(complex_number: complex) -> int:
    return int(abs(complex_number.real)) + int(abs(complex_number.imag))


def parse_directions(data: str) -> List[Tuple[str, int]]:
    return [(line[0], int(line[1:])) for line in data.splitlines(keepends=False)]


def rain_risk_part1(data: str) -> int:
    directions = parse_directions(data)
    curr_dir = EAST
    curr_pos = 0 + 0j
    for instruction, distance in directions:
        if instruction in 'LR':
            rotation = ROTATIONS[curr_dir]
            if instruction == 'R':
                distance = 360 - distance
            curr_dir = rotation[distance // 90]
        elif instruction == 'F':
            curr_pos += curr_dir * distance
        else:
            curr_pos += VECTOR[instruction] * distance

    return complex_to_manhattan(curr_pos)


def rain_risk_part2(data: str) -> int:
    directions = parse_directions(data)
    waypoint = 1 * NORTH + 10 * EAST
    curr_pos = 0 + 0j
    for instruction, distance in directions:
        if instruction in 'LR':
            if instruction == 'R':
                distance = 360 - distance
            x, y = waypoint.real, waypoint.imag
            waypoint = ((x + y * 1j), (y - x * 1j), (-x - y * 1j), (-y + x * 1j))[distance // 90]
        elif instruction == 'F':
            curr_pos += distance * waypoint
        else:
            waypoint += VECTOR[instruction] * distance

    return complex_to_manhattan(curr_pos)


if __name__ == '__main__':
    test_text = """F10
N3
F7
R90
F11"""
    assert rain_risk_part1(test_text) == 25
    assert rain_risk_part2(test_text) == 286

    with open('input.txt') as in_file:
        in_text = in_file.read()
        part1 = rain_risk_part1(in_text)
        print(f'Part1: {part1}')
        part2 = rain_risk_part2(in_text)
        print(f'Part2: {part2}')

    # Part1: 1710
    # Part2: 62045
