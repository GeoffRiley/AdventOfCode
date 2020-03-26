import numpy


def cell_power_level(x, y, grid_serial):
    rack_id = x + 10
    pwr = (rack_id * y + grid_serial) * rack_id
    pwr = (pwr // 100) % 10
    return pwr - 5


def chronal_charge_part_1(grid_serial):
    cells = numpy.fromfunction(cell_power_level, (300, 300), grid_serial=grid_serial)
    selections = sum(cells[x:x - 3 or None, y:y - 3 or None] for x in range(3) for y in range(3))
    maximum = int(selections.max())
    loc = numpy.where(selections == maximum)
    return loc[0][0], loc[1][0]


def chronal_charge_part_2(grid_serial):
    cells = numpy.fromfunction(cell_power_level, (300, 300), grid_serial=grid_serial)
    best_cell = None
    highest_score = -999
    # After 25 everything goes negative…
    for squ in range(1, 25):
        selections = sum(cells[x:x - squ or None, y:y - squ or None] for x in range(squ) for y in range(squ))
        maximum = int(selections.max())
        loc = numpy.where(selections == maximum)
        if maximum > highest_score:
            best_cell = (loc[0][0], loc[1][0], squ)
            highest_score = maximum
    return best_cell


if __name__ == '__main__':
    print(f'Day 11, part 1: {chronal_charge_part_1(7672)}')
    print(f'Day 11, part 2: {chronal_charge_part_2(7672)}')
    # Day 11, part 1: (22, 18)
    # Day 11, part 2: (234, 197, 14)
