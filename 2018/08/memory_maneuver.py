class Tree(object):
    def __init__(self):
        self.children = []
        self.metadata = []

    def add_child(self, leaf):
        self.children.append(leaf)

    def add_metadata(self, metadata):
        self.metadata.append(metadata)

    def sum_metadata(self):
        metasum = sum(self.metadata)
        for c in self.children:
            metasum += c.sum_metadata()
        return metasum

    def sum_tree(self):
        child_count = len(self.children)
        if child_count > 0:
            metasum = 0
            for x in self.metadata:
                if 0 < x <= child_count:
                    metasum += self.children[x - 1].sum_tree()
        else:
            metasum = self.sum_metadata()
        return metasum


class Datapump(object):
    def __init__(self, data):
        self.data = data
        self.point = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.point < len(self.data):
            res, self.point = self.data[self.point], self.point + 1
            return res
        else:
            raise StopIteration()

    def next(self):
        return self.__next__()


def parse_tree(tree_data):
    leaf = Tree()
    children = tree_data.next()
    metadata = tree_data.next()
    for _ in range(children):
        leaf.add_child(parse_tree(tree_data))
    for _ in range(metadata):
        leaf.add_metadata(tree_data.next())
    return leaf


def memory_maneuver_part_1(inp):
    datapump = Datapump([int(i) for i in inp[0].split()])
    tree = parse_tree(datapump)
    return tree.sum_metadata()


def memory_maneuver_part_2(inp):
    datapump = Datapump([int(i) for i in inp[0].split()])
    tree = parse_tree(datapump)
    return tree.sum_tree()


if __name__ == '__main__':
    with open('input.txt') as license_file:
        license_lines = license_file.read().splitlines(keepends=False)
        print(f'Day 8, part 1: {memory_maneuver_part_1(license_lines)}')
        print(f'Day 8, part 2: {memory_maneuver_part_2(license_lines)}')
        # Day 8, part 1: 45618
        # Day 8, part 2: 22306
