from wiper import wiper


def test_wiper():
    a, b = wiper("10000", 20)
    assert a == '10000011110010000111'
    assert b == '01100'
