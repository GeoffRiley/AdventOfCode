import os
import pickle
from pathlib import Path
from time import perf_counter

from requests import get


class LoaderLib:
    """Advent of Code loader library.

    Attributes:
        aoc_year (int): The year of Advent of Code to work with.

    Methods:
        print_solution
        get_puzzle_input
        cache_data
        retrieve_data
    """

    _aoc_input_url = 'https://adventofcode.com/{year}/day/{day}/input'

    def __init__(self, aoc_year):
        """Initialise helper library.

        Parameters:
            aoc_year (int): The year of Advent of Code to work with.
        """

        self._timer_start = perf_counter()
        self._timer_last = self._timer_start

        self.aoc_year = aoc_year

        user_profile = Path(os.environ['USERPROFILE'])
        self._aoc_path = user_profile / 'aoc'

        base_path = Path().cwd()
        while base_path.parts[-1].casefold() != 'AdventOfCode'.casefold():
            base_path = base_path.parent
            if len(base_path.parts) == 1:
                raise EnvironmentError('Cannot locate directory AdventOfCode')

        self._base_path = base_path

        aoc_cookie_filename = (self._aoc_path / 'aoc.cookie')
        if not aoc_cookie_filename.exists():
            raise EnvironmentError(f"No cookie file found ({aoc_cookie_filename})")
        aoc_cookie_value = aoc_cookie_filename.read_text()
        self._aoc_cookie = dict(session=aoc_cookie_value)

    def get_aoc_input(self, day, transform_function=lambda x: x):
        """Get puzzle input from the AOC website.

        Apply an optional transform function to it before returning.

        Cache the puzzle input locally for next time.

        Args:
            day (int): The day of the puzzle.
            transform_function: A transformation function to apply to
                the puzzle input.
        Returns:
            The puzzle input, transformed by transform_function.
        """
        cache_filename = self._base_path / str(self.aoc_year) / f'{day:02d}' / 'input.txt'
        puzzle_input = cache_filename.read_text() if cache_filename.exists() else None

        if puzzle_input is None:
            response = get(
                self._aoc_input_url.format(year=self.aoc_year, day=day),
                cookies=self._aoc_cookie)

            if response.status_code != 200:
                raise AssertionError('Unable to obtain puzzle input!')

            puzzle_input = response.text.rstrip('\n')
            cache_filename.parent.mkdir(parents=True, exist_ok=True)
            cache_filename.write_text(puzzle_input)

        return transform_function(puzzle_input)

    def print_solution(self, part, *args, **kwargs):
        """Print the puzzle solution with timer.

        Args:
            part (int or string): The part of the puzzle.
        """
        timer_now = perf_counter()
        lap_time = timer_now - self._timer_last
        elapsed_time = timer_now - self._timer_start

        print(f'\n{"-" * 80}')
        print(f' LAP -> {lap_time:<15.6f} | {elapsed_time :>15.6f} <- ELAPSED')
        print(f'{"-" * 80}\n Part {part:<3} : ', end='')
        print(*args, **kwargs)
        print(f'{"-" * 80}\n', flush=True)

        self._timer_last = timer_now

    def cache_data(self, day, key, obj):
        """Store some data in a cache file for later"""
        cache_filename = self._aoc_path / f'cache_{self.aoc_year}_{day:02d}_{key}.txt'
        cache_filename.parent.mkdir(parents=True, exist_ok=True)
        cache_filename.write_bytes(pickle.dumps(obj))

    def retrieve_data(self, day, key):
        """Retrieve some data from a cache file"""
        cache_filename = self._aoc_path / f'cache_{self.aoc_year}_{day:02d}_{key}.txt'
        obj = pickle.loads(cache_filename.read_bytes()) if cache_filename.exists() else None

        return obj


if __name__ == '__main__':
    aoc = LoaderLib(2021)
    in_text = aoc.get_aoc_input(1)
    in_vars = list(map(int, in_text.splitlines(keepends=False)))
    n = [x for x, y in zip(in_vars, in_vars[1:]) if x < y]
    aoc.print_solution('a', len(n))
    m = [x for x, y in zip(in_vars, in_vars[3:]) if x < y]
    aoc.print_solution(2, len(m))

    # --------------------------------------------------------------------------------
    #  LAP -> 0.004998        |        0.004998 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part a   : 1715
    # --------------------------------------------------------------------------------
    #
    #
    # --------------------------------------------------------------------------------
    #  LAP -> 0.000642        |        0.005640 <- ELAPSED
    # --------------------------------------------------------------------------------
    #  Part 2   : 1739
    # --------------------------------------------------------------------------------
