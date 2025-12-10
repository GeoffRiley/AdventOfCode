"""
Advent of code 2025
Day 10: Factory
"""
import re
from dataclasses import dataclass
from itertools import combinations
from textwrap import dedent

import scipy

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list

MACHINE_ON = '#'
MACHINE_OFF = '.'
LAMP_STATE_SWAP = {MACHINE_ON: MACHINE_OFF, MACHINE_OFF: MACHINE_ON}


# A structure that will store the required light configuration,
# the (multiple) button definitions, and the joltage requirements.
@dataclass
class Machine:
    lights: str
    buttons: list[tuple[int, ...]]
    joltage_requirements: list[tuple[int, ...]]

    def __post_init__(self):
        self._ensure_parsed_inputs()
        self.reset()
        self._precompute_masks()

    def _ensure_parsed_inputs(self):
        if isinstance(self.buttons, str):
            self.buttons = sorted([tuple(map(int, s.split(","))) for s in self.buttons.strip('() ').split(") (")])
        if isinstance(self.joltage_requirements, str):
            self.joltage_requirements = list(map(int, self.joltage_requirements.split(",")))

    def _precompute_masks(self):
        # Precompute bitmasks for Part 1
        self.target_mask = 0
        for i, char in enumerate(self.lights):
            if char == MACHINE_ON:
                self.target_mask |= (1 << i)

        self.button_masks = []
        for btn in self.buttons:
            mask = 0
            for light_idx in btn:
                mask |= (1 << light_idx)
            self.button_masks.append(mask)

    @classmethod
    def from_string(cls, line: str):
        # Split the line into the lights, buttons, and joltage requirements.
        # Format: "[lights] (buttons) (buttons) (buttons) ... {joltage_requirements}"
        r = re.match(r"\[(.+)]\s+(\(.+\)\s+)\{(.+)}", line)
        return cls(*r.groups())

    def reset(self):
        self.current_lights = MACHINE_OFF * len(self.lights)
        self.current_joltage = [0] * len(self.joltage_requirements)

    @property
    def button_count(self):
        return len(self.buttons)

    @property
    def lamp_activated(self):
        return self.current_lights == self.lights

    @property
    def joltage_activated(self):
        return all(
            self.joltage_requirements[i] == self.current_joltage[i] for i in range(len(self.joltage_requirements)))

    def use_lamp_button(self, button_num: int):
        if button_num >= self.button_count:
            raise IndexError(f"Button number {button_num} is out of range.")
        for light_num in self.buttons[button_num]:
            self.current_lights = (self.current_lights[:light_num]
                                   + LAMP_STATE_SWAP[self.current_lights[light_num]]
                                   + self.current_lights[light_num + 1:])

    def joltage_solve(self) -> int:
        joltage_list = self.joltage_requirements
        num_reqs = len(joltage_list)
        num_buttons = self.button_count

        button_list = self._build_optimization_matrix(num_reqs, num_buttons)

        equn = scipy.optimize.linprog([1] * self.button_count,
                                      A_eq=button_list,
                                      b_eq=joltage_list,
                                      bounds=(0, None),
                                      method="highs",
                                      integrality=1)
        return round(equn.fun)

    def _build_optimization_matrix(self, num_reqs: int, num_buttons: int) -> list[list[int]]:
        # Optimized matrix construction
        button_list = [[0] * num_buttons for _ in range(num_reqs)]
        for btn_idx, btn_tuple in enumerate(self.buttons):
            for req_idx in btn_tuple:
                if req_idx < num_reqs:
                    button_list[req_idx][btn_idx] = 1
        return button_list


def part1(machines: list[Machine]) -> int:
    return sum(count_buttons(machine) for machine in machines)


def count_buttons(machine: Machine) -> int:
    target = machine.target_mask
    button_masks = machine.button_masks
    n_buttons = len(button_masks)

    # Use range(n_buttons + 1) to include the case where all buttons are pressed
    for count in range(n_buttons + 1):
        for combo in combinations(button_masks, r=count):
            # Calculate the result of pressing these buttons using XOR
            current = 0
            for m in combo:
                current ^= m

            if current == target:
                return count
    raise ValueError("No solution found.")


def part2(machines: list[Machine]) -> int:
    return sum(machine.joltage_solve() for machine in machines)


def main():
    loader = LoaderLib(2025)
    testing = not True
    if not testing:
        input_text = loader.get_aoc_input(10)
    else:
        input_text = dedent(
            """\
                [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
                [...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
                [.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
            """
        ).strip("\n")
    # lines = [(extract_ints(param)) for param in list(lines_to_list(input_text))]
    # lines = [lines_to_list(line) for line in input_text.split("\n\n")]
    lines = lines_to_list(input_text)
    # lines = input_text.split(',')
    machines = [Machine.from_string(line) for line in lines]

    loader.print_solution("setup", f"{len(lines)=} ...")
    loader.print_solution(
        1,
        part1(
            machines,
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
            machines,
        ),
    )


if __name__ == "__main__":
    main()
    # --
    # --------------------------------------------------------------------------------
    #  LAP -> 0.002762        |        0.002762 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : len(lines)=151 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.005920        |        0.008681 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 428
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.482765        |        0.491446 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 16613
    # --------------------------------------------------------------------------------
