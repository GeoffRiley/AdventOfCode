"""
Advent of code 2024
Day 21: Keypad Conundrum
"""

from textwrap import dedent
from typing import Any

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


# Numeric Keypad Layout:
# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
# |   | 0 | A |
# +---+---+---+
numeric_pos = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    None: (3, 0),
    "0": (3, 1),
    "A": (3, 2),
}

# Directional Keypad Layout:
# +---+---+---+
# |   | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+
directional_pos = {
    None: (0, 0),
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}


def sanitize_paths(paths, p0, numeric=True) -> Any:
    """Sanitizes a list of paths by removing paths that pass through a
    specific excluded position.

    Filters out paths that intersect with a predefined excluded position based
    on the input parameters. The function modifies the input paths list
    in-place and returns the filtered paths.

    Args:
        paths (List[str]): A list of path strings representing directional
            movements.
        p0 (List[int]): The starting position coordinates.
        numeric (bool, optional): Flag to determine which excluded position
            set to use. Defaults to True.

    Returns:
        Any: The modified list of paths after filtering out paths crossing the
            excluded position.
    """

    excluded_pos = numeric_pos[None] if numeric else directional_pos[None]

    i = 0
    while i < len(paths):
        p = list(p0)
        for d in paths[i]:

            if d == "<":
                p[1] -= 1
            elif d == ">":
                p[1] += 1

            elif d == "^":
                p[0] -= 1
            elif d == "v":
                p[0] += 1

            if tuple(p) == excluded_pos:
                paths.pop(i)
                i -= 1
                break

        i += 1

    return paths


def get_shortest_paths(src_pos, trg_pos, numeric=True) -> Any:
    """Generates the shortest possible paths between two positions with
    optional filtering.

    Calculates the minimal directional paths from a source to a target
    position using cardinal directions. The function returns sanitized path
    variations based on the specified parameters.

    Args:
        src_pos (List[int]): The starting position coordinates.
        trg_pos (List[int]): The target position coordinates.
        numeric (bool, optional): Flag to determine path sanitization method.
            Defaults to True.

    Returns:
        Any: A list of sanitized shortest paths between the source and target
            positions.
    """

    cx = "^" if trg_pos[0] - src_pos[0] < 0 else "v"
    dx = abs(trg_pos[0] - src_pos[0])
    cy = "<" if trg_pos[1] - src_pos[1] < 0 else ">"
    dy = abs(trg_pos[1] - src_pos[1])

    return sanitize_paths(
        list({cx * dx + cy * dy, cy * dy + cx * dx}), src_pos, numeric=numeric
    )


def solve_numeric(num) -> list[list[str]]:
    """Generates a sequence of paths for numeric navigation between predefined
    positions.

    Calculates the shortest paths between numeric positions, starting from an
    initial position and moving through a sequence of numbers. The function
    returns a list of path variations with an additional 'A' marker at the end
    of each path.

    Args:
        num (Iterable[str]): A sequence of numeric identifiers to navigate
            through.

    Returns:
        List[List[str]]: A list of path variations for each numeric transition,
            with 'A' appended to each path.
    """

    pos = numeric_pos["A"]

    sequence = []

    for n in num:
        p = numeric_pos[n]
        paths = get_shortest_paths(pos, p, numeric=True)
        pos = p
        sequence.append(paths)

    sequence_parts = []
    for part in sequence:
        tmp = ["".join(p) + "A" for p in part]
        sequence_parts.append(tmp)

    return sequence_parts


def solve_directional(seq) -> list[list[str]]:
    """Generates a sequence of paths for directional navigation between
    predefined positions.

    Calculates the shortest paths between directional positions, starting from
    an initial position and moving through a sequence of directions. The
    function returns a list of path variations with an additional 'A' marker
    at the end of each path.

    Args:
        seq (Iterable[str]): A sequence of directional identifiers to navigate
            through.

    Returns:
        List[List[str]]: A list of path variations for each directional
            transition, with 'A' appended to each path.
    """

    pos = directional_pos["A"]

    sequence = []

    for n in seq:
        p = directional_pos[n]
        paths = get_shortest_paths(pos, p, numeric=False)
        pos = p
        sequence.append(paths)

    sequence_parts = []
    for part in sequence:
        tmp = ["".join(p) + "A" for p in part]
        sequence_parts.append(tmp)

    return sequence_parts


memory = {}


def min_cost(seq, depth) -> int | Any:
    """Calculates the minimum cost of navigating through a sequence of
    directional paths with a specified depth.

    Recursively computes the minimum cost of traversing a sequence using
    memoization to optimize performance. The function explores different
    path variations and determines the lowest total cost within the given
    depth constraint.

    Args:
        seq (Iterable[str]): A sequence of directional identifiers to navigate.
        depth (int): The maximum recursion depth for path exploration.

    Returns:
        Union[int, Any]: The minimum cost of navigating the sequence within
            the specified depth.
    """

    if depth == 0:
        return len(seq)

    if (seq, depth) in memory:
        return memory[(seq, depth)]

    sub_sequences = solve_directional(seq)

    cost = sum(min(min_cost(seq, depth - 1) for seq in part) for part in sub_sequences)
    memory[(seq, depth)] = cost
    return cost


def part1(lines: list[str]) -> int:
    """ """
    depth = 2

    tot = 0
    for num in lines:
        sequence = solve_numeric(num)

        seq_tot = sum(min(min_cost(seq, depth) for seq in part) for part in sequence)

        print(f"{num=} → {sequence=}, {seq_tot=}")
        tot += int(num[:-1]) * seq_tot

    return tot


def part2(lines: list[str]) -> int:
    """ """
    depth = 25

    tot = 0
    for num in lines:
        sequence = solve_numeric(num)

        seq_tot = sum(min(min_cost(seq, depth) for seq in part) for part in sequence)
        tot += int(num[:-1]) * seq_tot

    return tot


def main():
    loader = LoaderLib(2024)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(21)
    else:
        input_text = dedent(
            """\
                029A
                980A
                179A
                456A
                379A
            """
        ).strip("\n")
    # lines = [
    #     (extract_ints(param)) for param in [line for line in lines_to_list(input_text)]
    # ]
    # lines = [lines_to_list(line) for line in input_text.split("\n\n")]
    lines = lines_to_list(input_text)

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
    # --  Expected Results  --
    """
    +---------------------+-----------------------+------------------+
    | Example 029A:                                                  |
    +---------------------+-----------------------+------------------+
    | Tier 1              | Tier 2                | Tier 3           |
    | press: | result:    | press:   | result:    | press: | result: |
    +--------+------------+----------+------------+--------+---------+
    |    <   | A → ^      |          |            |        |         |
    |    v   | ^ → v      |          |            |        |         |
    |    A   | [press]    | v        | A → >      |        |         |
    |    <   | v → <      |          |            |        |         |
    |    A   | [press]    | <        | > → v      |        |         |
    |    A   | [press]    | <        | v → <      |        |         |
    |    >   | < → v      |          |            |        |         |
    |    >   | v → >      |          |            |        |         |
    |    ^   | > → A      |          |            |        |         |
    |    A   | [press]    | A        | [press]    | <      | A → 0   |
    |    v   | A → >      |          |            |        |         |
    |    A   | [press]    | >        | < → v      |        |         |
    |    A   | [press]    | >        | v → >      |        |         |
    |    <   | > → v      |          |            |        |         |
    |    ^   | v → ^      |          |            |        |         |
    |    A   | [press]    | ^        | > → A      |        |         |
    |    >   | ^ → A      |          |            |        |         |
    |    A   | [press]    | A        | [press]    | A      | [press] |
    |    <   | A → ^      |          |            |        |         |
    |    v   | ^ → v      |          |            |        |         |
    |    <   | v → <      |          |            |        |         |
    |    A   | [press]    | <        | A → ^      |        |         |
    |    >   | < → v      |          |            |        |         |
    |    >   | v → >      |          |            |        |         |
    |    ^   | > → A      |          |            |        |         |
    |    A   | [press]    | A        | [press]    | ^      | 0 → 2   |
    |    v   | A → >      |          |            |        |         |
    |    A   | [press]    | >        | ^ → A      |        |         |
    |    ^   | > → A      |          |            |        |         |
    |    A   | [press]    | A        | [press]    | A      | [press] |
    |    <   | A → ^      |          |            |        |         |
    |    v   | ^ → v      |          |            |        |         |
    |    A   | [press]    | v        | A → >      |        |         |
    |    >   | v → >      |          |            |        |         |
    |    ^   | > → A      |          |            |        |         |
    |    A   | [press]    | A        | [press]    | >      | 2 → 3   |
    |    <   | A → ^      |          |            |        |         |
    |    v   | ^ → v      |          |            |        |         |
    |    <   | v → <      |          |            |        |         |
    |    A   | [press]    | <        | > → v      |        |         |
    |    >   | < → v      |          |            |        |         |
    |    ^   | v → ^      |          |            |        |         |
    |    A   | [press]    | ^        | v → ^      |        |         |
    |    >   | ^ → A      |          |            |        |         |
    |    A   | [press]    | A        | [press]    | ^      | 3 → 6   |
    |    A   | [press]    | A        | [press]    | ^      | 6 → 9   |
    |    v   | A → >      |          |            |        |         |
    |    A   | [press]    | >        | ^ → A      |        |         |
    |    ^   | > → A      |          |            |        |         |
    |    A   | [press]    | A        | [press]    | A      | [press] |
    |    <   | A → ^      |          |            |        |         |
    |    v   | ^ → v      |          |            |        |         |
    |    <   | v → <      |          |            |        |         |
    |    A   | [press]    | <        | A → ^      |        |         |
    |    >   | < → v      |          |            |        |         |
    |    A   | [press]    | v        | ^ → v      |        |         |
    |    >   | v → >      |          |            |        |         |
    |    ^   | > → A      |          |            |        |         |
    |    A   | [press]    | A        | [press]    | v      | 9 → 6   |
    |    A   | [press]    | A        | [press]    | v      | 6 → 3   |
    |    A   | [press]    | A        | [press]    | v      | 3 → A   |
    |    v   | A → >      |          |            |        |         |
    |    A   | [press]    | >        | < → v      |        |         |
    |    <   | > → v      |          |            |        |         |
    |    ^   | v → ^      |          |            |        |         |
    |    A   | [press]    | ^        | > → A      |        |         |
    |    >   | ^ → A      |          |            |        |         |
    |    A   | [press]    | A        | [press]    | A      | [press] |
    +--------+------------+----------+------------+--------+---------+
    """
    # --------------------------------------------------------------------------------
    #  LAP -> 0.000140        |        0.000140 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : len(lines)=5 ...
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    #  LAP -> 0.000437        |        0.000577 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 164960
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    #  LAP -> 0.001765        |        0.002343 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 205620604017764
    # --------------------------------------------------------------------------------
