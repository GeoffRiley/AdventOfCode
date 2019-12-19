import pytest

from look_and_say import look_and_say


@pytest.mark.parametrize('in_val, out_val', [
    (1, 11),
    (11, 21),
    (21, 1211),
    (1211, 111221),
    (1112211, 312221)
])
def test_look_and_say(in_val, out_val):
    assert look_and_say(str(in_val)) == str(out_val)
