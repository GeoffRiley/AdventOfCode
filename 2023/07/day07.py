"""
Advent of code 2023
Day 07: Camel Cards
"""
from collections import Counter
from enum import Enum
from textwrap import dedent
from typing import Literal

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


class CardsFace(Enum):
    """
    The individual cards with a pack of card are represented by single
    characters. The following are the possible characters and their
    meaning:
    - A: Ace (14 points)
    - K: King (13 points)
    - Q: Queen (12 points)
    - J: Jack (11 points)
    - T: Ten (10 points)
    - 9: Nine (9 points)
    - 8: Eight (8 points)
    - 7: Seven (7 points)
    - 6: Six (6 points)
    - 5: Five (5 points)
    - 4: Four (4 points)
    - 3: Three (3 points)
    - 2: Two (2 points)
    - 0: Joker (0 points)
    These values are used to calculate the power of a hand when comparing
    two hands with equivalent types.
    """

    ACE = "A"
    KING = "K"
    QUEEN = "Q"
    JACK = "J"
    TEN = "T"
    NINE = "9"
    EIGHT = "8"
    SEVEN = "7"
    SIX = "6"
    FIVE = "5"
    FOUR = "4"
    THREE = "3"
    TWO = "2"
    JOKER = "_"

    def __str__(
        self,
    ) -> Literal["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2", "_"]:
        return self.value

    def __repr__(
        self,
    ) -> Literal["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2", "_"]:
        return self.value

    def __int__(self) -> int:
        """
        Convert the card face to its integer value
        """
        if self.value == "A":
            return 14
        elif self.value == "K":
            return 13
        elif self.value == "Q":
            return 12
        elif self.value == "J":
            return 11
        elif self.value == "T":
            return 10
        elif self.value == "_":
            return 0
        else:
            return int(self.value)


class HandTypes(Enum):
    """
    The different types of hands that can be formed with a pack of cards.
    The following are the possible types along with their power:
    - Five of a kind: 7
    - Four of a kind: 6
    - Full house: 5
    - Three of a kind: 4
    - Two pairs: 3
    - One pair: 2
    - High card: 1
    """

    FIVE_OF_A_KIND = 700_000_000
    FOUR_OF_A_KIND = 600_000_000
    FULL_HOUSE = 500_000_000
    THREE_OF_A_KIND = 400_000_000
    TWO_PAIRS = 300_000_000
    ONE_PAIR = 200_000_000
    HIGH_CARD = 100_000_000

    def __str__(
        self,
    ) -> Literal[
        "FIVE_OF_A_KIND",
        "FOUR_OF_A_KIND",
        "FULL_HOUSE",
        "THREE_OF_A_KIND",
        "TWO_PAIRS",
        "ONE_PAIR",
        "HIGH_CARD",
    ]:
        return self.name

    def __repr__(
        self,
    ) -> Literal[
        "FIVE_OF_A_KIND",
        "FOUR_OF_A_KIND",
        "FULL_HOUSE",
        "THREE_OF_A_KIND",
        "TWO_PAIRS",
        "ONE_PAIR",
        "HIGH_CARD",
    ]:
        return self.name

    def __int__(self) -> int:
        """
        Convert the hand type to its integer value
        """
        if self.name == "FIVE_OF_A_KIND":
            return self.FIVE_OF_A_KIND.value
        elif self.name == "FOUR_OF_A_KIND":
            return self.FOUR_OF_A_KIND.value
        elif self.name == "FULL_HOUSE":
            return self.FULL_HOUSE.value
        elif self.name == "THREE_OF_A_KIND":
            return self.THREE_OF_A_KIND.value
        elif self.name == "TWO_PAIRS":
            return self.TWO_PAIRS.value
        elif self.name == "ONE_PAIR":
            return self.ONE_PAIR.value
        else:
            return self.HIGH_CARD.value


class Hand:
    """
    A hand is a collection of five cards. The hand is used to determine
    the power of the hand and the type of hand. The power of the hand is
    used to compare two hands of the same type. The type of hand is used
    to compare two hands of different types.
    """

    def __init__(self, cards: str, bid: int, jokers_wild: bool = False) -> None:
        """
        Initialise the hand with the given list of cards and bid value
        """
        if jokers_wild:
            cards = cards.replace(CardsFace.JACK.value, CardsFace.JOKER.value)
        self.jokers_wild = jokers_wild
        self.cards = cards
        # convert the card string to a list of CardsFace objects
        self.cards_list = [CardsFace(c) for c in self.cards]
        self.bid = bid
        self.type = self.get_type()
        self.power = self.get_power()  # The power depends on the type

    def get_type(self) -> HandTypes:
        """
        Calculate the type of the hand
        """
        c = Counter(self.cards)
        if self.jokers_wild:
            if len(c) == 1:
                return HandTypes.FIVE_OF_A_KIND
            elif len(c) == 2:
                if c[CardsFace.JOKER.value] > 0:
                    return HandTypes.FIVE_OF_A_KIND
                if 4 in c.values():
                    return HandTypes.FOUR_OF_A_KIND
                else:
                    return HandTypes.FULL_HOUSE
            elif len(c) == 3:
                if 3 in c.values():
                    return (
                        HandTypes.THREE_OF_A_KIND
                        if c[CardsFace.JOKER.value] == 0
                        else HandTypes.FOUR_OF_A_KIND
                    )
                else:
                    return (
                        HandTypes.TWO_PAIRS
                        if c[CardsFace.JOKER.value] == 0
                        else HandTypes.FULL_HOUSE
                        if c[CardsFace.JOKER.value] == 1
                        else HandTypes.FOUR_OF_A_KIND
                    )
            elif len(c) == 4:
                return (
                    HandTypes.ONE_PAIR
                    if c[CardsFace.JOKER.value] == 0
                    else HandTypes.THREE_OF_A_KIND
                )
            return (
                HandTypes.HIGH_CARD
                if c[CardsFace.JOKER.value] == 0
                else HandTypes.ONE_PAIR
            )

        if len(c) == 1:
            return HandTypes.FIVE_OF_A_KIND
        elif len(c) == 2:
            if 4 in c.values():
                return HandTypes.FOUR_OF_A_KIND
            else:
                return HandTypes.FULL_HOUSE
        elif len(c) == 3:
            if 3 in c.values():
                return HandTypes.THREE_OF_A_KIND
            else:
                return HandTypes.TWO_PAIRS
        elif len(c) == 4:
            return HandTypes.ONE_PAIR
        return HandTypes.HIGH_CARD

    def get_power(self) -> int:
        """
        Calculate the power of the hand; the power depends on the type.
        The main power is the power of the hand type. The secondary power
        is the power of the cards in the hand.
        The order of the cards is important for the secondary power, so
        the cards are not sorted. The first card gives the highest power,
        the second card the second highest power, and so on.
        """
        base_power = self.type.value

        card_power = 0  # Power builds up from the cards in multiple of 15
        for card in self.cards_list:
            card_power = (card_power + int(card)) * 15

        return base_power + card_power


def part1(lines):
    """ """
    hands = []
    for line in lines:
        cards, bid = line.split()
        hands.append(Hand(cards, int(bid)))

    sorted_hands = sorted(hands, key=lambda x: x.power)
    payout = 0
    for n, hand in enumerate(sorted_hands):
        payout += hand.bid * (n + 1)
        # print(n, hand.cards, hand.bid, hand.type, hand.power)

    return payout


def part2(lines):
    """
    Joker rule: J is now a joker. It can be used as any card, but it
    is counted as a 0 for the purpose of calculating the power of the
    hand. The power of the hand is calculated as if the joker was not
    present.
    For example, the hand "JQJQJ 100" is FIVE_OF_A_KIND with base power
    of 700_000_000, but only the three Queens add to the bonus value.
    """
    hands = []
    for line in lines:
        cards, bid = line.split()
        hands.append(Hand(cards, int(bid), jokers_wild=True))

    sorted_hands = sorted(hands, key=lambda x: x.power)
    payout = 0
    for n, hand in enumerate(sorted_hands):
        payout += hand.bid * (n + 1)
        # print(n, hand.cards, hand.bid, hand.type, hand.power)

    return payout


def main():
    loader = LoaderLib(2023)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(7)
    else:
        input_text = dedent(
            """\
            32T3K 765
            T55J5 684
            KK677 28
            KTJJT 220
            QQQJA 483
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
    #  LAP -> 0.002639        |        0.002639 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 1000 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.038422        |        0.041061 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 247815719
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.049222        |        0.090283 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 248747492
    # --------------------------------------------------------------------------------
