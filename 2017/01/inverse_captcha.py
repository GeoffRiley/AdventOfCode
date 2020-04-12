def inverse_captcha(inp, pass1=True):
    result = 0
    inp = list(map(int, inp))
    if pass1:
        inp2 = inp[1:] + inp[:1]
    else:
        l = len(inp) // 2
        inp2 = inp[l:] + inp[:l]
    for x, y in zip(inp, inp2):
        if x == y:
            result += x
    return result


if __name__ == '__main__':
    assert inverse_captcha('1122') == 3
    assert inverse_captcha('1111') == 4
    assert inverse_captcha('1234') == 0
    assert inverse_captcha('91212129') == 9
    assert inverse_captcha('1212', False) == 6
    assert inverse_captcha('1221', False) == 0
    assert inverse_captcha('123425', False) == 4
    assert inverse_captcha('123123', False) == 12
    assert inverse_captcha('12131415', False) == 4
    with open('input.txt') as captcha_file:
        captcha_text = captcha_file.read().strip()
        print(f'Day 1, part 1: {inverse_captcha(captcha_text)}')
        print(f'Day 1, part 2: {inverse_captcha(captcha_text, False)}')
        # Day 1, part 1: 1047
        # Day 1, part 2: 982
