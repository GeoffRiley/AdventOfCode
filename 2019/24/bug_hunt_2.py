from copy import deepcopy

# We'll measure over 200 minutes
MINUTES = 200
# Prepare a template big enough to hold all generations
GRID_SIZE = 5
TOTAL_LEVELS = (MINUTES + 2) * 2 + 1
GRID_TEMPLATE = [[["." for col in range(GRID_SIZE)] for row in range(GRID_SIZE)] for z in range(TOTAL_LEVELS)]
START_LEVEL = MINUTES + 3


def num_next_level_neighbours(field, level, pos):
    if pos[0] == GRID_SIZE // 2 - 1:
        return sum(field[level][0][col] == "#" for col in range(GRID_SIZE))

    if pos[0] == GRID_SIZE // 2 + 1:
        return sum(field[level][GRID_SIZE - 1][col] == "#" for col in range(GRID_SIZE))

    if pos[1] == GRID_SIZE // 2 - 1:
        return sum(field[level][row][0] == "#" for row in range(GRID_SIZE))

    if pos[1] == GRID_SIZE // 2 + 1:
        return sum(field[level][row][GRID_SIZE - 1] == "#" for row in range(GRID_SIZE))


def num_neighbours(field, level, pos):
    count = 0

    # look around the four sides for neighbours
    for neighbour in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
        new_pos = (pos[0] + neighbour[0], pos[1] + neighbour[1])

        # if the neighbour is a centre spot, check the appropriate cells in the next level down
        if new_pos[0] == 2 and new_pos[1] == 2:
            count += num_next_level_neighbours(field, level - 1, pos)

        # if the neighbour is off the edge of the 5x5 grid, then check the cells in the next level up
        elif new_pos[0] == -1:
            if field[level + 1][1][2] == "#":
                count += 1

        elif new_pos[0] == GRID_SIZE:
            if field[level + 1][3][2] == "#":
                count += 1

        elif new_pos[1] == -1:
            if field[level + 1][2][1] == "#":
                count += 1

        elif new_pos[1] == GRID_SIZE:
            if field[level + 1][2][3] == "#":
                count += 1

        # if it's none of the 'special' cells, then just look at the normal cell!!
        elif field[level][new_pos[0]][new_pos[1]] == "#":
            count += 1

    return count


def generate(field):
    # Creat a new copy of the template to fill the results into
    new_field = deepcopy(GRID_TEMPLATE)

    for level in range(0, TOTAL_LEVELS - 1):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                # Skip centre spots
                if col == GRID_SIZE // 2 and row == GRID_SIZE // 2:
                    continue

                neighbour_count = num_neighbours(field, level, (row, col))
                if field[level][row][col] == "#":
                    # An active bug stays active if it only have one neighbour
                    if neighbour_count == 1:
                        new_field[level][row][col] = "#"
                else:
                    # An absent but appears if there are 1 or 2 active bugs in the neighbours
                    if neighbour_count in [1, 2]:
                        new_field[level][row][col] = "#"

    # new_field holds the next generation
    return new_field


def run():
    with open('input') as f:
        initial_grid = f.read().splitlines(keepends=False)

    # Make a copy of the template
    field = deepcopy(GRID_TEMPLATE)

    # Load the initial grid into the start level in the middle
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            field[START_LEVEL][row][col] = initial_grid[row][col]

    # Generate new states for 200 minutes
    for _ in range(MINUTES):
        field = generate(field)

    return sum(field[level][row][col] == "#"
               for level in range(TOTAL_LEVELS)
               for row in range(GRID_SIZE)
               for col in range(GRID_SIZE))


result = run()
print(f"Solution: {result}")
assert result == 1959
