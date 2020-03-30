def generate_grid(map_text):
    grid = []
    for y, row in enumerate(map_text):
        grid.append([x for x in row])
        for x, col in enumerate(row):
            if col in 'GE':
                char_tup = (col, 200, False)
                grid[y][x] = char_tup
    return grid


def move_character(grid, from_row, from_col, to_row, to_col, char):
    grid[from_row][from_col] = "."
    grid[to_row][to_col] = (char[0], char[1], True)


def attack(grid, row, col, enemy, damage=3):
    if not adjacent_enemy(grid, row, col, enemy):
        return False

    enemies = {}
    for coords in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]:
        if grid[coords[0]][coords[1]][0] == enemy:
            # enemy is a tuple, (char_type, hp, already_moved_bool)
            enemies[coords] = grid[coords[0]][coords[1]][1]

    # Filter to only the enemies with minimum hp
    min_hp = min(enemies.values())
    enemies = [x for x in enemies if enemies[x] == min_hp]

    # Now we have a list of coordinates, we can sort to get reading order, then take the first to get our enemy
    enemies.sort()
    coords = enemies[0]

    enemy = grid[coords[0]][coords[1]]
    enemy_pts = enemy[1] - damage
    enemy_tup = (enemy[0], enemy_pts, enemy[2])

    # Check for killed
    if enemy_pts <= 0:
        grid[coords[0]][coords[1]] = "."
        return True
    else:
        grid[coords[0]][coords[1]] = enemy_tup
        return False


def adjacent_enemy(grid, row, col, enemy):
    return any(x[0] == enemy for x in [grid[row + 1][col], grid[row - 1][col], grid[row][col + 1], grid[row][col - 1]])


def get_best_move(best_moves):
    if not best_moves:
        return None

    # First condition - fewest number of moves away
    min_steps = min([x[1] for x in best_moves])
    best_moves = [x for x in best_moves if x[1] == min_steps]

    # Second condition - if tie, choose the first tile in reading order
    best_moves.sort(key=lambda x: x[2])
    best_moves = [x for x in best_moves if x[2] == best_moves[0][2]]

    # Third condition - if tie, take the first step in reading order
    best_moves.sort(key=lambda x: x[0])
    best_moves = [x for x in best_moves if x[0] == best_moves[0][0]]

    return best_moves[0][0]


def count_characters(grid):
    seen = {"G": 0, "E": 0}
    for row in grid:
        for col in row:
            if col[0] in 'GE':
                seen[col[0]] += 1
    return seen


def seek_moves(grid, row, col, enemy):
    if adjacent_enemy(grid, row, col, enemy):
        return None

    first_moves = [(row + 1, col), (row - 1, col), (row, col - 1), (row, col + 1)]
    first_moves = [x for x in first_moves if grid[x[0]][x[1]] == "."]
    best_moves = []

    for move in first_moves:
        r, c = move
        if adjacent_enemy(grid, r, c, enemy):
            best_moves.append((move, 1, move))
            continue
        seen_coordinates = {(row, col), (r, c)}
        stack = [(r + 1, c), (r - 1, c), (r, c - 1), (r, c + 1)]
        # Filter stack to only include "." tiles, which we haven't already seen
        stack = [x for x in stack if grid[x[0]][x[1]] == "." and (x[0], x[1]) not in seen_coordinates]

        step_number = 1  # Already have moved one tile at this point
        run = True
        while run:
            step_number += 1
            new_stack = []

            for tile in stack:
                if tile in seen_coordinates:
                    continue
                seen_coordinates.add(tile)
                r, c = tile
                if adjacent_enemy(grid, r, c, enemy):
                    best_moves.append((move, step_number, (r, c)))
                    run = False
                    continue
                # Add all newly accessible tiles to stack
                new_tiles = [(r + 1, c), (r - 1, c), (r, c - 1), (r, c + 1)]
                new_stack += [x for x in new_tiles if grid[x[0]][x[1]] == "." and (x[0], x[1]) not in seen_coordinates]

            stack = list(set(new_stack))
            # We might also need to end at this point if we have no more newly accessible tiles
            if not stack:
                run = False

    return get_best_move(best_moves)


def make_move(grid, x, y, char, counts):
    r, c = y, x  # Keep track of our current coordinates in case we move
    hero = char[0]
    enemy = {"G": "E", "E": "G"}[hero]
    counts[hero] -= 1
    move_to = seek_moves(grid, y, x, enemy)
    if move_to:
        r, c = move_to  # Need to update our current coordinates for the impending attack
        move_character(grid, y, x, r, c, char)
    return r, c, enemy, hero


def check_death(grid, counts, hero, rounds):
    # Check to see if it's over - all of one side dead
    current_counts = count_characters(grid)
    game_over = any(x == 0 for x in current_counts.values())
    # If game is over, we need to see if the round is complete or not
    if game_over:
        # Means we ended midround
        if counts[hero] > 0:
            final_score = score_game(grid, rounds)
        # Otherwise round is complete- add 1 to rounds when calculating
        else:
            rounds += 1
            final_score = score_game(grid, rounds)
        return final_score
    return None


def score_game(grid, rounds):
    pts = sum(n[1] for row in grid for n in row if n[0] in 'GE')
    return rounds * pts


def reset_moved_flags(grid):
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if col[0] in 'GE':
                grid[y][x] = (col[0], col[1], False)


def beverage_bandits_part_1(map_text):
    grid = generate_grid(map_text)

    rounds = 0

    while True:
        counts = count_characters(grid)

        for y, row in enumerate(grid):
            for x, col in enumerate(row):
                character = grid[y][x]
                if isinstance(character, tuple):
                    if character[2]:
                        continue

                    r, c, enemy, hero = make_move(grid, x, y, character, counts)
                    death = attack(grid, r, c, enemy)
                    if death:
                        final_score = check_death(grid, counts, hero, rounds)
                        if final_score:
                            return final_score

        reset_moved_flags(grid)

        rounds += 1


def beverage_bandits_part_2_loop(map_text, damage_dict):
    grid = generate_grid(map_text)
    rounds = 0

    while True:
        counts = count_characters(grid)
        for y, row in enumerate(grid):
            for x, col in enumerate(row):
                character = grid[y][x]
                if isinstance(character, tuple):
                    if character[2]:
                        continue

                    r, c, enemy, hero = make_move(grid, x, y, character, counts)
                    damage = damage_dict[hero]
                    death = attack(grid, r, c, enemy, damage)
                    if death and enemy == "E":
                        return False
                    elif death:
                        final_score = check_death(grid, counts, hero, rounds)
                        if final_score:
                            return final_score

        reset_moved_flags(grid)
        rounds += 1


def beverage_bandits_part_2(map_text):
    score = False
    damage_dict = {"G": 3, "E": 3}
    while not score:
        damage_dict["E"] += 1
        score = beverage_bandits_part_2_loop(map_text, damage_dict)
    return score


if __name__ == "__main__":
    with open('input.txt') as map_file:
        map_lines = map_file.read().splitlines(keepends=False)
        print(f'Day 15, part 1: {beverage_bandits_part_1(map_lines)}')
        print(f'Day 15, part 2: {beverage_bandits_part_2(map_lines)}')
        # Day 15, part 1: 190012
        # Day 15, part 2: 34364
