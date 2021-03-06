import pytest
from monitor import create_map, find_best_station, vapourise_asteroids


@pytest.mark.parametrize('text_map, best, num', [
    ('''......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####''', (5, 8), 33),
    ('''#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.''', (1, 2), 35),
    ('''.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..''', (6, 3), 41),
    ('''.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##''', (11, 13), 210)
])
def test_map_search(text_map, best, num):
    grid = create_map(text_map)
    assert all(isinstance(n, int) for row in grid for n in row)
    assert find_best_station(grid) == (best, num)


@pytest.fixture(scope='module')
def small_asteroids():
    grid = create_map('''.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....#...###..
..#.#.....#....##''')
    return vapourise_asteroids(grid, (8, 3))


@pytest.fixture(scope='module')
def asteroids():
    grid = create_map('''.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##''')
    return vapourise_asteroids(grid, (11, 13))


"""
01234567890123456

          111  1
        89012  5
.#....###24...#.. 0
##...##.13#67..9# 1
##...#...5.8####. 2
..#.....X...###.. 
..#.#.....#....## 

(8,1) (9,0) (9,1) (10,0) (9,2) (11,1) (12,1) (11,2) (15,1)

          1 11111
    4     0 23456
.#....###.....#.. 
##...##...#.....# 
##...#......1234. 2
..#.....X...5##.. 3
..#.9.....8....76 4

(12,2) (13,2) (14,2) (15,2) (12,3) (16,4) (15,4) (10,4) (4,4)

123  6
.8....###.....#.. 1
56...9#...#.....# 2
34...7........... 3
..2.....X....##.. 4
..1.............. 5

(3,5) (3,4) (1,3) (2,3) (1,2) (2,2) (6,3) (2,1) (6,2)


"""


@pytest.mark.parametrize('position, coord', [
    (1, (8, 1)),
    (2, (9, 0)),
    (3, (9, 1)),
    (4, (10, 0)),
    (5, (9, 2)),
    (6, (11, 1)),
    (7, (12, 1)),
    (8, (11, 2)),
    (9, (15, 1)),
    (10, (12, 2)),
    (11, (13, 2)),
    (12, (14, 2)),
    (13, (15, 2)),
    (14, (12, 3)),
    (15, (16, 4)),
    (16, (15, 4)),
    (17, (10, 4)),
    (18, (4, 4)),
    (19, (2, 4)),
    (20, (2, 3)),
    (21, (0, 2)),
    (22, (1, 2)),
    (23, (0, 1)),
    (24, (1, 1)),
    (25, (5, 2)),
    (26, (1, 0)),
    (27, (5, 1)),
])
def test_vapourise_small_asteroids(small_asteroids, position, coord):
    assert small_asteroids[position - 1][1] == coord


@pytest.mark.parametrize('position, coord', [
    (1, (11, 12)),
    (2, (12, 1)),
    (3, (12, 2)),
    (10, (12, 8)),
    (20, (16, 0)),
    (50, (16, 9)),
    (100, (10, 16)),
    (199, (9, 6)),
    (200, (8, 2)),
    (201, (10, 9)),
    (299, (11, 1))
])
def test_vapourise_asteroids(asteroids, position, coord):
    assert asteroids[position - 1][1] == coord
