"""
Advent of code 2023
Day 02: Cube Conundrum
"""
from dataclasses import dataclass
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


@dataclass
class TargetBag:
    red: int
    green: int
    blue: int

    def __le__(self, other):
        return (self.red <= other.red and
                self.green <= other.green and
                self.blue <= other.blue)


def part1(lines, target_bag: TargetBag):
    """
    Each line gives the result of single game.
        Game: \d+: \(\(\d+ \(red|green|blue\),?\){,3};?\)+
    Each game consists of three dice draws. The dice are coloured
    red, green or blue, and any combination may be drawn. The
    number of each colour is recorded before the colour name.
    A comma follows each colour excepting the last in a group,
    a semicolon follows each group excepting the last in a game.
    Each game is recorded upon a single line in the input.

    The target_bag contains the maximum number of each colour
    for a game to be counted.

    The sum of all valid game numbers should be returned.
    """
    game_list = []
    for line in lines:
        game, draws = line.split(':')
        # remove the word 'Game' off the front
        _, game = game.split()
        draw_list = draws.split(';')
        assert len(draw_list) >= 1
        m_colours = TargetBag(0, 0, 0)
        for draw in draw_list:
            col_list = {d.split()[1]: d.split()[0] for d in draw.split(',')}
            m_colours.red = max(m_colours.red, int(col_list.get('red', 0)))
            m_colours.green = max(m_colours.green, int(col_list.get('green', 0)))
            m_colours.blue = max(m_colours.blue, int(col_list.get('blue', 0)))
        if m_colours <= target_bag:
            game_list.append(int(game))

    return sum(game_list)


def part2(lines):
    """
    Sum of the 'proper' calibration values
    """
    game_list = []
    for line in lines:
        game, draws = line.split(':')
        # remove the word 'Game' off the front
        _, game = game.split()
        draw_list = draws.split(';')
        assert len(draw_list) >= 1
        m_colours = TargetBag(0, 0, 0)
        for draw in draw_list:
            col_list = {d.split()[1]: d.split()[0] for d in draw.split(',')}
            m_colours.red = max(m_colours.red, int(col_list.get('red', 0)))
            m_colours.green = max(m_colours.green, int(col_list.get('green', 0)))
            m_colours.blue = max(m_colours.blue, int(col_list.get('blue', 0)))
        game_list.append(m_colours.red * m_colours.green * m_colours.blue)

    return sum(game_list)


def main():
    loader = LoaderLib(2023)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(2)
    else:
        input_text = dedent('''\
            Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
            Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
            Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
            Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
            Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
            ''').strip('\n')
    target_bag = TargetBag(12, 13, 14)
    lines = lines_to_list(input_text)

    loader.print_solution('setup', f'{len(lines)} ...')
    loader.print_solution(1, part1(lines, target_bag))
    loader.print_solution(2, part2(lines))


if __name__ == '__main__':
    main()
    # --
    # --------------------------------------------------------------------------------
    #  LAP -> 0.001174        |        0.001174 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 100 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.006103        |        0.007276 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 2447
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.006320        |        0.013597 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 56322
    # --------------------------------------------------------------------------------
