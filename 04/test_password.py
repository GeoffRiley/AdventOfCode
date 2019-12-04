import pytest
from password import verify_password


@pytest.mark.parametrize('pwd, res', [
    (111111, False),  # Was True for part one.
    (223450, False),
    (123789, False),
    (12345, False),
    ('abcdef', False),
    (112233, True),
    (123444, False),
    (111122, True)
])
def test_verify_password(pwd: int, res: bool):
    assert verify_password(pwd) is res


@pytest.mark.parametrize('pwd, v_range, res', [
    (111111, '156218-652527', False),
    (233456, '156218-652527', True)
])
def test_verify_password_and_range(pwd, v_range, res):
    assert verify_password(pwd, v_range) is res
