from collections import defaultdict

direction_offsets = {
    'nw': (-1, +1),
    'ne': (0, +1),
    'sw': (0, -1),
    'se': (+1, -1),
    'w': (-1, 0),
    'e': (1, 0),
}


def create_grid(data):
    lines = data.splitlines(keepends=False)
    directions = ['nw', 'ne', 'sw', 'se', 'w', 'e']
    grid = defaultdict(int)
    # line_table = []
    for line in lines:
        # line_directions = []
        working_line = line
        location = (0, 0)
        while working_line:
            for d in directions:
                if working_line.startswith(d):
                    location = (location[0] + direction_offsets[d][0], location[1] + direction_offsets[d][1])
                    # line_directions.append(d)
                    working_line = working_line[len(d):]
                    break
        # assert line == ''.join(line_directions)
        # line_table.append(line_directions)
        grid[location] += 1
    return grid


def lobby_layout_part1(data: str) -> int:
    grid = create_grid(data)
    return sum(g % 2 for g in grid.values())


def lobby_layout_part2(data: str) -> int:
    grid = create_grid(data)
    black_tiles = {k for k, v in grid.items() if v % 2}
    for _ in range(100):
        next_tiles = defaultdict(int)
        new_black_tiles = set()
        for tile in black_tiles:
            for direction in direction_offsets.values():
                next_tiles[(direction[0] + tile[0], direction[1] + tile[1])] += 1
        for tile, count in next_tiles.items():
            if count == 2 or (count == 1 and tile in black_tiles):
                new_black_tiles.add(tile)
        black_tiles = new_black_tiles

    return len(black_tiles)


if __name__ == '__main__':
    test_text = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""
    assert lobby_layout_part1(test_text) == 10
    assert lobby_layout_part2(test_text) == 2208

    with open('input.txt') as in_file:
        in_text = in_file.read()
        part1 = lobby_layout_part1(in_text)
        print(f'Part1: {part1}')
        part2 = lobby_layout_part2(in_text)
        print(f'Part2: {part2}')
