from collections import defaultdict


def build_coords(lines):
    coords = set()
    max_r = max_c = 0
    for line in lines:
        r, c = map(int, line.split(", "))
        coords.add((r, c))
        max_r = max(max_r, r)
        max_c = max(max_c, c)
    return coords, max_c, max_r


def chronal_coordinates_part_1(inp):
    coords, max_c, max_r = build_coords(inp)
    coord_id_to_point = {coord_id: point for coord_id, point in enumerate(coords, start=1)}
    region_sizes = defaultdict(int)
    infinite_ids = set()
    for i in range(max_r + 1):
        for j in range(max_c + 1):
            min_dists = sorted([(abs(r - i) + abs(c - j), coord_id) for coord_id, (r, c) in coord_id_to_point.items()])

            if len(min_dists) == 1 or min_dists[0][0] != min_dists[1][0]:
                coord_id = min_dists[0][1]
                region_sizes[coord_id] += 1

                if i == 0 or i == max_r or j == 0 or j == max_c:
                    infinite_ids.add(coord_id)

    return max(size for coord_id, size in region_sizes.items() if coord_id not in infinite_ids)


def chronal_coordinates_part_2(inp, manhattan_limit):
    coords, max_c, max_r = build_coords(inp)
    size_shared_region = 0
    for i in range(max_r + 1):
        for j in range(max_c + 1):
            size_shared_region += int(sum(abs(r - i) + abs(c - j) for r, c in coords) < manhattan_limit)

    return size_shared_region


if __name__ == '__main__':
    with open('input.txt') as coords_file:
        coords_list = coords_file.read().splitlines(keepends=False)
        print(f'Day 6, part 1: {chronal_coordinates_part_1(coords_list)}')
        print(f'Day 6, part 2: {chronal_coordinates_part_2(coords_list, 10000)}')
        # Day 6, part 1: 5035
        # Day 6, part 2: 35294
