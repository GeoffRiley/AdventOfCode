"""
Advent of code 2022
Day 19: Not Enough Minerals
"""
from functools import reduce
from operator import mul
from textwrap import dedent

from z3 import Int, Optimize, sat

from aoc.loader import LoaderLib

BOTS = [
    'ore',
    'clay',
    'obsidian',
    'geode',
]


def parse_blueprint(blueprint_strings):
    # Initialize an empty list to hold the component lists
    bp_list = []

    ##
    # Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore.
    #              Each obsidian robot costs 3 ore and 14 clay.
    #              Each geode robot costs 2 ore and 7 obsidian.
    # Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore.
    #              Each obsidian robot costs 3 ore and 8 clay.
    #              Each geode robot costs 3 ore and 12 obsidian.
    ##

    # Iterate through each line of the bp
    for line in blueprint_strings:
        # Split the line into a list of words
        bp_num, bp_text = line.split(': ')
        robot_lines = bp_text.split('.')
        robot_list = []
        for bot in robot_lines:
            words = bot.split()
            if len(words) <= 0:
                continue
            components = [0, 0, 0]
            # check after 'Each xxx robot costs…'
            for i in range(4, len(words)):
                if words[i] not in BOTS or not words[i - 1].isdigit():
                    continue

                ndx = BOTS.index(words[i])
                components[ndx] = int(words[i - 1])

            robot_list.append(components)
        bp_list.append(robot_list)
    return bp_list


def make_variable_set(t, product, qualifier=None):
    if qualifier is None:
        qualifier = ''
    else:
        qualifier += '_'
    return [Int(f"{product}_{qualifier}{i}") for i in range(t + 1)]


def get_geode_count(t, bp):
    #############
    # Variables #
    #############

    # Quantity of ore/clay/obsidian/geodes at each time stamp
    ore = make_variable_set(t, 'ore')
    cla = make_variable_set(t, 'cla')
    obs = make_variable_set(t, 'obs')
    geo = make_variable_set(t, 'geo')

    # Number of robots that produce ore/clay/obsidian/geodes at each time stamp
    ore_bot = make_variable_set(t, 'ore', 'r')
    cla_bot = make_variable_set(t, 'cla', 'r')
    obs_bot = make_variable_set(t, 'obs', 'r')
    geo_bot = make_variable_set(t, 'geo', 'r')

    # Number of robots to buy produce ore/clay/obsidian/geodes at each time stamp
    ore_bot_buy = make_variable_set(t, 'ore', 'br')
    cla_bot_buy = make_variable_set(t, 'cla', 'br')
    obs_bot_buy = make_variable_set(t, 'obs', 'br')
    geo_bot_buy = make_variable_set(t, 'geo', 'br')

    ###############
    # Constraints #
    ###############

    # Initial quantity of minerals is 0
    constraints = [ore[0] == 0, cla[0] == 0, obs[0] == 0, geo[0] == 0]

    # At each time stamp, the quantity of mineral is the
    # previous quantity plus the income from the robots
    # minus the cost of buying a new robot
    for i in range(1, t + 1):
        constraints.extend(
            [
                ore[i] == (ore[i - 1] + ore_bot[i - 1] - (ore_bot_buy[i - 1] * bp[0][0])
                           - (cla_bot_buy[i - 1] * bp[1][0]) - (obs_bot_buy[i - 1] * bp[2][0]) - (
                                   geo_bot_buy[i - 1] * bp[3][0])),
                cla[i] == (cla[i - 1] + cla_bot[i - 1] - (ore_bot_buy[i - 1] * bp[0][1])
                           - (cla_bot_buy[i - 1] * bp[1][1]) - (obs_bot_buy[i - 1] * bp[2][1]) - (
                                   geo_bot_buy[i - 1] * bp[3][1])),
                obs[i] == (obs[i - 1] + obs_bot[i - 1] - (ore_bot_buy[i - 1] * bp[0][2])
                           - (cla_bot_buy[i - 1] * bp[1][2]) - (obs_bot_buy[i - 1] * bp[2][2]) - (
                                   geo_bot_buy[i - 1] * bp[3][2])),
                geo[i] == (geo[i - 1] + geo_bot[i - 1]),
            ]
        )

    # Can buy only if the quantity of minerals is enough
    for i in range(1, t + 1):
        constraints.extend(
            [
                ore_bot_buy[i] * bp[0][0] <= ore[i], cla_bot_buy[i] * bp[1][0] <= ore[i],
                obs_bot_buy[i] * bp[2][0] <= ore[i], geo_bot_buy[i] * bp[3][0] <= ore[i],
                ore_bot_buy[i] * bp[0][1] <= cla[i], cla_bot_buy[i] * bp[1][1] <= cla[i],
                obs_bot_buy[i] * bp[2][1] <= cla[i], geo_bot_buy[i] * bp[3][1] <= cla[i],
                ore_bot_buy[i] * bp[0][2] <= obs[i], cla_bot_buy[i] * bp[1][2] <= obs[i],
                obs_bot_buy[i] * bp[2][2] <= obs[i], geo_bot_buy[i] * bp[3][2] <= obs[i],
            ]
        )
    # Can take a new robot if the amount of minerals is enough
    for i in range(1, t + 1):
        constraints.extend(
            [
                ore_bot[i] == ore_bot[i - 1] + ore_bot_buy[i - 1],
                cla_bot[i] == cla_bot[i - 1] + cla_bot_buy[i - 1],
                obs_bot[i] == obs_bot[i - 1] + obs_bot_buy[i - 1],
                geo_bot[i] == geo_bot[i - 1] + geo_bot_buy[i - 1],
            ]
        )

    for i in range(1, t + 1):
        constraints.extend(
            [
                ore_bot_buy[i] <= 1, cla_bot_buy[i] <= 1, obs_bot_buy[i] <= 1, geo_bot_buy[i] <= 1,
                ore[i] >= 0, cla[i] >= 0, obs[i] >= 0, geo[i] >= 0,
                ore_bot[i] >= 0, cla_bot[i] >= 0, obs_bot[i] >= 0, geo_bot[i] >= 0,
                ore_bot_buy[i] >= 0, cla_bot_buy[i] >= 0, obs_bot_buy[i] >= 0, geo_bot_buy[i] >= 0,
                ore_bot_buy[i] + cla_bot_buy[i] + obs_bot_buy[i] + geo_bot_buy[i] <= 1,
            ]
        )

    # Start with a single robot
    constraints.extend(
        [
            ore_bot[0] == 1, cla_bot[0] == 0, obs_bot[0] == 0, geo_bot[0] == 0,
            ore_bot_buy[0] == 0, cla_bot_buy[0] == 0, obs_bot_buy[0] == 0, geo_bot_buy[0] == 0,
            ore[0] == 0, cla[0] == 0, obs[0] == 0, geo[0] == 0,
        ]
    )

    #############
    # Objective #
    #############

    # maximize the quantity of geo[t] at time t
    objective = geo[t]

    #####################
    # Solve the problem #
    #####################

    solver = Optimize()
    solver.add(constraints)
    solver.maximize(objective)

    if solver.check() == sat:
        model = solver.model()
        return model[geo[t]].as_long()


def part1(bp_list) -> int:
    """
    """
    results = [get_geode_count(24, bp_list[i]) * (i + 1) for i in range(len(bp_list))]
    return sum(results)


def part2(bp_list) -> int:
    """
    """
    results = [get_geode_count(32, bp_list[i]) for i in range(min(len(bp_list), 3))]
    return reduce(mul, results)


def main():
    loader = LoaderLib(2022)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(19)
    else:
        # input_text = (Path.cwd() / 'testdata.txt').read_text().strip('\n')
        input_text = dedent('''\
            Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
            Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
        ''').strip('\n')

    bp_list = parse_blueprint(input_text.splitlines())

    loader.print_solution('setup', f'{len(bp_list)} ...')
    loader.print_solution(1, part1(bp_list))
    loader.print_solution(2, part2(bp_list))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.003986        |        0.003986 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 30 ...
    # --------------------------------------------------------------------------------
    # 
    # 
    # --------------------------------------------------------------------------------
    #  LAP -> 21.131597       |       21.135583 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 1349
    # --------------------------------------------------------------------------------
    # 
    # 
    # --------------------------------------------------------------------------------
    #  LAP -> 4.332479        |       25.468062 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 21840
    # --------------------------------------------------------------------------------
