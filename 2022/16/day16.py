"""
Advent of code 2022
Day 16: Proboscidea Volcanium
"""
import re
from textwrap import dedent
from typing import Dict, Union

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list

global Valves
Valves: Dict[str, Dict[str, Union[int, tuple, dict]]]


def part1() -> int:
    """
    Valves is a dictionary of valve names containing tuples giving
    the pressure release (per minute) and a list of exits to other
    Valves available
    """
    best = 0

    def search(opened, flowed, current_room, depth_to_go):
        nonlocal best
        if flowed > best:
            best = flowed

        if depth_to_go <= 0:
            return

        if current_room not in opened:
            search(opened.union([current_room]),
                   flowed + Valves[current_room]['rate'] * depth_to_go,
                   current_room,
                   depth_to_go - 1)
        else:
            for k in [x for x in Valves[current_room]['exits'].keys() if x not in opened]:
                search(opened,
                       flowed,
                       k,
                       depth_to_go - Valves[current_room]['exits'][k])

    search({'AA'}, 0, 'AA', 29)

    return best


def part2() -> int:
    """
    """
    best = 0

    def search(opened, flowed, current_room, depth_to_go, elephants_turn):
        nonlocal best
        if flowed > best:
            best = flowed

        if depth_to_go <= 0:
            return

        if current_room not in opened:
            search(opened.union([current_room]), flowed + Valves[current_room]['rate'] * depth_to_go, current_room,
                   depth_to_go - 1, elephants_turn)
            if not elephants_turn:
                search({current_room}.union(opened), flowed + Valves[current_room]['rate'] * depth_to_go, 'AA', 25,
                       True)
        else:
            for k in [x for x in Valves[current_room]['exits'].keys() if x not in opened]:
                search(opened, flowed, k, depth_to_go - Valves[current_room]['exits'][k], elephants_turn)

    search({'AA'}, 0, 'AA', 25, False)

    return best


def main():
    global Valves
    loader = LoaderLib(2022)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(16)
    else:
        # input_text = (Path.cwd() / 'testdata.txt').read_text().strip('\n')
        input_text = dedent('''\
            Valve AA has flow rate=0; tunnels lead to Valves DD, II, BB
            Valve BB has flow rate=13; tunnels lead to Valves CC, AA
            Valve CC has flow rate=2; tunnels lead to Valves DD, BB
            Valve DD has flow rate=20; tunnels lead to Valves CC, AA, EE
            Valve EE has flow rate=3; tunnels lead to Valves FF, DD
            Valve FF has flow rate=0; tunnels lead to Valves EE, GG
            Valve GG has flow rate=0; tunnels lead to Valves FF, HH
            Valve HH has flow rate=22; tunnel leads to valve GG
            Valve II has flow rate=0; tunnels lead to Valves AA, JJ
            Valve JJ has flow rate=21; tunnel leads to valve II
        ''').strip('\n')

    Valves = {}
    for line in lines_to_list(input_text):
        matches = re.match(
            r'Valve (\w+) has flow rate=(\d+); tunnels? leads? to Valves? ([A-Z, ]*)',
            line,
            re.IGNORECASE
        )
        if matches:
            valve, rate, destinations = matches.groups()
            Valves[valve] = {'rate': int(rate), 'valves': destinations.split(', '), 'exits': {}}
        else:
            raise SyntaxError(f'Something wrong with line: {line}')

    # Work out valid paths using the bfs algorithm
    def local_bfs(frontier, end):
        depth = 1
        while True:
            next_frontier = set()
            for x in frontier:
                if x == end:
                    return depth
                for y in Valves[x]['valves']:
                    next_frontier.add(y)
            frontier = next_frontier
            depth += 1

    keys = sorted([x for x in list(Valves.keys()) if Valves[x]['rate'] != 0])
    # nodes = {k: Node(v) for k, v in Valves.items()}
    for k in keys + ['AA']:
        for k2 in keys:
            if k2 != k:
                Valves[k]['exits'][k2] = local_bfs(Valves[k]['valves'], k2)

    loader.print_solution('setup', f'{len(Valves)} ...')
    loader.print_solution(1, part1())
    loader.print_solution(2, part2())


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.035866        |        0.035866 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 58 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 2.446590        |        2.482455 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 1659
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 1716.185693     |     1718.668149 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 2382
    # --------------------------------------------------------------------------------
