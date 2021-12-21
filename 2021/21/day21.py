"""
Advent of code 2021
Day 21: Dirac Dice
"""
from collections import defaultdict
from dataclasses import dataclass
from itertools import product

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


class DeterministicDie:
    def __init__(self, sides: int):
        self._loop_count = 0
        self._sides = sides
        self._val = 1

    def __iter__(self):
        return self

    def __next__(self):
        val = self._val
        self._val += 1
        if self._val > self._sides:
            self._val = 1
            self._loop_count += 1
        return val

    def triple_roll(self) -> int:
        return next(self) + next(self) + next(self)

    def total_roll_count(self) -> int:
        return self._val + self._loop_count * self._sides - 1


@dataclass
class GameState:
    player1_pos: int
    player2_pos: int
    player1_score: int = 0
    player2_score: int = 0

    @property
    def player1(self):
        return self.player1_pos, self.player1_score

    @property
    def player2(self):
        return self.player2_pos, self.player2_score

    def __repr__(self):
        return f'{self.__class__.__name__}({self.player1_pos}, {self.player2_pos}, {self.player1_score}, {self.player2_score})'

    def __hash__(self):
        return hash((self.player1_pos, self.player2_pos, self.player1_score, self.player2_score))

    def __iter__(self):
        yield self.player1_pos
        yield self.player2_pos
        yield self.player1_score
        yield self.player2_score


def part1(lines):
    """
    """
    die = DeterministicDie(100)
    players = {n: v - 1 for n, v in enumerate(lines)}
    scores = {0: 0, 1: 0}
    player = 1
    while scores[player] < 1000:
        player = -(player - 1)  # Swap between 0 and 1
        players[player] = (players[player] + die.triple_roll()) % 10
        scores[player] += players[player] + 1
    player = -(player - 1)
    loser = scores[player]
    return die.total_roll_count() * loser
    # 1002474


def part2(lines):
    """
    Now we're using a "dirac dice": a 3 sided die that throws all 3 sides into separate universes!

    Rolling 3 times results in 3 x 3 x 3 universes
        1 / 1 / 1 to one universe
        1 / 1 / 2 to another
        1 / 1 / 3 ...
        …
        3 / 3 / 1 ...
        3 / 3 / 2 to the twentieth universe
        3 / 3 / 3 to the twenty-first universe

    Each universe can get a roll total between 3 and 9, the throws occur in a specific regularity:
        3: 1 in 27
        4: 3 in 27
        5: 6 in 27
        6: 7 in 27
        7: 6 in 27
        8: 3 in 27
        9: 1 in 27

    Using these probabilities we can reduce the number of times that we need to calculate results
    from 27 to 7.
    """
    roll_prob = {k: 0 for k in range(3, 10)}
    for x in product(range(1, 4), repeat=3):
        roll_prob[sum(x)] += 1
    assert sum(roll_prob.values()) == 27

    player_win_count = {0: 0, 1: 0}
    player_positions = tuple(v - 1 for v in lines)

    # There are a finite number of ways that the games can be in, so this can be modelled using
    # a state machine---dictionary---holding the count of universes that could be in that state.
    # The key is a tuple made up of the positions of the two players, and their current scores.
    # Of course, we start off with a single universe… that's where the easy stops.
    universe_state = {GameState(*player_positions): 1}

    player = 0
    while universe_state:
        # collect the next set of universe states
        new_state = defaultdict(int)

        # cycle through the current universe states and see what the next turn might result in
        for state, uni_count in universe_state.items():
            # remember the state is: ([player1_pos, player2_pos, player1_score, player2_score])

            # Try each possible roll of the die.
            for die in range(3, 10):
                this_pos, this_score = state.player2 if player else state.player1

                # Move the player first
                this_pos = (this_pos + die) % 10

                # Update score, remembering the '+1' for zero indexing the track.
                this_score += this_pos + 1

                # Check if we have a winner.
                if this_score > 20:
                    # We have a winner… count those winning universes.
                    player_win_count[player] += uni_count * roll_prob[die]
                else:
                    # Not a win yet, but that's more universes entered the fray.
                    # We need a new state object!
                    state2 = GameState(*state)
                    if player:
                        state2.player2_pos, state2.player2_score = this_pos, this_score
                    else:
                        state2.player1_pos, state2.player1_score = this_pos, this_score
                    new_state[state2] = new_state[state2] + uni_count * roll_prob[die]

        # change player
        player = -(player - 1)
        # Start again, with the new set of states.
        universe_state = new_state

    winning_universes = max(player_win_count.values())

    return winning_universes, f'Player 1 wins in {player_win_count[0]} universes; ' \
                              f'player 2 wins in {player_win_count[1]} universes.'
    # 919758187195363


def main():
    loader = LoaderLib(2021)
    input_text = loader.get_aoc_input(21)

    #     input_text = """Player 1 starting position: 4
    # Player 2 starting position: 8"""

    lines = [int(line.rsplit(': ', maxsplit=1)[1]) for line in lines_to_list(input_text)]

    # assert len(lines) == len(...)
    loader.print_solution('setup', f'{len(lines)} players start at {lines}')
    loader.print_solution(1, part1(lines))
    loader.print_solution(2, part2(lines))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.062884        |        0.062884 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 2 players start at [5, 6]
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.002322        |        0.065206 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 1002474
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 3.755012        |        3.820218 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : (919758187195363, 'Player 1 wins in 919758187195363 universes; player 2 wins in 635572886949720 universes.')
    # --------------------------------------------------------------------------------
