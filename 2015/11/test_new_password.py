import pytest

from new_password import check_password, generate_password


@pytest.mark.parametrize('password, valid', [
    ('hijklmmn', False),
    ('abbceffg', False),
    ('abbcegjk', False),
    ('abcdffaa', True),
    ('ghjaabcc', True)
])
def test_check_password(password, valid):
    assert check_password(password) == valid


@pytest.mark.parametrize('old_password, new_password', [
    ('abcdefgh', 'abcdffaa'),
    ('ghijklmn', 'ghjaabcc')
])
def test_generate_password(old_password, new_password):
    assert generate_password(old_password) == new_password
