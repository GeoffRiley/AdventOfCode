"""
Advent of code 2021
Day 4: Giant Squid
"""
from collections import defaultdict
from typing import List

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list, grouped, extract_ints


def prepare_index(cards: List[List[List[int]]]) -> dict:
    """Go through all the cards noting where all numbers appear."""
    index = defaultdict(list)
    for n, card in enumerate(cards):
        for y, row in enumerate(card):
            for x, element in enumerate(row):
                index[element].append((n, x, y))
    return index


def check_win(card: List[List[int]], col: int, row: int) -> bool:
    """Check the values in the row and column of the current card to see if
        all values are None: if this is the case for either the row or the
        column then we have a win!
    """
    return all(x is None for x in card[row]) or \
           all(y[col] is None for y in card)


def part1(cards: List[List[List[int]]], bingo_calls: list[int]):
    """Work through the calls and check off the cards until we have a winner.
        Winner = full row OR column
    """
    index = prepare_index(cards)

    # perform calls
    for call in bingo_calls:
        for card, col, row in index[call]:
            # mark the card
            cards[card][row][col] = None
            if check_win(cards[card], col, row):
                # we got the winner
                s = sum(sum(i for i in row if i is not None) for row in cards[card])
                return s * call, f'winning card #{card}, winning call {call}'

    raise ValueError('There is a wrong value somewhere')


def part2(cards: List[List[List[int]]], bingo_calls: list[int]):
    """Work through the calls once again, but keep going until the last board
        wins.
    """
    index = prepare_index(cards)
    winning_cards = set()

    # perform calls
    for call in bingo_calls:
        for card, col, row in index[call]:
            if card not in winning_cards:
                # mark the card
                cards[card][row][col] = None
                if check_win(cards[card], col, row):
                    # once a card has won, we won't check it any further
                    winning_cards.add(card)
                    if len(winning_cards) == len(cards):
                        s = sum(sum(i for i in row if i is not None) for row in cards[card])
                        return s * call, f'final winning card #{card}, winning call {call}'

    raise ValueError('There is a wrong value somewhere')


def main():
    loader = LoaderLib(2021)
    input_text = loader.get_aoc_input(4)
    lines = lines_to_list(input_text)

    bingo_calls = extract_ints(lines[0])
    bingo_cards = [[extract_ints(row) for row in rows] for _, *rows in grouped(lines[1:], 6)]

    assert len(lines) == (len(bingo_cards) * 6 + 1)
    loader.print_solution('setup', f'{len(bingo_calls)} calls for {len(bingo_cards)} cards')
    loader.print_solution(1, part1(bingo_cards, bingo_calls))
    loader.print_solution(2, part2(bingo_cards, bingo_calls))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.011869        |        0.011869 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 100 calls for 100 cards
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.004671        |        0.016540 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : (23177, 'winning card #11, winning call 49')
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.005887        |        0.022428 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : (6804, 'final winning card #59, winning call 28')
    # --------------------------------------------------------------------------------
