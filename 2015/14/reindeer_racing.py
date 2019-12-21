import re
from collections import defaultdict


def reindeer_racing(disposition: str, period: int, scoring=False) -> int:
    names = defaultdict(list)

    for line in disposition.splitlines(keepends=False):
        # Dancer can fly 37 km/s for 1 seconds, but then must rest for 36 seconds.
        match = re.match(r'^(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds\.', line)
        if match is None:
            raise ValueError(f'Bad disposition string {line}')
        res = match.groups()
        # Name = [ speed , flight time, rest time ]
        names[res[0]] = [int(res[1]), int(res[2]), int(res[3])]

    race = {n: [0, 0, v[0], v[1], v[2], 'R', 0, 0] for n, v in names.items()}

    # values:
    # v0 -- next event time,
    # v1 -- distance travelled at next event,
    # v2 -- speed,
    # v3 -- flight time,
    # v4 -- rest time,
    # v5 -- running state
    # v6 -- cumulative distance
    # v7 -- points
    tm = 0
    while tm < period:
        for n, v in race.items():
            if tm >= v[0]:
                if v[5] == 'F':
                    if v[0] + v[4] > period:
                        part = period - v[0]
                        v[0] += part
                    else:
                        v[0] += v[4]
                    v[5] = 'R'
                else:
                    if v[0] + v[3] > period:
                        part = period - v[0]
                        v[0] += part
                        v[1] += v[2] * part
                    else:
                        v[0] += v[3]
                        v[1] += v[2] * v[3]
                    v[5] = 'F'

        for r, v in race.items():
            if v[5] == 'F':
                v[6] += v[2]
        tm += 1
        dist = max(race.values(), key=lambda x: x[6])[6]
        for r, v in race.items():
            if v[6] == dist:
                v[7] += 1
    # pprint(race)

    if scoring:
        return max(race.values(), key=lambda x: x[7])[7]
    else:
        return max(race.values(), key=lambda x: x[1])[1]


if __name__ == '__main__':
    with open('input') as f:
        catering_needs = f.read()
    print(f'Part 1: {reindeer_racing(catering_needs, 2503)}')
    '''
    {'Blitzen': [2503, 2496, 13, 4, 49, 'R', 2496, 5],
     'Comet': [2503, 2493, 3, 37, 76, 'F', 2493, 22],
     'Cupid': [2503, 2592, 12, 4, 43, 'R', 2592, 13],
     'Dancer': [2503, 2516, 37, 1, 36, 'R', 2516, 1],
     'Dasher': [2503, 2460, 10, 4, 37, 'F', 2460, 0],
     'Donner': [2503, 2655, 9, 5, 38, 'R', 2655, 414],
     'Prancer': [2503, 2484, 9, 12, 97, 'R', 2484, 153],
     'Rudolph': [2503, 2540, 20, 7, 132, 'F', 2540, 887],
     'Vixen': [2503, 2640, 8, 8, 53, 'F', 2640, 1059]}
    Part 1: 2655
    '''

    print(f'Part 2: {reindeer_racing(catering_needs, 2503, scoring=True)}')

    '''
    {'Blitzen': [2503, 2496, 13, 4, 49, 'R', 2496, 5],
     'Comet': [2503, 2493, 3, 37, 76, 'F', 2493, 22],
     'Cupid': [2503, 2592, 12, 4, 43, 'R', 2592, 13],
     'Dancer': [2503, 2516, 37, 1, 36, 'R', 2516, 1],
     'Dasher': [2503, 2460, 10, 4, 37, 'F', 2460, 0],
     'Donner': [2503, 2655, 9, 5, 38, 'R', 2655, 414],
     'Prancer': [2503, 2484, 9, 12, 97, 'R', 2484, 153],
     'Rudolph': [2503, 2540, 20, 7, 132, 'F', 2540, 887],
     'Vixen': [2503, 2640, 8, 8, 53, 'F', 2640, 1059]}
    Part 2: 1059
    '''
