from microbots import microbots

instruction = '''value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2'''


def test_microbots():
    assert microbots(instruction, val_a=2, val_b=5) == 2
