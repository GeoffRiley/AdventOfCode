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

    def values(self) -> tuple[int, int, int]:
        for rng in self.range_list:
            yield rng

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
        # print(f"-- xlate({rng}); {self.title=}")  # DEBUG
        # print(f"  >> Range covered: ({rng[0]} → {rng[0]+rng[1]-1})")  # DEBUG
        seek, cnt = rng
        new_rngs = []
        for dest, src, length in self.range_list:
            # print(f"  && Mapping: {self._show_range((dest, src, length))}")  # DEBUG
            offset = dest - src
            if seek in range(src, src + length):
                chop = self.split_range((seek, cnt), src + length - 1)
                # print(f"    \\\\ Split range: {chop}")
                if len(chop) == 1:
                    # The seek range is entirely within the source range.
                    dest_rng = self._apply_offset(chop, offset)
                    # print(f"    ** New dest range: {dest_rng}")
                    new_rngs.extend(dest_rng)
                    seek, cnt = (seek + cnt, 0)
                    # print(f"    [] End of seek range: ({seek}, {cnt})")
                else:
                    # The seek range is split into two ranges.
                    dest_rng = self._apply_offset(chop[:-1], offset)
                    # print(f"    ** New dest range: {dest_rng}")
                    new_rngs.extend(dest_rng)
                    seek, cnt = chop[-1]
                    # print(f"    <> New seek range: ({seek}, {cnt})")
            if cnt == 0:
                break
        if cnt > 0:
            # We didn't find a mapping for the entire seek range.
            # We assume a 1:1 mapping for the remainder of the seek range.
            # print(f"    ** No mapping for ({seek}, {cnt})")  # DEBUG
            new_rngs.append((seek, cnt))  # Assume 1:1 mapping
        # print(f"    \\\\ New ranges: {new_rngs}")  # DEBUG
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
    # for i in range(len(mappings)):
    #     mappings[i].dump()
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


def calculate_seed_location2(seed, mappings, start_index=0):
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
        mapping.get(seed_location[0]),
        mapping.get(seed_location[1]),
    seed_cache[seed] = seed_location
    return seed_location


def map_intervals(source_intervals, mapping_ranges):
    new_intervals = []
    for s_start, s_end in source_intervals:
        intervals = []
        # Collect all mapping ranges that overlap with s_start to s_end
        for m_src_start, m_src_end, m_dest_start, m_dest_end in mapping_ranges:
            overlap_start = max(s_start, m_src_start)
            overlap_end = min(s_end, m_src_end)
            if overlap_start <= overlap_end:
                offset = overlap_start - m_src_start
                dest_start = m_dest_start + offset
                dest_end = dest_start + (overlap_end - overlap_start)
                intervals.append((dest_start, dest_end))
        # For parts not covered by any mapping, they map to themselves
        # Find gaps between mapping ranges and map them to themselves
        mapping_src_intervals = [
            (m_src_start, m_src_end) for m_src_start, m_src_end, _, _ in mapping_ranges
        ]
        mapping_src_intervals.sort()
        idx = 0
        i = s_start
        while i <= s_end:
            # Skip mapping ranges that are before i
            while (
                idx < len(mapping_src_intervals) and mapping_src_intervals[idx][1] < i
            ):
                idx += 1
            if (
                idx < len(mapping_src_intervals)
                and mapping_src_intervals[idx][0] <= i <= mapping_src_intervals[idx][1]
            ):
                # i is within a mapping range, will be handled above
                i = mapping_src_intervals[idx][1] + 1
            else:
                # i is not in any mapping range, maps to itself
                unmapped_start = i
                if idx < len(mapping_src_intervals):
                    unmapped_end = min(s_end, mapping_src_intervals[idx][0] - 1)
                else:
                    unmapped_end = s_end
                intervals.append((unmapped_start, unmapped_end))
                i = unmapped_end + 1
        # Merge intervals
        intervals.sort()
        merged = []
        for start, end in intervals:
            if not merged or start > merged[-1][1] + 1:
                merged.append((start, end))
            else:
                merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        new_intervals.extend(merged)
    # Merge new_intervals
    new_intervals.sort()
    merged_intervals = []
    for start, end in new_intervals:
        if not merged_intervals or start > merged_intervals[-1][1] + 1:
            merged_intervals.append((start, end))
        else:
            merged_intervals[-1] = (
                merged_intervals[-1][0],
                max(merged_intervals[-1][1], end),
            )
    return merged_intervals


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

    # Working through every single seed is too slow, so we'll just work
    # through the seeds ranges. Each range may directly map to another range,
    # or it may diverge into multiple ranges. We need to keep track of the
    # chopped up ranges so that we can follow those sub-ranges too.
    # This lends itself to a recursive solution, using the number of groups
    # as the recursion depth.
    #
    # First we need to convert the seed list into a list of seed ranges.
    intervals = [
        (seed, count)
        for seed, count in seed_list
        # for seed, count in grouped(seed_list, 2)
    ]

    # print(f'Starting: {intervals=}')
    # Starting:
    #  intervals=[
    #  (630335678, 701491196),
    #  (260178142, 385183562),
    #  (1548082684, 2067859966),
    #  (4104586697, 4135279672),
    #  (1018893962, 1429853751),
    #  (3570781652, 3615843761),
    #  (74139777, 180146500),
    #  (3262608046, 3476068196),
    #  (3022784256, 3144777385),
    #  (2138898608, 2175668591)
    # ]

    # The seed ranges need to be modified from the format
    #  (dest_start, src_start, length) to
    #  (src_start, src_end, dest_start, dest end)
    new_mapping = []
    for mapping in mappings:
        current_mapping = []
        new_mapping.append(current_mapping)
        for mapp in mapping.values():
            dest_start, src_start, length = mapp
            src_end = src_start + length - 1
            dest_end = dest_start + length - 1
            current_mapping.append((src_start, src_end, dest_start, dest_end))

    # Process mappings
    for mapping_ranges in new_mapping:
        intervals = map_intervals(intervals, mapping_ranges)
        # If the number of intervals exceeds a threshold, we can stop
        # For this problem, since we're only interested in the minimal
        # location number, we can keep track of the minimal number
        if len(intervals) > 1000:
            break
    # Extract the minimal location number
    min_location = min(start for start, end in intervals)

    # Output the minimal location number
    return min_location


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
    seed_ranges = [(a, a + b) for a, b in grouped(extract_ints(groups[0][0]), 2)]
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
            seed_list=seed_ranges,
            mappings=mappings,
        ),
    )


if __name__ == "__main__":
    main()
    # --
    # --------------------------------------------------------------------------------
    # LAP -> 0.000497        |        0.000497 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part setup : seed_list = [630335678, 71155519, 260178142, 125005421, 
    #                           1548082684, 519777283, 4104586697, 30692976,
    #                           1018893962, 410959790, 3570781652, 45062110,
    #                           74139777, 106006724, 3262608046, 213460151, 
    #                           3022784256, 121993130, 2138898608, 36769984]; 
    #              No. of mappings = 7
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.000255        |        0.000752 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 1   : 51580674
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # LAP -> 0.001288        |        0.002039 <- ELAPSED
    # --------------------------------------------------------------------------------
    # Part 2   : 99751240
    # --------------------------------------------------------------------------------
