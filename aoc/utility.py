import re
from typing import List, Tuple, Any, Iterable


def to_list(line: str):
    """ Transform a comma-separated string to a list. """
    return [element.strip() for element in line.split(',')]


def extract_ints(line: str, negative: bool = False) -> List[int]:
    """ Trawl the input line for any integers and return them as a list.

    This will extract ints, including negatives if requested that are not
    necessarily comma separated.
    """
    regex = r'(-?\d+)' if negative else r'(\d+)'
    return list(map(int, re.findall(regex, line)))


def to_list_int(line: str) -> List[int]:
    """ Transform a string of comma-separated integers to a list. """
    return list(map(int, line.split(',')))


def lines_to_list(lines: str) -> List[str]:
    """ Transform multi-line input to a list. """
    return lines.splitlines(keepends=False)


def lines_to_list_int(lines: str) -> List[int]:
    """ Transform multi-line integer input to a list. """
    return list(map(int, lines.splitlines(keepends=False)))


def sequence_to_int(line: str) -> List[int]:
    """ Transform a sequence of digits to a list of integers. """
    return list(map(int, line))


def grouped(iterable: Iterable[Any], n: int) -> Iterable[Tuple[Any, ...]]:
    """ Create groups of tuples comprising 'n' values from the given iter.

    s -> (s0, s1, s2, ..., s(n-1)),
        (sn, s(n+1), s(n+2), ..., s(2n-1))...
    """
    return zip(*[iter(iterable)] * n)


def pairwise(iterable: Iterable[Any]) -> Iterable[Tuple[Any, Any]]:
    """ Divide the given iter into pairs and return as tuple pairs.

    s -> (s0, s1), (s2, s3), (s4, s5), ...
    """
    itr = iter(iterable)
    return zip(itr, itr)
