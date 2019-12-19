def look_and_say(in_val: str) -> str:
    out_val = ''
    count = 1
    for i in range(1, len(in_val)):
        if in_val[i - 1] == in_val[i]:
            count += 1
        else:
            out_val += f'{str(count)}{in_val[i - 1]}'
            count = 1
    out_val += f'{str(count)}{in_val[-1]}'
    return out_val


if __name__ == '__main__':
    the_val = '1113122113'
    for i in range(40):
        the_val = look_and_say(the_val)
    print(f'Part 1: {len(the_val)}')
    for i in range(10):
        the_val = look_and_say(the_val)
    print(f'Part 2: {len(the_val)}')
