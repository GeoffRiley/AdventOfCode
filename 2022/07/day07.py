"""
Advent of code 2022
Day 07: No Space Left On Device
"""
from collections import defaultdict
from typing import List, Dict, Any

from aoc.loader import LoaderLib
from aoc.search import Node
from aoc.utility import lines_to_list


def construct_tree(lines: List[str]) -> (Node, Dict[Node, Dict[str, Any]]):
    """ Parse the command lines provided """
    root = Node('/', None)
    filelists = {root: {}}
    current_dir = root
    for line in lines:
        parts = line.split()
        if parts[0] == '$':
            # parse command line
            if parts[1] == 'cd':
                # change directory
                if parts[2] == '/':
                    current_dir = root
                elif parts[2] == '..':
                    current_dir = current_dir.parent
                else:
                    current_dir = filelists[current_dir][parts[2]]
            elif parts[1] == 'ls':
                pass
            else:
                raise SyntaxError(f'Do not understand command {" ".join(parts[1:])}')
        elif parts[0] == 'dir':
            # Add a new directory
            new_dir = Node(parts[1], current_dir)
            filelists[current_dir][parts[1]] = new_dir
            filelists[new_dir] = {}
            # current_dir = new_dir
        elif parts[0].isnumeric():
            filelists[current_dir][parts[1]] = int(parts[0])
        else:
            raise SyntaxError(f'What is this all about: {line}')
    return root, filelists


previous_sizes = defaultdict(int)


def get_dir_size(node: Node, filelist: Dict[Node, Dict[str, Any]]) -> int:
    """ Calculate the size of the files in this directory and descendant nodes """
    if node in previous_sizes:
        return previous_sizes[node]
    size = 0
    for _, value in filelist[node].items():
        if isinstance(value, Node):
            size += get_dir_size(value, filelist)
        else:
            size += value

    previous_sizes[node] = size
    return size


def part1(filelist: Dict[Node, Dict[str, Any]]) -> int:
    """
    Find all directories with a total size of less than 100k
    and total them up. Return this value.

    @:param tree: root node of the directory tree
    @:param filelist: list of directory nodes with contents
    @:return int:
    """
    total = 0
    for node, _ in filelist.items():
        size = get_dir_size(node, filelist)
        if size < 100_000:
            total += size

    return total


def part2(tree: Node, filelist: Dict[Node, Dict[str, Any]]) -> int:
    """
    Calculate which directories need to be deleted in order to release
    enough free space for the application to be loaded.
    Return the size that is going to be cleared when the directory is
    removed.

    @:param tree: root node of the directory tree
    @:param filelist: list of directory nodes with contents
    @:return int:
    """
    total_disk_space = 70_000_000
    target_disk_space = 30_000_000
    space_available = total_disk_space - get_dir_size(tree, filelist)
    required_to_delete = target_disk_space - space_available

    total = total_disk_space
    for node, _ in filelist.items():
        size = get_dir_size(node, filelist)
        if size > required_to_delete:
            total = min(size, total)

    return total


def main():
    loader = LoaderLib(2022)
    input_text = loader.get_aoc_input(7)

    # input_text = dedent('''\
    #     $ cd /
    #     $ ls
    #     dir a
    #     14848514 b.txt
    #     8504156 c.dat
    #     dir d
    #     $ cd a
    #     $ ls
    #     dir e
    #     29116 f
    #     2557 g
    #     62596 h.lst
    #     $ cd e
    #     $ ls
    #     584 i
    #     $ cd ..
    #     $ cd ..
    #     $ cd d
    #     $ ls
    #     4060174 j
    #     8033020 d.log
    #     5626152 d.ext
    #     7214296 k
    # ''').strip('\n')

    lines = lines_to_list(input_text)
    tree, filelist = construct_tree(lines)

    loader.print_solution('setup', f'{len(filelist)} ...')
    loader.print_solution(1, part1(filelist))
    loader.print_solution(2, part2(tree, filelist))


if __name__ == '__main__':
    main()
    # --------------------------------------------------------------------------------
    #  LAP -> 0.007183        |        0.007183 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : 189 ...
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.001719        |        0.008902 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 1583951
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.000444        |        0.009345 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 214171
    # --------------------------------------------------------------------------------
