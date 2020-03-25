from collections import defaultdict, deque


def play_game(marbles, players):
    scores = defaultdict(int)
    circle = deque([0])
    for marble in range(1, marbles + 1):
        if marble % 23 == 0:
            circle.rotate(7)
            scores[marble % players] += marble + circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)
    return max(scores.values())


def marble_mania_part_1(inp):
    words = inp[0].split()
    players = int(words[0])
    marbles = int(words[6])
    return play_game(marbles, players)


def marble_mania_part_2(inp):
    words = inp[0].split()
    players = int(words[0])
    marbles = int(words[6]) * 100
    return play_game(marbles, players)


if __name__ == '__main__':
    with open('input.txt') as marble_file:
        marbles_text = marble_file.read().splitlines(keepends=False)
        print(f'Day 9, part 1: {marble_mania_part_1(marbles_text)}')
        print(f'Day 9, part 2: {marble_mania_part_2(marbles_text)}')
        # Day 9, part 1: 434674
        # Day 9, part 2: 3653994575
