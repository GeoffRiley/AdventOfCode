import pytest
from ip7 import check_abba, check_aba


@pytest.mark.parametrize('addr, res', [
    ('abba[mnop]qrst', True),
    ('abcd[bddb]xyyx', False),
    ('aaaa[qwer]tyui', False),
    ('ioxxoj[asdfgh]zxcvbn', True)
])
def test_check_abba(addr, res):
    assert check_abba(addr) == res


@pytest.mark.parametrize('addr, res', [
    ('aba[bab]xyz', True),
    ('xyx[xyx]xyx', False),
    ('aaa[kek]eke', True),
    ('zazbz[bzb]cdb', True)
])
def test_check_aba(addr, res):
    assert check_aba(addr) == res
