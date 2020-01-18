from collections import defaultdict
from hashlib import md5
from os.path import exists


def otp(salt: str, min_hashes=40000, part2=False):
    fname = f'input-{salt}{"-ext" if part2 else ""}'
    if exists(fname):
        with open(fname) as f:
            start = len(f.readlines())
    else:
        start = 0

    with open(fname, 'a') as f:
        for key in range(start, max(start + 1000, min_hashes)):
            cand = md5(f'{salt}{key}'.encode()).hexdigest()
            if part2:
                for _ in range(2016):
                    cand = md5(cand.encode()).hexdigest()
            f.write(cand + '\n')

    res = set()
    candidates = defaultdict(list)

    with open(fname) as f:
        for key, cand in enumerate(f.read().splitlines(keepends=False)):
            try:
                ch = [c[0] for c in zip(cand, cand[1:], cand[2:], cand[3:], cand[4:]) if len(set(c)) == 1][0]
                for chk in candidates[ch]:
                    if 0 < key - chk <= 1000:
                        res.add(chk)
                        # candidates[ch].remove(chk)
            except:
                pass

            try:
                ch = [c[0] for c in zip(cand, cand[1:], cand[2:]) if len(set(c)) == 1][0]
                candidates[ch].append(key)
            except:
                pass

    return list(sorted(res))


if __name__ == '__main__':
    answer = otp('cuanljph', 40000)
    print(f'Part 1: {answer[63]}')
    answer = otp('cuanljph', 40000, part2=True)
    print(f'Part 2: {answer[63]}')
    # Part 1: 23769
    # Part 2: 20606
