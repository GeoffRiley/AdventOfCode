from message_noise import scrub_noise

msg = '''eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar'''


def test_scrub_noise():
    assert scrub_noise(msg) == 'easter'
    assert scrub_noise(msg, True) == 'advent'
