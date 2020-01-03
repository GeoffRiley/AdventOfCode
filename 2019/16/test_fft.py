import pytest

from fft import fft, perform_phase


@pytest.mark.parametrize('pass_num, digits, result', [
    (1, '12345678', '48226158'),
    (2, '48226158', '34040438'),
    (3, '34040438', '03415518'),
    (4, '03415518', '01029498')
])
def test_perform_phase(pass_num, digits, result):
    d_array = tuple(int(a) for a in digits)
    r_array = tuple(int(a) for a in result)
    assert perform_phase(d_array) == r_array


@pytest.mark.parametrize('digits, result', [
    ('80871224585914546619083218645595', '24176176'),
    ('19617804207202209144916044189917', '73745418'),
    ('69317163492948606335995924319873', '52432133')
])
def test_fft(digits, result):
    assert fft(digits) == result


@pytest.mark.parametrize('digits, result', [
    ('03036732577212944063491565474664', '84462026'),
    ('02935109699940807407585447034323', '78725270'),
    ('03081770884921959731165446850517', '53553731')
])
def test_ttf_10k(digits, result):
    assert fft(digits, part2=True) == result
