from reindeer_racing import reindeer_racing

reindeer_spec = '''Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.'''


def test_reindeer_racing():
    assert reindeer_racing(reindeer_spec, 1000) == 1120


def test_reindeer_racing_2():
    assert reindeer_racing(reindeer_spec, 1000, scoring=True) == 689
