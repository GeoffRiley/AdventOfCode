"""
Advent of code 2023
Day 15: Lens Library
"""
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import to_list


def do_hash(string: str) -> int:
    """
    Calculate the hash of a string.
    """
    hsh = 0
    for char in string:
        hsh += ord(char)
        hsh *= 17
        hsh %= 256
    return hsh


def part1(lines: list[str]) -> int:
    """
    Calulate the hash for each string and return the sum of all hashes.
    """
    running_total = 0
    for element in lines:
        running_total += do_hash(element)

    return running_total


def part2(lines: list[str]) -> int:
    """
    We have 256 lens boxes. Each ready to take one or more lenses.
    Our command string is a list of instructions on how to place lenses into
    the boxes. Each instruction takes the form of a multi character label, a
    function, either '=' or '-', and an integer in the case of the '='
    function.
    """
    lens_boxes = [{} for _ in range(256)]
    for element in lines:
        if "=" in element:
            # place a lens in a box
            box_label, focal_length = element.split("=")
            focal_length = int(focal_length)
            box_number = do_hash(box_label)
            if box_number >= 256:
                raise ValueError(f"Invalid box number: {box_number}")
            lens_boxes[box_number][box_label] = focal_length
        elif "-" in element:
            # remove a lens from a box
            box_label = element.strip("-")
            box_number = do_hash(box_label)
            if box_number >= 256:
                raise ValueError(f"Invalid box number: {box_number}")
            if box_label in lens_boxes[box_number]:
                lens_boxes[box_number].pop(box_label)
        else:
            raise ValueError(f"Invalid command: {element}")
    # calculate the total focal length of all lenses in all boxes
    total_focal_length = 0
    for box in range(len(lens_boxes)):
        for n, focal_length in enumerate(lens_boxes[box].values(), start=1):
            total_focal_length += (box + 1) * (n) * (focal_length)

    return total_focal_length


def main():
    loader = LoaderLib(2023)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(15)
    else:
        input_text = dedent(
            """\
            rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
            """
        ).strip("\n")
    # lines = [
    #     (pat, to_list_int(param))
    #     for pat, param in [line.split() for line in lines_to_list(input_text)]
    # ]
    # lines = [lines_to_list(line) for line in input_text.split("\n\n")]
    lines = to_list(input_text)

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
    #  LAP -> 0.000330        |        0.000330 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : len(lines)=4000 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.000977        |        0.001307 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 515210
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.001523        |        0.002830 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 246762
    # --------------------------------------------------------------------------------
