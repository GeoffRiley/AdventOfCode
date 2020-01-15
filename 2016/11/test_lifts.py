from lifts import parse, lifts_assemble

arrangement = '''The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.'''


def test_parse():
    # expected = {
    #     'first': ['hydrogen-compatible microchip', 'lithium-compatible microchip'],
    #     'second': ['hydrogen generator'],
    #     'third': ['lithium generator'],
    #     'fourth': []
    # }
    expected = [11, 4, 16, 0]
    assert parse(arrangement) == expected


def test_lifts_assemble():
    assert lifts_assemble(parse(arrangement)) == 11
