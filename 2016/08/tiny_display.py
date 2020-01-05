import re


def do_display(script: str, width: int = 50, height: int = 6):
    display = [[False for _ in range(width)] for _ in range(height)]
    for line in script.splitlines(keepends=False):
        if line.startswith('rect '):
            x, y = [int(v) for v in re.search(r'(\d+)x(\d+)', line[5:]).groups()]
            for row in range(y):
                for col in range(x):
                    display[row][col] = True
        elif line.startswith('rotate column '):
            x, delta = [int(v) for v in re.search(r'x=(\d+) by (\d+)', line[14:]).groups()]
            tmp = [v[x] for v in display]
            tmp = tmp[-delta:] + tmp[:-delta]
            for v, row in zip(tmp, display):
                row[x] = v
        elif line.startswith('rotate row '):
            y, delta = [int(v) for v in re.search(r'y=(\d+) by (\d+)', line[11:]).groups()]
            tmp = display[y]
            display[y] = tmp[-delta:] + tmp[:-delta]
        else:
            raise SyntaxError(f'I don\'t know what to do with {line}')
    return display


if __name__ == '__main__':
    with open('input') as f:
        the_script = f.read()
    disp = do_display(the_script)

    part1 = sum(1 for rows in disp for x in rows if x)
    print(f'Part 1: {part1}')
    part2 = '\n'.join(''.join('#' if x else ' ' for x in row) for row in disp)
    print(f'Part 2:\n{part2}')
    # Part 1: 119
    # Part 2:
    # #### #### #  # ####  ### ####  ##   ##  ###   ##
    #    # #    #  # #    #    #    #  # #  # #  # #  #
    #   #  ###  #### ###  #    ###  #  # #    #  # #  #
    #  #   #    #  # #     ##  #    #  # # ## ###  #  #
    # #    #    #  # #       # #    #  # #  # #    #  #
    # #### #    #  # #    ###  #     ##   ### #     ##
    #   ZFHFSFOGPO
