import re
from collections import Counter
from enum import IntEnum


class Errors(IntEnum):
    NO_ERROR = 0
    SIX_DIGITS = 1
    OUT_OF_RANGE = 2
    TRIPLE_DIGITS = 3
    SEQUENCE_FAULT = 4


FIND_DOUBLES = re.compile(r'((\d)\2+)')


def verify_password(pwd, v_range='000000-999999', lo=None, hi=None):
    pwd_str = str(pwd)
    if lo is None:
        lo, hi = [int(v) for v in v_range.split('-')]

    # Is six digit number
    if len(pwd_str) != 6 or not pwd_str.isdigit():
        return Errors.SIX_DIGITS

    # Is within specified range
    if not (lo <= pwd <= hi):
        return Errors.OUT_OF_RANGE

    # Has two adjacent digits the same
    if not any(len(g[0]) == 2 for g in FIND_DOUBLES.findall(pwd_str)):
        return Errors.TRIPLE_DIGITS

    # Increase in value as they go left to right
    # if "".join(sorted(pwd_str)) != pwd_str:
    #     return Errors.SEQUENCE_FAULT
    # The following is quicker!
    x = '0'
    for y in pwd_str:
        if y < x:
            return Errors.SEQUENCE_FAULT
        x = y

    return Errors.NO_ERROR


if __name__ == '__main__':
    input_range = '156218-652527'
    lo, hi = [int(v) for v in input_range.split('-')]
    print('==================')
    count = Counter(verify_password(d, lo=lo, hi=hi) for d in range(lo, hi + 1))
    ratio = 40 / count[max(count)]
    for item, val in count.items():
        print(f'{item.name:15} : {val:6} : {"*" * int(ratio * val)}')
    print('==================')
