from hashing_passwords import find_password, find_password2


def test_hashing_passwords():
    assert find_password('abc') == '18f47a30'


def test_find_password2():
    assert find_password2('abc') == '05ace8e3'
