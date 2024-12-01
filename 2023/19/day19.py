"""
Advent of code 2023
Day 19: Aplenty
"""

import operator
import re
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list


def parse_workflows(workflow_text, work_pass=1):
    workflows = {}
    pattern = re.compile(r"(\w+)\{(.*?)\}")
    for line in workflow_text:
        name, rules_str = pattern.match(line).groups()
        rules = []
        for rule_str in rules_str.split(","):
            if ":" in rule_str:
                condition_str, destination = rule_str.split(":")
                # Convert condition into a lambda function
                if work_pass == 1:
                    condition = parse_condition1(condition_str)
                else:
                    condition = parse_condition2(condition_str)
            else:
                # Last rule with no condition
                if work_pass == 1:
                    condition = lambda part: True
                else:
                    condition = None
                destination = rule_str.strip()
            rules.append((condition, destination))
        workflows[name] = rules
    return workflows


def parse_condition1(condition_str):
    ops = {">": operator.gt, "<": operator.lt, "==": operator.eq}
    for op_str, op_func in ops.items():
        if op_str in condition_str:
            attr, value = condition_str.split(op_str)
            attr = attr.strip()
            value = int(value.strip())
            return lambda part: op_func(part[attr], value)
    # Should not reach here
    raise ValueError(f"Invalid condition: {condition_str}")


def parse_condition2(condition_str):
    for op in [">", "<", "=="]:
        if op in condition_str:
            variable, value = condition_str.split(op)
            variable = variable.strip()
            value = int(value.strip())
            return (variable, op, value)
    # Should not reach here
    raise ValueError(f"Invalid condition: {condition_str}")


def split_constraints(constraints, condition):
    variable, op, value = condition
    v_min, v_max = constraints[variable]
    true_constraints = None
    false_constraints = None

    if op == ">":
        if value < v_max:
            true_min = max(v_min, value + 1)
            true_max = v_max
            true_constraints = constraints.copy()
            true_constraints[variable] = (true_min, true_max)
        if v_min <= value:
            false_min = v_min
            false_max = min(v_max, value)
            false_constraints = constraints.copy()
            false_constraints[variable] = (false_min, false_max)
    elif op == "<":
        if v_min < value:
            true_min = v_min
            true_max = min(v_max, value - 1)
            true_constraints = constraints.copy()
            true_constraints[variable] = (true_min, true_max)
        if value <= v_max:
            false_min = max(v_min, value)
            false_max = v_max
            false_constraints = constraints.copy()
            false_constraints[variable] = (false_min, false_max)
    elif op == "==":
        if v_min <= value <= v_max:
            # True constraint
            true_constraints = constraints.copy()
            true_constraints[variable] = (value, value)
            # False constraints
            false_constraints_list = []
            if v_min <= value - 1:
                fc1 = constraints.copy()
                fc1[variable] = (v_min, value - 1)
                false_constraints_list.append(fc1)
            if value + 1 <= v_max:
                fc2 = constraints.copy()
                fc2[variable] = (value + 1, v_max)
                false_constraints_list.append(fc2)
            false_constraints = false_constraints_list
        else:
            # Condition can't be true
            true_constraints = None
            false_constraints = [constraints]
    else:
        raise ValueError(f"Invalid operator: {op}")

    return true_constraints, false_constraints


def count_combinations(constraints):
    total = 1
    for v_min, v_max in constraints.values():
        total *= v_max - v_min + 1
        if total == 0:
            return 0
    return total


def compute_acceptance(workflow_name, constraints, workflows, cache):
    key = (workflow_name, tuple(sorted(constraints.items())))
    if key in cache:
        return cache[key]
    total_accepted = 0
    rules = workflows[workflow_name]

    def process_rules(constraints, rule_idx):
        if rule_idx >= len(rules):
            return 0
        condition, destination = rules[rule_idx]
        if condition is not None:
            true_constraints, false_constraints = split_constraints(
                constraints, condition
            )
            total = 0
            # Process true constraints
            if true_constraints:
                if destination == "A":
                    total += count_combinations(true_constraints)
                elif destination == "R":
                    pass  # Rejected
                else:
                    total += compute_acceptance(
                        destination, true_constraints, workflows, cache
                    )
            # Process false constraints
            if false_constraints:
                if isinstance(false_constraints, list):
                    for fc in false_constraints:
                        total += process_rules(fc, rule_idx + 1)
                else:
                    total += process_rules(false_constraints, rule_idx + 1)
            return total
        else:
            # Last rule with no condition
            if destination == "A":
                return count_combinations(constraints)
            elif destination == "R":
                return 0
            else:
                return compute_acceptance(destination, constraints, workflows, cache)

    total_accepted = process_rules(constraints, 0)
    cache[key] = total_accepted
    return total_accepted


def parse_parts(parts_text):
    parts = []
    pattern = re.compile(r"\{(.*?)\}")
    for line in parts_text:
        attrs = {}
        for attr_str in pattern.match(line).group(1).split(","):
            key, value = attr_str.split("=")
            attrs[key.strip()] = int(value.strip())
        parts.append(attrs)
    return parts


def process_part(part, workflows, start_workflow="in"):
    current_workflow = start_workflow
    while True:
        for condition, destination in workflows[current_workflow]:
            if condition(part):
                if destination == "A":
                    return True  # Accepted
                elif destination == "R":
                    return False  # Rejected
                else:
                    current_workflow = destination
                break
    # Should not reach here
    return False


def part1(lines: list[list[str]]) -> int:
    """ """
    workflows = parse_workflows(lines[0])
    parts = parse_parts(lines[1])
    total = 0
    for part in parts:
        if process_part(part, workflows):
            total += sum(part[attr] for attr in ["x", "m", "a", "s"])
    return total


def part2(lines: list[list[str]]) -> int:
    """ """
    workflows = parse_workflows(lines[0], work_pass=2)
    # Initial constraints: all variables range from 1 to 4000
    initial_constraints = {
        "x": (1, 4000),
        "m": (1, 4000),
        "a": (1, 4000),
        "s": (1, 4000),
    }
    cache = {}
    total_accepted = compute_acceptance("in", initial_constraints, workflows, cache)
    return total_accepted


def main():
    loader = LoaderLib(2023)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(19)
    else:
        input_text = dedent(
            """\
                px{a<2006:qkq,m>2090:A,rfg}
                pv{a>1716:R,A}
                lnx{m>1548:A,A}
                rfg{s<537:gd,x>2440:R,A}
                qs{s>3448:A,lnx}
                qkq{x<1416:A,crn}
                crn{x>2662:A,R}
                in{s<1351:px,qqz}
                qqz{s>2770:qs,m<1801:hdj,R}
                gd{a>3333:R,R}
                hdj{m>838:A,pv}

                {x=787,m=2655,a=1222,s=2876}
                {x=1679,m=44,a=2067,s=496}
                {x=2036,m=264,a=79,s=2244}
                {x=2461,m=1339,a=466,s=291}
                {x=2127,m=1623,a=2188,s=1013}
            """
        ).strip("\n")

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
    # -
    # --------------------------------------------------------------------------------
    #  LAP -> 0.000722        |        0.000722 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : len(lines)=2 ...
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    #  LAP -> 0.002100        |        0.002823 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 432788
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    #  LAP -> 0.001892        |        0.004715 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 142863718918201
    # --------------------------------------------------------------------------------
