from typing import List, Dict, Tuple


def setup_player_decks(data: str) -> Dict[int, List[int]]:
    players: Dict[int, List[int]] = {
        int((lines := player.splitlines(keepends=False))[0].strip(':').split()[1]): list(map(int, lines[1:]))
        for player in data.strip().split('\n\n')
    }
    return players


def crab_combat_part1(data: str) -> int:
    players: Dict[int, List[int]] = setup_player_decks(data)

    while all(len(p) > 0 for p in players.values()):
        a, b = (p.pop(0) for p in players.values())
        if a > b:
            players[1].extend([a, b])
        else:
            players[2].extend([b, a])
    winner = players[1].copy()
    winner.extend(players[2])

    return sum(n * i for n, i in enumerate(winner[::-1], start=1))


def crab_combat_part2(data: str) -> int:
    players: Dict[int, List[int]] = setup_player_decks(data)

    def play(playcards: Dict[int, List[int]]) -> Tuple[int, Dict[int, List[int]]]:
        play_log = set()
        while all(len(p) > 0 for p in playcards.values()):
            if str(playcards) in play_log:
                # Force player 1 win
                playcards[1].extend(playcards[2])
                playcards[2].clear()
                break
            else:
                play_log.add(str(playcards))
                a, b = (p.pop(0) for p in playcards.values())
                c, d = (len(p) for p in playcards.values())
                if a <= c and b <= d:
                    # Setup sub-game
                    n_players: Dict[int, List[int]] = dict()
                    n_players[1] = playcards[1][:a]
                    n_players[2] = playcards[2][:b]
                    sub_win, _ = play(n_players)
                else:
                    sub_win = 1 if a > b else 2
            if sub_win == 1:
                playcards[1].extend([a, b])
            else:
                playcards[2].extend([b, a])
        return 1 if len(playcards[1]) > 0 else 2, playcards

    win, players = play(players)
    winner = players[win].copy()

    return sum(n * i for n, i in enumerate(winner[::-1], start=1))


if __name__ == '__main__':
    test_text = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
"""
    assert crab_combat_part1(test_text) == 306
    assert crab_combat_part2(test_text) == 291
    test_text2 = """Player 1:
43
19

Player 2:
2
29
14
"""
    assert crab_combat_part2(test_text2) == 369

    with open('input.txt') as in_file:
        in_text = in_file.read()
        part1 = crab_combat_part1(in_text)
        print(f'Part1: {part1}')
        part2 = crab_combat_part2(in_text)
        print(f'Part2: {part2}')

    # Part1: 30138
    # Part2: 31587
