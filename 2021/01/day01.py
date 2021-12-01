def main():
    with open("input.txt") as infile:
        lines = [int(n) for n in infile.read().splitlines(keepends=False)]
        current = lines[0]
        count = 0
        for line in lines[1:]:
            if line > current:
                count += 1
            current = line
        print(f"Part 1: Increase: {count} times")
        count = 0
        current = sum(lines[0:2])
        for line in zip(lines[1:], lines[2:], lines[3:]):
            n = sum(line)
            if n > current:
                count += 1
            current = n
        print(f"Part 2: Increase: {count} times")


if __name__ == "__main__":
    main()

# Part 1: Increase: 1715 times
# Part 2: Increase: 1739 times
