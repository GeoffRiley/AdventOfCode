"""
Advent of code 2025
Day 09: Movie Theater
"""
from bisect import bisect_left, bisect_right
from textwrap import dedent

from aoc.loader import LoaderLib
from aoc.utility import lines_to_list, extract_ints


def part1(lines: list[tuple[int, ...]]) -> int:
    # Keep raw integer tuples for speed; compute area directly.
    pts = list(lines)
    n = len(pts)
    max_area = 0
    for i in range(n - 1):
        xi, yi = pts[i]
        for j in range(i + 1, n):
            xj, yj = pts[j]
            # Inclusive area (matches Rectangle.area())
            area = (abs(xi - xj) + 1) * (abs(yi - yj) + 1)
            if area > max_area:
                max_area = area
    return max_area


def part2(lines: list[tuple[int, ...]]) -> int:
    # Avoid building all O(n^2) edges; precompute min/max spans per x and per y,
    # and detect crossings by scanning only unique x or y strictly inside the rectangle.
    pts = list(lines)
    n = len(pts)

    # Precompute min/max y for each x, and min/max x for each y
    x_minmax: dict[int, tuple[int, int]] = {}
    y_minmax: dict[int, tuple[int, int]] = {}
    for x, y in pts:
        # Update x -> (min_y, max_y)
        if x in x_minmax:
            lo, hi = x_minmax[x]
            if y < lo:
                lo = y
            if y > hi:
                hi = y
            x_minmax[x] = (lo, hi)
        else:
            x_minmax[x] = (y, y)
        # Update y -> (min_x, max_x)
        if y in y_minmax:
            lo, hi = y_minmax[y]
            if x < lo:
                lo = x
            if x > hi:
                hi = x
            y_minmax[y] = (lo, hi)
        else:
            y_minmax[y] = (x, x)

    xs = sorted(x_minmax)
    ys = sorted(y_minmax)

    max_area = 0
    for i in range(n - 1):
        xi, yi = pts[i]
        for j in range(i + 1, n):
            xj, yj = pts[j]
            # Rectangle bounds
            left, right = (xi, xj) if xi < xj else (xj, xi)
            top, bottom = (yi, yj) if yi < yj else (yj, yi)
            # Early area pruning (inclusive area)
            area = (right - left + 1) * (bottom - top + 1)
            if area <= max_area:
                continue

            crossed = False
            # Check for vertical crossings: any x strictly between left and right
            li = bisect_right(xs, left)
            ri = bisect_left(xs, right)
            for k in range(li, ri):
                mn_y, mx_y = x_minmax[xs[k]]
                if mn_y < bottom and mx_y > top:
                    crossed = True
                    break

            if not crossed:
                # Check for horizontal crossings: any y strictly between top and bottom
                tj = bisect_right(ys, top)
                bj = bisect_left(ys, bottom)
                for k in range(tj, bj):
                    mn_x, mx_x = y_minmax[ys[k]]
                    if mn_x < right and mx_x > left:
                        crossed = True
                        break

            if not crossed:
                # No crossing edges inside the rectangle; update maximum area
                max_area = area

    return max_area


def main():
    loader = LoaderLib(2025)
    testing = False
    if not testing:
        input_text = loader.get_aoc_input(9)
    else:
        input_text = dedent(
            """\
                7,1
                11,1
                11,7
                9,7
                9,5
                2,5
                2,3
                7,3
            """
        ).strip("\n")
    lines = [tuple(extract_ints(param)) for param in list(lines_to_list(input_text))]
    # lines = [lines_to_list(line) for line in input_text.split("\n\n")]
    # lines = lines_to_list(input_text)
    # lines = input_text.split(',')

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
    #  LAP -> 0.001620        |        0.001620 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part setup : len(lines)=496 ...
    # --------------------------------------------------------------------------------
    # 
    # 
    # --------------------------------------------------------------------------------
    #  LAP -> 0.028843        |        0.030463 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 1   : 4790063600
    # --------------------------------------------------------------------------------
    # 
    # 
    # --------------------------------------------------------------------------------
    #  LAP -> 0.193916        |        0.224379 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 1516172795
    # --------------------------------------------------------------------------------
