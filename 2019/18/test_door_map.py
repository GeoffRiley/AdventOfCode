import pytest

from door_map import setup_grid, search

map1 = '''#########
#b.A.@.a#
#########'''

map2 = '''########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################'''

map3 = '''########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################'''

map4 = '''#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################'''

map5 = '''########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################'''


@pytest.mark.parametrize('maze, steps', [
    (map1, 8),
    (map2, 86),
    (map3, 132),
    (map4, 136),
    (map5, 81)
])
def test_door_map(maze, steps):
    setup_grid(maze)
    assert search() == steps
