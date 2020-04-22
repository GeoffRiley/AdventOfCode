def like_a_rogue(inp, repeat):
    grid = [1 if ch == '.' else 0 for ch in inp]
    res = sum(grid)
    for _ in range(1, repeat):
        grid = [0 if i != j else 1 for i, j in zip([1] + grid[:-1], grid[1:] + [1])]
        res += sum(grid)
    return res


if __name__ == '__main__':
    with open('input.txt') as first_row_file:
        first_row = first_row_file.read().strip()
        print(f'Day 18, part 1: {like_a_rogue(first_row, 40)}')
        print(f'Day 18, part 2: {like_a_rogue(first_row, 400_000)}')
        # Day 18, part 1: 2016
        # Day 18, part 2: 19998750
