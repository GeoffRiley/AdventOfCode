"""
Advent of code 2024
Day 19: Linen Layout
"""

from collections import deque
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


class AhoNode:
    def __init__(self):
        # edges for each character; since we have w,u,b,r,g, we can store in a dict or array
        self.edges = {}
        self.fail = None  # failure link
        self.output = []  # list of pattern IDs that end at this node


def build_automaton(patterns):
    # 1. Build trie
    root = AhoNode()
    for pattern_id, pattern in enumerate(patterns):
        current = root
        for ch in pattern:
            if ch not in current.edges:
                current.edges[ch] = AhoNode()
            current = current.edges[ch]
        # Mark the end of a pattern
        current.output.append(pattern_id)

    # 2. Build failure links using BFS
    queue = deque()
    # Set failure link for root to itself or None, and children of root
    # Typically root.fail = root, but None is also used; we just handle that logic later.
    root.fail = root
    for ch, node in root.edges.items():
        node.fail = root
        queue.append(node)

    # BFS to assign failure links
    while queue:
        current = queue.popleft()
        for ch, next_node in current.edges.items():
            # Find the failure link for this next_node
            f = current.fail
            while f is not root and ch not in f.edges:
                f = f.fail
            f = f.edges[ch] if ch in f.edges else root
            next_node.fail = f
            # If the fail node has output patterns, inherit them
            next_node.output += f.output
            queue.append(next_node)

    return root


def can_form_design(design, patterns):
    # dp[i] will be True if the substring design[:i] can be formed
    # by concatenating one or more patterns from the list
    dp = [False] * (len(design) + 1)
    dp[0] = True  # Empty string can always be formed

    for i in range(len(design)):
        if dp[i]:
            for pat in patterns:
                # Check if the current pattern matches the substring
                # starting at position i
                if design[i:].startswith(pat):
                    dp[i + len(pat)] = True

    return dp[len(design)]


def next_state(root, current_node, ch):
    # Follow fail links if no direct edge is found
    while current_node != root and ch not in current_node.edges:
        current_node = current_node.fail
    # If there's a valid edge, follow it; otherwise, we're at the root
    current_node = current_node.edges[ch] if ch in current_node.edges else root
    return current_node


def patterns_ending_here(state, pattern_lengths):
    # Convert pattern IDs to pattern lengths (or just return IDs if you prefer)
    return [pattern_lengths[pid] for pid in state.output]


def count_ways(design, root, pattern_lengths):
    dp = [0] * (len(design) + 1)
    dp[0] = 1
    current_node = root

    for i, ch in enumerate(design):
        # Advance to the next state in the automaton
        current_node = next_state(root, current_node, ch)

        # For each pattern that ends here, update dp
        for plen in patterns_ending_here(current_node, pattern_lengths):
            start_idx = i - plen + 1
            dp[i + 1] += dp[start_idx]

    return dp[len(design)]


def part1(lines: list[str]) -> int:
    """
    The first line of the input contains a comma-separated list of colour
    combinations. These are the colours that are allowed to be next to each
    other.
    The following lines contain strings of colours.
    The strings are the required colours to be assembled, in order, from the
    allowed colours.
    It may not be possible to assemble some of the strings.

    The first part of this puzzle is to determine how many strings can be
    assembled from the allowed colours.
    """
    allowed_colours = sorted(
        lines[0][0].split(", "), key=lambda x: len(x), reverse=True
    )
    strings = lines[1]
    return sum(bool(can_form_design(string, allowed_colours)) for string in strings)


def part2(lines: list[str]) -> int:
    """ """

    allowed_colours = sorted(
        lines[0][0].split(", "), key=lambda x: len(x), reverse=True
    )
    pattern_lengths = [len(pat) for pat in allowed_colours]

    root = build_automaton(allowed_colours)  # returns root of trie with failure links

    strings = lines[1]
    return sum(count_ways(string, root, pattern_lengths) for string in strings)


def main():
    loader = LoaderLib(2024)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(19)
    else:
        input_text = dedent(
            """\
                r, wr, b, g, bwu, rb, gb, br

                brwrr
                bggr
                gbbr
                rrbgbr
                ubwu
                bwurrg
                brgr
                bbrgwb
            """
        ).strip("\n")
    # lines = [
    #     (extract_ints(param)) for param in [line for line in lines_to_list(input_text)]
    # ]
    lines = [lines_to_list(line) for line in input_text.split("\n\n")]
    # lines = lines_to_list(input_text)

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
    # LAP -> 0.000141        |        0.000141 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : len(lines)=2 ...
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.507103        |        0.507244 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 287
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.010789        |        0.518033 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 2   : 571894474468161
    # --------------------------------------------------------------------------------
