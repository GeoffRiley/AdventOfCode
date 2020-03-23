def calibrate_part_1(inp):
    ans = 0
    for line in inp:
        ans += int(line)
    return ans


def calibrate_part_2(inp):
    ans = 0
    history = {0}
    while True:
        for line in inp:
            ans += int(line)
            if ans in history:
                return ans
            history.add(ans)


if __name__ == '__main__':
    with open('input.txt') as calfile:
        cal_strings = calfile.read().splitlines(keepends=False)
        print(f'Day 1, part 1: {calibrate_part_1(cal_strings)}')
        print(f'Day 1, part 2: {calibrate_part_2(cal_strings)}')
        # Day 1, part 1: 513
        # Day 1, part 2: 287
