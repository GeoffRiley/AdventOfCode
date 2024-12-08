"""
Advent of code 2023
Day 20: Pulse Propagation
"""

from collections import deque
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list

# Define constants for pulse types
LOW = "low"
HIGH = "high"


# Define Module classes
class Module:
    def __init__(self, name):
        self.name = name
        self.outputs = []  # Destination module names
        self.inputs = []  # Source module names

    def reset(self):
        pass  # To be overridden in subclasses

    def copy(self):
        pass  # To be overridden in subclasses

    def receive_pulse(self, pulse_type, source_module, pulse_queue, pulse_counts):
        pass  # To be overridden in subclasses

    def get_state(self):
        pass  # To be overridden in subclasses

    def set_state(self, state):
        pass  # To be overridden in subclasses


class FlipFlopModule(Module):
    def __init__(self, name):
        super().__init__(name)
        self.state = False  # Initially off

    def reset(self):
        self.state = False

    def copy(self):
        new_module = FlipFlopModule(self.name)
        new_module.outputs = self.outputs[:]
        new_module.inputs = self.inputs[:]
        new_module.state = self.state
        return new_module

    def receive_pulse(self, pulse_type, source_module, pulse_queue, pulse_counts):
        if pulse_type == HIGH:
            return
        # Toggle state
        self.state = not self.state
        # Send pulse based on new state
        new_pulse_type = HIGH if self.state else LOW
        pulse_counts[new_pulse_type] += len(self.outputs)
        for dest_module in self.outputs:
            pulse_queue.append((new_pulse_type, dest_module, self.name))

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state


class ConjunctionModule(Module):
    def __init__(self, name):
        super().__init__(name)
        self.memory = {}  # {input_module_name: pulse_type}

    def reset(self):
        self.memory = {}

    def copy(self):
        new_module = ConjunctionModule(self.name)
        new_module.outputs = self.outputs[:]
        new_module.inputs = self.inputs[:]
        new_module.memory = self.memory.copy()
        return new_module

    def receive_pulse(self, pulse_type, source_module, pulse_queue, pulse_counts):
        # Update memory
        self.memory[source_module] = pulse_type
        # Initialize memory for new inputs
        for input_module in self.inputs:
            if input_module not in self.memory:
                self.memory[input_module] = LOW
        # Determine pulse to send
        new_pulse_type = LOW if all(p == HIGH for p in self.memory.values()) else HIGH
        pulse_counts[new_pulse_type] += len(self.outputs)
        for dest_module in self.outputs:
            pulse_queue.append((new_pulse_type, dest_module, self.name))

    def get_state(self):
        # Represent state as sorted tuple of (input_module_name, pulse_type)
        return tuple(sorted(self.memory.items()))

    def set_state(self, state):
        self.memory = dict(state)


class BroadcasterModule(Module):
    def copy(self):
        new_module = BroadcasterModule(self.name)
        new_module.outputs = self.outputs[:]
        new_module.inputs = self.inputs[:]
        return new_module

    def receive_pulse(self, pulse_type, source_module, pulse_queue, pulse_counts):
        pulse_counts[pulse_type] += len(self.outputs)
        for dest_module in self.outputs:
            pulse_queue.append((pulse_type, dest_module, self.name))


class UntypedModule(Module):
    def copy(self):
        new_module = UntypedModule(self.name)
        new_module.outputs = self.outputs[:]
        new_module.inputs = self.inputs[:]
        return new_module

    def receive_pulse(self, pulse_type, source_module, pulse_queue, pulse_counts):
        pass  # Do nothing


# Parse module configuration
def parse_configuration(config_lines):
    modules = {}
    for line in config_lines:
        line = line.strip()
        if not line or "->" not in line:
            continue
        left, right = line.split("->")
        left = left.strip()
        right = right.strip()
        if left.startswith("%"):
            module_name = left[1:].strip()
            module = FlipFlopModule(module_name)
        elif left.startswith("&"):
            module_name = left[1:].strip()
            module = ConjunctionModule(module_name)
        elif left == "broadcaster":
            module_name = "broadcaster"
            module = BroadcasterModule(module_name)
        else:
            module_name = left
            module = UntypedModule(module_name)
        if module_name not in modules:
            modules[module_name] = module
        else:
            module = modules[module_name]
        # Parse destinations
        destinations = [dest.strip() for dest in right.split(",")]
        module.outputs.extend(destinations)
    # Build inputs mapping
    module_names = list(
        modules.keys()
    )  # Make a list of module names to avoid modifying the dictionary during iteration
    for module_name in module_names:
        module = modules[module_name]
        for dest_name in module.outputs:
            if dest_name not in modules:
                dest_module = UntypedModule(dest_name)
                modules[dest_name] = dest_module
            else:
                dest_module = modules[dest_name]
            dest_module.inputs.append(module.name)
    return modules


# Simulate the pulses
def simulate_pulses(modules, num_presses=1):
    pulse_counts = {LOW: 0, HIGH: 0}
    pulse_queue = []
    for _ in range(num_presses):
        # Reset the pulse queue
        pulse_queue.append((LOW, "broadcaster", "button"))
        pulse_counts[LOW] += 1  # Count the pulse sent by the button
        # Keep track of pulses received by rx
        while pulse_queue:
            pulse_type, dest_module_name, source_module_name = pulse_queue.pop(0)
            dest_module = modules[dest_module_name]
            dest_module.receive_pulse(
                pulse_type, source_module_name, pulse_queue, pulse_counts
            )
        # Wait until all pulses have been processed before next button press
    return pulse_counts


# BFS to find minimal button presses to send a low pulse to 'rx'
def bfs_min_presses_to_rx(modules, flag_module="rx"):
    # Initial state: all modules in default state
    initial_modules_state = {}
    for name, module in modules.items():
        module.reset()
        initial_modules_state[name] = module.copy()

    # Queue items: (button_presses, modules_state)
    queue = deque()
    visited_states = set()
    pulse_counts = {LOW: 0, HIGH: 0}

    # Helper function to get a hashable representation of the modules state
    def get_modules_state_hash(modules_state):
        state = []
        for name in sorted(modules_state.keys()):
            module = modules_state[name]
            if isinstance(module, FlipFlopModule):
                state.append((name, module.get_state()))
            elif isinstance(module, ConjunctionModule):
                state.append((name, module.get_state()))
            # Untyped and broadcaster modules do not have state
        return tuple(state)

    # Start BFS
    initial_state_hash = get_modules_state_hash(initial_modules_state)
    queue.append((0, initial_modules_state))
    visited_states.add(initial_state_hash)

    while queue:
        button_presses, current_modules_state = queue.popleft()
        button_presses += 1

        # Copy the modules for the new state
        new_modules_state = {
            name: module.copy() for name, module in current_modules_state.items()
        }

        # Simulate one button press
        pulse_queue = deque()
        pulse_queue.append((LOW, "broadcaster", "button"))

        rx_received_low_pulse = False

        while pulse_queue:
            pulse_type, dest_module_name, source_module_name = pulse_queue.popleft()
            dest_module = new_modules_state[dest_module_name]

            # If dest_module is 'rx', check if it receives a low pulse
            if dest_module_name == flag_module:
                if pulse_type == LOW:
                    rx_received_low_pulse = True
                    break  # We can stop processing further pulses
                else:
                    continue  # rx ignores high pulses
            dest_module.receive_pulse(
                pulse_type, source_module_name, pulse_queue, pulse_counts
            )

        if rx_received_low_pulse:
            return button_presses

        # Get the state hash
        state_hash = get_modules_state_hash(new_modules_state)
        if state_hash in visited_states:
            continue  # Already visited this state
        visited_states.add(state_hash)
        # Add the new state to the queue
        queue.append((button_presses, new_modules_state))

    # If we exit the loop, rx cannot receive a low pulse
    return None


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    return a * b // gcd(a, b)


# Function to compute LCM of a list of numbers
def compute_lcm(numbers):
    from functools import reduce

    return reduce(lcm, numbers)


def find_conjunctions_affecting_rx(modules):
    # modules: dict[module_name: module_object]
    # each module_object has: .inputs (list of sources), .type (maybe 'flipflop', 'conjunction', 'broadcaster', 'untyped')

    # target is "rx" but that is fed directly from "ls", so
    # track that instead
    target = modules["rx"].inputs[0]
    if target not in modules:
        return []

    mod = modules[target]
    stack = list(mod.inputs)
    visited = set()
    conjunctions_impacting_rx = []

    while stack:
        current = stack.pop(0)
        if current in visited:
            continue
        visited.add(current)

        mod = modules[current]
        # Determine if it's a conjunction module
        # Depending on how you stored it, you might have:
        # if isinstance(mod, ConjunctionModule):
        # or if you stored type info in mod.type
        if hasattr(mod, "memory"):  # or another property unique to conjunction modules
            conjunctions_impacting_rx.append(current)
        else:
            # Add all input modules to the stack
            for inp in mod.inputs:
                if inp not in visited:
                    stack.append(inp)

    return conjunctions_impacting_rx


def part1(modules: list[Module]) -> int:
    """ """
    # Simulate pulses for 1000 button presses
    num_presses = 1000
    pulse_counts = simulate_pulses(modules, num_presses)
    # Output the result
    total_low = pulse_counts[LOW]
    total_high = pulse_counts[HIGH]
    return total_low * total_high


def part2(modules: list[Module]) -> int:
    """
    How many button presses until rx goes low.

    Examining the input, rx is fed purely from a Conjunction (ls).
    ls received inputs from four conjunctions: tx, dd, nz and ph

    If we can work out the period of each of the four conjunctions,
    then perhaps that will give values that can be used to find a
    least common multiple: "the answer"?
    """
    # Reset all module states
    for module in modules.values():
        module.reset()

    target_conjuntions = find_conjunctions_affecting_rx(modules)

    # Keep pressing the button until rx receives a low pulse
    presses_rec = []
    for mod_name in target_conjuntions:
        button_presses = bfs_min_presses_to_rx(modules, mod_name)
        presses_rec.append(button_presses)

    return compute_lcm(presses_rec)


def main():
    loader = LoaderLib(2023)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(20)
    else:
        input_text = dedent(
            """\
                broadcaster -> a
                %a -> inv, con
                &inv -> b
                %b -> con
                &con -> output
            """
            # """\
            #     broadcaster -> a, b, c
            #     %a -> b
            #     %b -> c
            #     %c -> inv
            #     &inv -> a
            # """
        ).strip("\n")
    # lines = [
    #     (pat, to_list_int(param))
    #     for pat, param in [line.split()
    #         for line in lines_to_list(input_text)]
    # ]
    # lines = [lines_to_list(line) for line in input_text.split("\n\n")]
    lines = lines_to_list(input_text)

    modules = parse_configuration(lines)

    loader.print_solution("setup", f"{len(modules)=} ...")
    loader.print_solution(
        1,
        part1(
            modules,
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
            modules,
        ),
    )


if __name__ == "__main__":
    main()
    # --
    # --------------------------------------------------------------------------------
    # LAP -> 0.000767        |        0.000767 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : len(modules)=59 ...
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.016994        |        0.017761 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 869395600
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.990013        |        1.007774 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 2   : 232605773145467
    # --------------------------------------------------------------------------------
