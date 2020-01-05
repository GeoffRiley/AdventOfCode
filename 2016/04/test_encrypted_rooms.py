import pytest
from encrypted_rooms import check_room, decrypt_room

sec_sum = 0


@pytest.mark.parametrize('room_name, reality', [
    ('aaaaa-bbb-z-y-x-123[abxyz]', True),
    ('a-b-c-d-e-f-g-h-987[abcde]', True),
    ('not-a-real-room-404[oarel]', True),
    ('totally-real-room-200[decoy]', False)
])
def test_check_room(room_name, reality):
    global sec_sum

    check, sec = check_room(room_name)
    assert check == reality
    if check:
        sec_sum += sec


def test_sec_sum():
    global sec_sum

    assert sec_sum == 1514


def test_decrypt_room():
    txt, sec = decrypt_room('qzmt-zixmtkozy-ivhz-343[abc]')
    assert txt == 'very encrypted name'
