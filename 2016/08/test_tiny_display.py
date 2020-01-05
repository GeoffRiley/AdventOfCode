from tiny_display import do_display

script = '''rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1'''

expected = [
    [False, True, False, False, True, False, True],
    [True, False, True, False, False, False, False],
    [False, True, False, False, False, False, False]
]


def test_do_display():
    assert do_display(script, width=7, height=3) == expected
