"""
Advent of code 2025
Day 12: Christmas Tree Farm

Okay, I was expecting a part two… so I did a lot more than ended up being
necessary for part one. Ha! Thanks, Eric; I needed to spend more time
thinking about this problem. :)

Fun fact: I didn't solve the problem with the test data, I tried the full
input just to find out what it was like. I didn't have the heart to pull
all that coding to pieces again afterwards.

Onward to 2026!?
"""
from dataclasses import dataclass
from textwrap import dedent

from aoc.loader import LoaderLib

presents = {}
regions = []


@dataclass
class Region:
    """
    Represents a region on the Christmas tree farm with its dimensions and present requirements.
    Provides properties to calculate the area, present occupancy, and whether all presents can fit.

    Attributes:
        width: The width of the region.
        length: The length of the region.
        present_list_counts: List of counts for each present type required in the region.
    """
    width: int
    length: int
    present_list_counts: list[int]

    @property
    def area(self):
        return self.width * self.length

    @property
    def present_occupancy(self):
        return sum(count * len(presents[i]) for i, count in enumerate(self.present_list_counts))

    @property
    def could_fit(self):
        return self.area > self.present_occupancy


def parse_input(input_text: str):
    """
    Parses the input text and extracts present and region definitions.
    Returns dictionaries of present shapes and a list of region requirements.

    Args:
        input_text: The raw input string containing present and region definitions.

    Returns:
        tuple: A dictionary of presents and a list of Region objects.
    """
    # The input has two sections. The first section is a list of presents starting with their index and a colon.
    # Line one of the present definition is the present index followed by a colon. That is followed by a series of lines
    # representing the present. Each line is a series of # and . characters representing the present. A blank line ends
    # the present definition.
    # The second section is a list of regions. 
    # Region definitions begin with their size in the format "[width]x[length]". The size is followed by a colon.
    # On the same line thereafter is listed the number of presents of each type that should be accommodated in the area.
    # In order, there is an index for each present type: the first number represents the number of type 0 presents, the
    # second number represents the number of type 1 presents, and so on.
    line_groups = input_text.split("\n\n")
    presents_section = line_groups[:-1]
    regions_section = line_groups[-1].split("\n")

    make_presents(presents_section)
    make_regions(regions_section)

    return presents, regions


def make_regions(regions_section: list[str]):
    """
    Parses the region definitions and adds Region objects to the regions list.
    Each region specifies its size and the number of presents of each type it must accommodate.

    Args:
        regions_section: List of strings, each containing the definition of a region.

    Returns:
        None
    """
    for line in regions_section:
        region_size, region_present_counts = line.split(":")
        region_size = list(map(int, region_size.split("x")))
        region_present_counts = list(map(int, region_present_counts.split()))
        regions.append(Region(width=region_size[0], length=region_size[1], present_list_counts=region_present_counts))


def make_presents(presents_section: list[str]):
    """
    Parses the present definitions and populates the presents dictionary with their shapes.
    Each present is represented as a set of coordinates where its shape occupies space.

    Args:
        presents_section: List of strings, each containing the definition of a present.

    Returns:
        None
    """
    for section in presents_section:
        lines = section.splitlines()
        present_index = int(lines[0].strip(': '))
        present_lines = lines[1:]
        presents[present_index] = set()
        for y, line in enumerate(present_lines):
            for x, char in enumerate(line):
                if char == '#':
                    presents[present_index].add((x, y))


def part1(presents, regions) -> int:
    """
    Calculates the total number of regions that could fit all their assigned presents.
    Returns the count of regions where the available area exceeds the present occupancy.

    Args:
        presents: Dictionary mapping present indices to their shapes.
        regions: List of Region objects representing areas and present requirements.

    Returns:
        int: The number of regions that can accommodate all assigned presents.
    """
    return sum(region.could_fit for region in regions)


def part2(presents, regions) -> int:
    ...


def main():
    loader = LoaderLib(2025)
    testing = not True
    if not testing:
        input_text = loader.get_aoc_input(12)
    else:
        input_text = dedent(
            """\
                0:
                ###
                ##.
                ##.
                
                1:
                ###
                ##.
                .##
                
                2:
                .##
                ###
                ##.
                
                3:
                ##.
                ###
                ##.
                
                4:
                ###
                #..
                ###
                
                5:
                ###
                .#.
                ###
                
                4x4: 0 0 0 0 2 0
                12x5: 1 0 1 0 2 2
                12x5: 1 0 1 0 3 2
            """
        ).strip("\n")
    # lines = [(extract_ints(param)) for param in list(lines_to_list(input_text))]
    # lines = [lines_to_list(line) for line in input_text.split("\n\n")]
    # lines = lines_to_list(input_text)
    # lines = input_text.split(',')
    presents, regions = parse_input(input_text)

    loader.print_solution("setup", f"{len(presents)=} {len(regions)=} ...")
    loader.print_solution(
        1,
        part1(
            presents, regions
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
            presents, regions,
        ),
    )


if __name__ == "__main__":
    main()
    # --
    # --------------------------------------------------------------------------------
    #  LAP -> 0.002778        |        0.002778 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : len(presents)=6 len(regions)=1000 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.001073        |        0.003850 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 414
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.000021        |        0.003872 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : None
    # --------------------------------------------------------------------------------
