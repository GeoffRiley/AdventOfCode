from otp import otp


# def test_otp():
#     res = otp('abc')
#     assert res[0] == 39
#     assert res[1] == 92
#     assert res[63] == 22728

def test_otp_part2():
    res = otp('abc', part2=True)
    assert res[0] == 10
    assert res[63] == 22551
