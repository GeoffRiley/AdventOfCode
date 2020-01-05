import re
import string
from collections import Counter


def check_room(room_name: str) -> (bool, int):
    room_text, sector, checksum = split_name(room_name)
    return do_room_check(room_text, checksum), sector


def do_room_check(room_name, checksum):
    room_name = room_name.replace('-', '')
    c = sorted(Counter(c for c in room_name).items(), key=lambda i: (-i[1], i[0]))
    return ''.join([a[0] for a in c])[:5] == checksum


def decrypt_room(room_name: str) -> (str, int):
    room_text, sector, _ = split_name(room_name)
    return do_decrypt(room_text, sector)


def do_decrypt(room_name, sector):
    shift = sector % 26
    fm = string.ascii_lowercase  # 'abcdefghijklmnopqrstuvwxyz'
    tw = fm[shift:] + fm[:shift]
    return room_name.translate(str.maketrans(fm + '-', tw + ' ')), sector


def split_name(room_name):
    room_text, sector, checksum = re.match(r'(.*)-(\d+)\[(.*)\]', room_name).groups()
    return room_text, int(sector), checksum


if __name__ == '__main__':
    with open('input') as f:
        room_list = f.read()
    sec_tot = 0
    names = dict()
    for room in room_list.splitlines(keepends=False):
        rm, sec, check = split_name(room)
        if do_room_check(rm, check):
            sec_tot += sec
            names[sec] = do_decrypt(rm, sec)[0]
    print(f'Part 1: {sec_tot}')
    pole = [n for n in names.items() if 'northpole' in n[1]]
    print(f'Part 2: {pole[0]}')
    # Part 1: 158835
    # Part 2: (993, 'northpole object storage')
