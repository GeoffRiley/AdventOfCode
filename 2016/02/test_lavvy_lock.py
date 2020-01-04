from lavvy_lock import lavvy_decode


def test_lavvy_decode():
    test_code = '''ULL
RRDDD
LURDL
UUUUD'''
    assert lavvy_decode(test_code) == '1985'
    assert lavvy_decode(test_code, True) == '5DB3'
