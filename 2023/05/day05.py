"""
Advent of code 2023
Day 05: If You Give A Seed A Fertilizer
"""
from itertools import pairwise
from textwrap import dedent
from typing import List, Tuple

from aoc.loader import LoaderLib
from aoc.utility import extract_ints, grouped, lines_to_list


class RangeMapper:
    def __init__(self, title=None) -> None:
        self.range_list = list()
        self.title = title or "RangeMapper"

    def __repr__(self) -> str:
        return f"RangeMapper({self.range_list})"

    def __len__(self) -> int:
        return len(self.range_list)

    def add_range(self, dest: int, src: int, length: int) -> None:
        self.range_list.append((dest, src, length))
        self.range_list.sort(key=lambda x: x[1])

    def get(self, key: int) -> int:
        for dest, src, length in self.range_list:
            if key in range(src, src + length):
                return dest - src + key
        return key

    @staticmethod
    def _show_range(rng: Tuple[int, int, int]) -> str:
        dest, src, length = rng
        return f"({src} → {src+length-1}) ⇒ ({dest} → {dest+length-1})"

    def dump(self) -> None:
        print(f"/-- {self.title} dump:")
        for rng in self.range_list:
            print(f"|    ({self._show_range(rng)})")
        print("\\--")

    def split_range(
        self, rng: Tuple[int, int], rng_border: int
    ) -> List[Tuple[int, int]]:
        """
        Split a range into two ranges.
        `rng` is a tuple of (start, length) values.
        `rng_border` is the value that the range is split at.
        The return value is a list of tuples of (start, length) values
        representing the two ranges.
        """
        print(f"    // split_range({rng}, {rng_border})")  # DEBUG
        seek, cnt = rng
        if (seek == rng_border) or (seek + cnt <= rng_border):  # No split
            return [(seek, cnt)]
        return [
            (seek, rng_border - seek + 1),
            (rng_border + 1, cnt - (rng_border - seek)),
        ]  # Split

    @staticmethod
    def _apply_offset(rngs, offset):
        """
        Apply an offset to a list of ranges.
        `rngs` is a list of tuples of (start, length) values.
        `offset` is the offset to be applied.
        The return value is a new list of tuples of (start, length) values
        with the offset applied.
        """
        return [(start + offset, length) for start, length in rngs]

    def xlate(self, rng: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Translate a range of values through the mapping.
        `rng` is a tuple of (start, length) values.
        The target range is the range of values that the source range maps to,
        however, the source range may be split into multiple ranges.
        The return value is a list of tuples of (start, length) values
        representing the target ranges.
        """
        print(f"-- xlate({rng}); {self.title=}")  # DEBUG
        print(f"  >> Range covered: ({rng[0]} → {rng[0]+rng[1]-1})")  # DEBUG
        seek, cnt = rng
        new_rngs = []
        for dest, src, length in self.range_list:
            print(f"  && Mapping: {self._show_range((dest, src, length))}")  # DEBUG
            offset = dest - src
            if seek in range(src, src + length):
                chop = self.split_range((seek, cnt), src + length - 1)
                print(f"    \\\\ Split range: {chop}")
                if len(chop) == 1:
                    # The seek range is entirely within the source range.
                    dest_rng = self._apply_offset(chop, offset)
                    print(f"    ** New dest range: {dest_rng}")
                    new_rngs.extend(dest_rng)
                    seek, cnt = (seek + cnt, 0)
                    print(f"    [] End of seek range: ({seek}, {cnt})")
                else:
                    # The seek range is split into two ranges.
                    dest_rng = self._apply_offset(chop[:-1], offset)
                    print(f"    ** New dest range: {dest_rng}")
                    new_rngs.extend(dest_rng)
                    seek, cnt = chop[-1]
                    print(f"    <> New seek range: ({seek}, {cnt})")
            if cnt == 0:
                break
        if cnt > 0:
            # We didn't find a mapping for the entire seek range.
            # We assume a 1:1 mapping for the remainder of the seek range.
            print(f"    ** No mapping for ({seek}, {cnt})")  # DEBUG
            new_rngs.append((seek, cnt))  # Assume 1:1 mapping
        print(f"    \\\\ New ranges: {new_rngs}")  # DEBUG
        return new_rngs


def make_mappings(groups) -> list[RangeMapper]:
    mappings: list[RangeMapper] = []
    for group in groups[1:]:
        mapping = RangeMapper(group[0].split()[0])
        for line in group[1:]:
            dest, src, length = line.split()
            mapping.add_range(int(dest), int(src), int(length))
        # print(f"{group[0]} PRE INFILL len(mapping) = {len(mapping)}")
        infill = []
        for (dest1, src1, length1), (dest2, src2, length2) in pairwise(
            mapping.range_list
        ):
            diff = src2 - src1
            if diff < length1:
                infill.append((dest1 + length1, src1 + length1, diff - length1))
        for rng in infill:
            mapping.add_range(*rng)
        # print(f"{group[0]} POST INFILL len(mapping) = {len(mapping)}")
        mappings.append(mapping)
    for i in range(len(mappings)):
        mappings[i].dump()
    return mappings


seed_cache = dict()


def calculate_seed_location(seed, mappings, start_index=0):
    """
    Calculate the location of a seed.
    The `seed` parameter is the seed value.
    The `mappings` parameter is a list of RangeMapper objects.
    The `start_index` parameter is the index into the mappings list to start
    the calculation.
    """
    if seed in seed_cache:
        return seed_cache[seed]
    seed_location = seed
    for mapping in mappings[start_index:]:
        seed_location = mapping.get(seed_location)
    seed_cache[seed] = seed_location
    return seed_location


def part1(seed_list, mappings):
    """
    The `groups` parameter is a list of lists of strings.
    The first list is a list of seeds, the rest are lists of maps.
    The format of the list of seeds is the string "seeds:" followed by a list
    of integers. These integers are used as keys to the seed-to-soil map.
    Each map is a list of strings, the first string is the name of the map,
    the rest are the map values. The map values are integers that define
    ranges of values to be translated to the next map. The arrangement of the
    values in the map is the starting value of the destination range, the
    starting value of the source range, and the length of the source range.
    The last map in the list is the humidity-to-location map. The humidity
    value is used as an index into the humidity-to-location map to find the
    location of the seed.
    For all maps, any value that is not explicitly defined is assumed to be
    self referential. For example, if the seed-to-soil map is not defined for
    a seed, the seed is assumed to be planted in soil with the same value as
    the seed.
    """
    final_seed_locations = []

    for seed in seed_list:
        seed_location = calculate_seed_location(seed, mappings)
        final_seed_locations.append(seed_location)

    return min(final_seed_locations)


def part2(seed_list, mappings):
    """
    So, the seeds line is actually a list of pairs of values. The first value
    is the seed, the second value is the number of seeds after that seed. For
    example, the line "seeds: 79 14 55 13" means that there are two pairs of
    descriptors, the first shows that there are 14 seeds after seed 79, the
    second shows that there are 13 seeds after seed 55. The first seed is
    number 79, the second is number 80, the third is number 81, and so on.
    """
    final_seed_locations = []

    # Working through every single seed is too slow, so we'll just work
    # through the seeds ranges. Each range may directly map to another range,
    # or it may diverge into multiple ranges. We need to keep track of the
    # chopped up ranges so that we can follow those sub-ranges too.
    # This lends itself to a recursive solution, using the number of groups
    # as the recursion depth.
    #
    # First we need to convert the seed list into a list of seed ranges.
    seed_ranges = [(seed, count, 0) for seed, count in grouped(seed_list, 2)]

    while len(seed_ranges) > 0:
        seed, seed_count, index = seed_ranges.pop(0)
        if index == len(mappings):
            # We've reached the end of the mappings.
            # We add the location of the lowest seed in the range.
            # We don't need to add the location of every seed in the range,
            # because we know that the seeds are in order, and we know that
            # the location of the lowest seed is the location of the range.
            print(
                f"** Reached end of mappings; {seed=}, {seed_count=}, {index=}"
            )  # DEBUG
            final_seed_locations.append(seed)
            continue
        if seed_count == 1:
            # We have a single seed, so we can calculate the location, and
            # remove it from the list of candidates.
            print(f"** Single seed; {seed=}, {seed_count=}, {index=}")  # DEBUG
            seed_location = calculate_seed_location(seed, mappings, index)
            final_seed_locations.append(seed_location)
            continue
        # We need to translate the seed range through the mapping.
        new_ranges = mappings[index].xlate((seed, seed_count))
        # Add the new ranges to the list of seed ranges.
        seed_ranges.extend([(sd, ct, index + 1) for sd, ct in new_ranges])

    print(f"** {final_seed_locations=}")  # DEBUG
    return min(final_seed_locations)


def main():
    loader = LoaderLib(2023)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(5)
    else:
        input_text = dedent(
            """\
            seeds: 79 14 55 13

            seed-to-soil map:
            50 98 2
            52 50 48

            soil-to-fertilizer map:
            0 15 37
            37 52 2
            39 0 15

            fertilizer-to-water map:
            49 53 8
            0 11 42
            42 0 7
            57 7 4

            water-to-light map:
            88 18 7
            18 25 70

            light-to-temperature map:
            45 77 23
            81 45 19
            68 64 13

            temperature-to-humidity map:
            0 69 1
            1 0 69

            humidity-to-location map:
            60 56 37
            56 93 4
            """
        ).strip("\n")

    groups = [lines_to_list(group) for group in input_text.split("\n\n")]
    seed_list = extract_ints(groups[0][0])
    mappings: List[RangeMapper] = make_mappings(groups)

    # lines = lines_to_list(input_text)

    loader.print_solution(
        "setup", f"seed_list = {seed_list}; No. of mappings = {len(mappings)}"
    )
    loader.print_solution(
        1,
        part1(
            seed_list=seed_list,
            mappings=mappings,
        ),
    )
    loader.print_solution(
        2,
        part2(
            seed_list=seed_list,
            mappings=mappings,
        ),
    )


if __name__ == "__main__":
    main()
    # --
    # 157361872 too high
    # 33366705 too low
    # 105230362 too high
