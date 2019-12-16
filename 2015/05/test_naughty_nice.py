import pytest

from naughty_nice import is_nice, is_nicer


@pytest.mark.parametrize('name, nice', [
    ('ugknbfddgicrmopn', True),
    ('aaa', True),
    ('jchzalrnumimnmhp', False),
    ('haegwjzuvuyypxyu', False),
    ('dvszwmarrgswjxmb', False)
])
def test_is_nice(name, nice):
    assert is_nice(name) == nice


@pytest.mark.parametrize('name, nice', [
    ('qjhvhtzxzqqjkmpb', True),
    ('xxyxx', True),
    ('uurcxstgmygtbstg', False),
    ('ieodomkazucvgmuy', False)
])
def test_is_nicer(name, nice):
    assert is_nicer(name) == nice
