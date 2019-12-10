from collections import defaultdict
from typing import List, Tuple, Any

import numpy as np


def cart2pol(x, y):
    rho = np.hypot(x, y)
    phi = np.arctan2(y, x)
    return rho, phi


def create_map(text_map: str) -> List[list]:
    asteroid_array = []
    for line in text_map.splitlines(keepends=False):
        asteroid_array.append([0 if v == '.' else 1 for v in line])
    return asteroid_array


def visible_list(asteroid_array, y, x):
    angles = defaultdict(list)
    for row in range(len(asteroid_array)):
        for col in range(len(asteroid_array[row])):
            if asteroid_array[row][col] == 1:
                r, ang = cart2pol(col - x, row - y)
                angles[ang].append((r, (col, row)))
    res = []
    for k, v in angles.items():
        sel = v[0]
        for i in v[1:]:
            if i[0] < sel[0]:
                sel = i
        res.append((k, sel[1]))
    return res


def scan_from(asteroid_array, y, x):
    return len(visible_list(asteroid_array, y, x))


def find_best_station(asteroid_array: List[list]):
    findings = ((None, None), 0)
    for row in range(len(asteroid_array)):
        for col in range(len(asteroid_array[row])):
            if asteroid_array[row][col] == 1:
                i = scan_from(asteroid_array, row, col)
                if i > findings[1]:
                    findings = ((col, row), i)
    return findings


def vapourise_asteroids(asteroid_array: List[list], coord: Tuple[int, int]) -> \
        List[Tuple[Tuple[Any, Any], Tuple[int, int]]]:
    src_x, src_y = coord
    # asteroid_coordinate = []
    vapourised = []
    asteroid_array[src_y][src_x] = 2  # identify our station

    done = False
    while not done:
        visible_asteroids = visible_list(asteroid_array, src_y, src_x)
        if len(visible_asteroids) == 0:
            done = True
            continue
        current_angle = np.deg2rad(-90)
        while len(visible_asteroids) > 0:
            minimum_angle = np.deg2rad(360)
            selected = None
            for a in visible_asteroids:
                diff_angle = a[0] - current_angle
                if 0 <= diff_angle < minimum_angle:
                    minimum_angle = diff_angle
                    selected = a
            if selected is None:
                current_angle = np.deg2rad(-180)
            else:
                vapourised.append(selected)
                x, y = selected[1]
                asteroid_array[y][x] = 3
                visible_asteroids.remove(selected)
    return vapourised


if __name__ == '__main__':
    with open('input') as f:
        initial_grid = f.read()
    grid = create_map(initial_grid)
    best_station = find_best_station(grid)
    print(f'PART 1: {best_station[1]}')
    vaped = vapourise_asteroids(grid, best_station[0])
    print(f'PART 2 {vaped[199]}')
