"""
Advent of code 2023
Day 04: Scratchcards
"""
from collections import defaultdict
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


def parse_game_input(line):
    """
    Each game line shows a list of winning numbers and a list of your numbers,
    separated by a pipe (|).
    Example: Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    The game number is the number after the word "Card".
    The winning numbers are the numbers before the pipe.
    Your numbers are the numbers after the pipe.

    We return the number of winning numbers that match
    your numbers.
    """
    numbers = line.split(":")[1]
    winners, runners = [x.strip() for x in numbers.split("|")]

    winning_numbers = set([int(x) for x in winners.split()])
    your_numbers = set([int(x) for x in runners.split()])

    return len(winning_numbers & your_numbers)


def part1(lines):
    """
    We have a stack of scratchcards.
    Each card has a list of winning numbers and a list of your numbers.
    If any of your numbers match any of the winning numbers, you win.
    For each winning number you double your winnings.

    What is the total amount of money you win?
    """
    game_list = []

    for line in lines:
        winning_count = parse_game_input(line)

        if winning_count > 0:
            game_list.append(2 ** (winning_count - 1))

    return sum(game_list)


SEMAPHORE = object()


def totaliser(card_num, game_cards, score_cache):
    """
    This is a recursive function.
    We are given a card number and a dictionary of game cards.
    We return the total number of cards won.
    """
    # First check the cache!
    if score_cache[card_num] is not SEMAPHORE:
        return score_cache[card_num]
    # Second, we know that we can never exceeed the number of cards
    # in the game.
    if card_num >= len(game_cards):
        return 0
    # Finally, we recursively call ourself for any winning cards.
    # Easiest to do this in a list comprehension.
    total = 1 + sum(
        totaliser(x, game_cards, score_cache)
        for x in range(card_num + 1, card_num + game_cards[card_num] + 1)
    )
    # Store the result in the cache.
    score_cache[card_num] = total
    return total


def part2(lines):
    """
    Now we know more about the game.
    Each of the winning scractchcards with winning numbers award copies
    of the subsequently numbered scratchcards.
    For example, if card 4 has three winning numbers, you get copies of
    cards 5, 6 and 7.
    These copies are added to the stack of scratchcards, but retain their
    original card number and can trigger further winnings.
    """
    # We need to keep track of the cards we have won.
    # We'll generate a list of all the cards in a dictionary, with the
    # card number as the key and the number of copies as the value.
    card_list = defaultdict(int)
    game_cards = []  # We'll use this to look up the winning numbers.

    # This is going to be a recursive function, so we'll use a cache to
    # store the partial results. The SEMAPHORE object is used as a placeholder
    # for the uncalculated cache entries.
    score_cache = [SEMAPHORE] * len(lines)

    # Initialise the game card list.
    for line in lines:
        winning_count = parse_game_input(line)
        game_cards.append(winning_count)

    for card_num in range(0, len(game_cards)):
        card_list[card_num] = totaliser(card_num, game_cards, score_cache)

    return sum(card_list.values())


def main():
    loader = LoaderLib(2023)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(4)
    else:
        input_text = dedent(
            """\
            Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
            Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
            Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
            Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
            Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
            Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
            """
        ).strip("\n")
    lines = lines_to_list(input_text)

    loader.print_solution("setup", f"{len(lines)} ...")
    loader.print_solution(
        1,
        part1(
            lines,
        ),
    )
    loader.print_solution(
        2,
        part2(
            lines,
        ),
    )


if __name__ == "__main__":
    main()
    # --
    # --------------------------------------------------------------------------------
    #  LAP -> 0.000114        |        0.000114 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 190 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.000817        |        0.000931 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 15205
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.000874        |        0.001805 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 6189740
    # --------------------------------------------------------------------------------
    #
