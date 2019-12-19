"""
Based upon code from a number of different projects… not necessarily in Python!
"""

from collections import deque
from functools import lru_cache
from string import ascii_lowercase as lowercase, ascii_uppercase as uppercase
from typing import Tuple

BOT = '@'
WALL = '#'

grid = {}
grid_width = 0
grid_height = 0
grid_links = {}
keys = {}
doors = {}
bot_loc: Tuple[int, int] or None = None


def reset():
    global grid, grid_width, grid_height, grid_links, keys, doors

    grid = {}
    grid_width = 0
    grid_height = 0
    grid_links = {}
    keys = {}
    doors = {}


def neighbours(centre_row, centre_col):
    global grid, grid_width, grid_height
    for dir_row, dir_col in ((0, 1), (-1, 0), (0, -1), (1, 0)):
        target_row, target_col = (centre_row + dir_row, centre_col + dir_col)

        if 0 <= target_row < grid_height and 0 <= target_col < grid_width:
            if grid[target_row][target_col] != WALL:
                yield target_row, target_col


def setup_grid(map_text):
    global grid, grid_width, grid_height, bot_loc, keys, doors

    reset()
    grid = [[col_num for col_num in line] for line in map_text.splitlines(keepends=False)]
    grid_height = len(grid)
    grid_width = len(grid[0])
    for row_num, row_data in enumerate(grid):
        for col_num, cell in enumerate(row_data):
            pos = (row_num, col_num)
            if cell != WALL:
                if pos not in grid_links:
                    grid_links[pos] = set()

                for neigh in neighbours(*pos):
                    grid_links[pos].add(neigh)

                if cell in lowercase:
                    keys[cell] = pos
                    keys[pos] = cell
                elif cell in uppercase:
                    doors[cell.lower()] = pos
                    doors[pos] = cell.lower()
                elif cell == BOT:
                    bot_loc = pos


@lru_cache(maxsize=None)
def reachable_keys(start_pos, used_keys):
    # part 1
    global grid_links, keys, doors

    queue = deque([(0, start_pos)])
    visited = set()
    found_keys = {}

    while queue:
        dist, node = queue.popleft()

        if node not in visited:
            visited.add(node)

            if node in keys:
                k = keys[node]

                if k not in used_keys and (k not in found_keys or found_keys[k] > dist):
                    found_keys[k] = dist
                    continue

            if node in doors and not doors[node] in used_keys:
                continue

            for neighbor in filter(lambda n: n not in visited, grid_links[node]):
                new_dist = dist + 1
                queue.append((new_dist, neighbor))

    return found_keys


@lru_cache(maxsize=None)
def search(start_pos=None, used_keys=frozenset()):
    # part 1
    global bot_loc, keys

    if start_pos is None:
        start_pos = bot_loc
    key_targets = reachable_keys(start_pos, used_keys)
    if not key_targets:
        if len(used_keys) == len(keys) // 2:
            return 0
        else:
            return float('inf')

    best = float('inf')

    for k, d in key_targets.items():
        key_pos = keys[k]
        dist = d + search(key_pos, used_keys | {k})

        if dist < best:
            best = dist

    return best


@lru_cache(maxsize=None)
def reachable_keys2(bots, used_keys):
    # part2
    global grid_links, keys, doors

    queue = deque()
    visited = set()
    found_keys = {}

    for bot in bots:
        queue.append((0, bot, bot))

    while queue:
        dist, node, owner = queue.popleft()

        if node not in visited:
            visited.add(node)

            if node in keys:
                k = keys[node]

                if k not in used_keys and (k not in found_keys or found_keys[k] > dist):
                    found_keys[k] = (owner, dist)
                    continue

            if node in doors and not doors[node] in used_keys:
                continue

            for neighbor in filter(lambda n: n not in visited, grid_links[node]):
                queue.append((dist + 1, neighbor, owner))

    return found_keys


@lru_cache(maxsize=None)
def search2(bots, used_keys=frozenset()):
    # part 2
    global keys

    located_keys = reachable_keys2(bots, used_keys)
    if not located_keys:
        if len(used_keys) == len(keys) // 2:
            return 0
        else:
            return float('inf')

    best = float('inf')

    for k, (owner, d) in located_keys.items():
        new_bots = []

        for b in bots:
            if b == owner:
                new_bots.append(keys[k])
            else:
                new_bots.append(b)

        new_bots = tuple(new_bots)
        dist = d + search2(new_bots, used_keys | {k})

        if dist < best:
            best = dist

    return best


def make_map_mods():
    # Modify the map ready for part 2
    # ...           @#@
    # .@.  becomes  ### to divide into quarters
    # ...           @#@
    global grid_links, bot_loc

    del grid_links[bot_loc]
    for neigh in neighbours(*bot_loc):
        del grid_links[neigh]

        for neigh_neigh in neighbours(*neigh):
            if neigh_neigh in grid_links:
                grid_links[neigh_neigh].remove(neigh)


if __name__ == '__main__':
    with open('input') as f:
        plan = f.read()

    setup_grid(plan)

    ans = search(bot_loc)
    print(f'Part 1: {ans}')

    make_map_mods()

    row, col = bot_loc
    part2_bots = (
        (row + 1, col + 1),
        (row + 1, col - 1),
        (row - 1, col + 1),
        (row - 1, col - 1),
    )

    ans2 = search2(part2_bots)

    print(f'Part 2: {ans2}')
