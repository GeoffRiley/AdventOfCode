"""
Advent of code 2025
Day 11: Reactor
"""

from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


def part1(lines: list[str]) -> int:
    network = {}
    stack = {}

    for line in lines:
        device, outputs = line.split(': ')
        network[device] = outputs.split()

    def cycle(node: tuple[str,]) -> int:
        if node[0] == 'out':
            return 1
        if node in stack:
            return stack[node]
        stack[node] = sum(
            cycle(
                (next_node,)
            ) for next_node in network[node[0]]
        )
        return stack[node]

    return cycle(('you',))


def part2(lines: list[str]) -> int:
    network = {}
    stack = {}

    for line in lines:
        device, outputs = line.split(': ')
        network[device] = outputs.split()

    def cycle(node: tuple[str, bool, bool]) -> int | tuple[str, bool, bool]:
        if node[0] == 'out':
            return 1 if node[1] and node[2] else 0
        if node in stack:
            return stack[node]
        stack[node] = sum(
            cycle(
                (next_node,
                 node[1] or node[0] == 'dac',
                 node[2] or node[0] == 'fft')
            ) for next_node in network[node[0]]
        )
        return stack[node]

    return cycle(('svr', False, False))


def main():
    loader = LoaderLib(2025)
    testing = not True
    if not testing:
        input_text = loader.get_aoc_input(11)
    else:
        input_text = dedent(
            """\
                aaa: you hhh
                you: bbb ccc
                bbb: ddd eee
                ccc: ddd eee fff
                ddd: ggg
                eee: out
                fff: out
                ggg: out
                hhh: ccc fff iii
                iii: out
            """
        ).strip("\n")
    # lines = [(extract_ints(param)) for param in list(lines_to_list(input_text))]
    # lines = [lines_to_list(line) for line in input_text.split("\n\n")]
    lines = lines_to_list(input_text)
    # lines = input_text.split(',')

    loader.print_solution("setup", f"{len(lines)=} ...")
    loader.print_solution(
        1,
        part1(
            lines,
        ),
    )

    if testing:
        input_text = dedent(
            """\
                svr: aaa bbb
                aaa: fft
                fft: ccc
                bbb: tty
                tty: ccc
                ccc: ddd eee
                ddd: hub
                hub: fff
                eee: dac
                dac: fff
                fff: ggg hhh
                ggg: out
                hhh: out
            """
        ).strip("\n")
        lines = lines_to_list(input_text)

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
    #  LAP -> 0.000408        |        0.000408 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : len(lines)=595 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.000691        |        0.001099 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 658
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.004178        |        0.005277 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 371113003846800
    # --------------------------------------------------------------------------------
