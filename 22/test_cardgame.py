import pytest

from cardgame import cardgame


@pytest.mark.parametrize('instr, result', [
    ('''deal with increment 7
deal into new stack
deal into new stack''',
     '0 3 6 9 2 5 8 1 4 7'),
    ('''cut 6
deal with increment 7
deal into new stack''',
     '3 0 7 4 1 8 5 2 9 6'),
    ('''deal with increment 7
deal with increment 9
cut -2''',
     '6 3 0 7 4 1 8 5 2 9'),
    ('''deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1''',
     '9 2 5 8 1 4 7 0 3 6')
])
def test_cardgame(instr, result):
    deck = [n for n in range(10)]
    assert ' '.join(str(v) for v in cardgame(deck, instr)) == result
