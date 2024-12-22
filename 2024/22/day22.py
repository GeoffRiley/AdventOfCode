"""
Advent of code 2024
Day 22: Monkey Market
"""

from collections import defaultdict
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list_int
from aoc.maths import sign


def mix(secret: int, new_num: int) -> int:
    """
    Performs a bitwise XOR operation between a secret number and a new number.

    Calculates the bitwise exclusive OR (XOR) of the secret and new numbers.
    This function provides a way to combine two numbers using bitwise XOR,
    which can be used for various mixing or encryption techniques.

    Args:
        secret (int): The original secret number to be mixed.
        new_num (int): The number to be XORed with the secret number.

    Returns:
        int: The result of the bitwise XOR operation between the secret and
            new number.
    """
    return secret ^ new_num


def prune(secret: int) -> int:
    """
    Reduces a secret number to a value within a specific range using modulo
    operation.

    Limits the secret number to a maximum value of 16,777,216 by performing a
    modulo operation. This function effectively truncates or wraps the input
    number to ensure it stays within a predefined range.

    Args:
        secret (int): The original number to be pruned.

    Returns:
        int: The result of the secret number modulo 16,777,216.
    """
    return secret % 16777216


def mix_and_prune(secret: int, shift: int) -> int:
    """
    Mixes and prunes a secret number using a specific shift value.

    Combines the secret number with a new number using bitwise XOR, then
    reduces the result to a value within a specific range. This function
    provides a way to mix and prune a number in a single step, which can be
    useful for various cryptographic or random number generation algorithms.

    Args:
        secret (int): The original secret number to be mixed and pruned.
        shift (int): The number of bits to shift the secret number.

    Returns:
        int: The result of the mixed and pruned secret number.
    """
    new_num = secret << shift if shift > 0 else secret >> -shift
    mixed = mix(secret, new_num)
    return prune(mixed)


def psuedo_random(seed: int) -> int:
    """
    Generates a pseudorandom number using a specific seed value.

    Calculates a pseudorandom number based on a seed value. This function
    provides a way to generate random-looking numbers that are deterministic
    and repeatable, making them suitable for simulations and other applications
    that require random data.

    Args:
        seed (int): The initial seed value used to generate the pseudorandom
            number.

    Returns:
        int: A pseudorandom number based on the seed value.
    """
    num = mix_and_prune(seed, 6)
    num = mix_and_prune(num, -5)
    num = mix_and_prune(num, 11)
    return num, sign(num) * abs(num) % 10


def part1(lines: list[int]) -> int:
    """
    Calculates a total by applying a pseudo-random transformation to each
    input line multiple times.

    Iterates through a list of input numbers, applying a pseudo-random
    transformation 2000 times to each number. The function accumulates the
    transformed values and returns their sum.

    Args:
        lines (List[int]): A list of initial numbers to be transformed.

    Returns:
        int: The total sum of the transformed numbers after multiple
            iterations.
    """
    total = 0
    for i in lines:
        num = i
        for _ in range(2000):
            num, _ = psuedo_random(num)
        # print(f"{i}: {num}")
        total += num
    return total
    #  Part 1   : 19847565303


def part2(lines: list[int]) -> int:
    """
    Determines the optimal sequence of four consecutive price changes that
    maximizes the total number of bananas collected across all buyers.

    Args:
        lines (List[int]): A list of initial secret numbers for each buyer.

    Returns:
        int: The maximum total number of bananas that can be collected.
    """
    # Dictionary to map each sequence of 4 changes to a list of corresponding
    # prices
    sequences_to_prices = defaultdict(list)

    for idx, initial_secret in enumerate(lines):
        secret = initial_secret

        # Generate the initial price
        current_price = secret % 10
        prices = [current_price]

        # Generate 2000 new secrets and their corresponding prices
        for _ in range(2000):
            secret, digit = psuedo_random(secret)
            prices.append(digit)

        # Compute the list of changes between consecutive prices
        changes = [prices[i] - prices[i - 1] for i in range(1, len(prices))]

        # Dictionary to keep track of the first occurrence of each sequence
        # per buyer
        seen_sequences = {}

        # Slide a window of 4 changes to identify all possible sequences
        for i in range(len(changes) - 3):
            seq = tuple(changes[i : i + 4])

            # If the sequence hasn't been seen before for this buyer, record it
            if seq not in seen_sequences:
                # The price at the point where the sequence completes
                price_at_seq = prices[i + 4]
                seen_sequences[seq] = price_at_seq

        # Aggregate the first occurrence prices for each sequence across all
        # buyers
        for seq, price_at_seq in seen_sequences.items():
            sequences_to_prices[seq].append(price_at_seq)

    # Initialize variables to track the maximum total and the best sequence
    max_total = 0
    best_sequence = None

    # Iterate through all sequences to find the one with the highest total sum
    for seq, prices in sequences_to_prices.items():
        total = sum(prices)
        if total > max_total:
            max_total = total
            best_sequence = seq

    # (Optional) Print the best sequence for verification
    print(f"Best sequence: {best_sequence} with total bananas: {max_total}")

    return max_total


def main():
    loader = LoaderLib(2024)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(22)
    else:
        # input_text = dedent(
        #     """\
        #         1
        #         10
        #         100
        #         2024
        #     """
        # ).strip("\n")
        input_text = dedent(
            """\
                1
                2
                3
                2024
            """
        ).strip("\n")
    # lines = [
    #     (extract_ints(param)) for param in
    #                       [line for line in lines_to_list(input_text)]
    # ]
    # lines = [lines_to_list(line) for line in input_text.split("\n\n")]
    lines = lines_to_list_int(input_text)

    loader.print_solution("setup", f"{len(lines)=} ...")
    loader.print_solution(
        1,
        part1(
            lines,
        ),
    )

    # if testing:
    #     input_text = dedent(
    #         """\
    #         """
    #     ).strip("\n")
    #     lines = lines_to_list(input_text)

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
    # LAP -> 0.000776        |        0.000776 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : len(lines)=2374 ...
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 1.789137        |        1.789913 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 19847565303
    # --------------------------------------------------------------------------------

    # Best sequence: (0, -1, 0, 2) with total bananas: 2250

    # --------------------------------------------------------------------------------
    # LAP -> 3.833602        |        5.623515 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 2   : 2250
    # --------------------------------------------------------------------------------
