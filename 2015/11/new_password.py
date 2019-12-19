import re


def check_password(password: str) -> bool:
    if len(password) != 8:
        return False
    if len(set(password).intersection('ilo')) > 0:
        return False
    if not password.islower():
        return False
    p = bytearray(password.encode())
    triple = False
    for i in range(2, len(p)):
        if p[i] == p[i - 1] + 1 == p[i - 2] + 2:
            triple = True
            break
    if not triple:
        return False
    if len(re.findall(r'(.)\1', password)) < 2:
        return False
    return True


seq = 'abcdefghjkmnpqrstuvwxyz'
next_letter = dict(zip(seq, seq[1:] + seq[0]))


def inc_password(password: str) -> str:
    p_arr = [c for c in password]
    letter = len(p_arr) - 1
    while True:
        carry = p_arr[letter] == 'z'
        p_arr[letter] = next_letter[p_arr[letter]]
        if not carry:
            return ''.join(p_arr)
        letter -= 1


def generate_password(password: str) -> str:
    if 'i' in password:
        password = (password[:password.index('i')] + 'jaaaaaaaa')[:8]
    if 'l' in password:
        password = (password[:password.index('l')] + 'maaaaaaaa')[:8]
    if 'o' in password:
        password = (password[:password.index('o')] + 'paaaaaaaa')[:8]
    password = inc_password(password)
    while not check_password(password):
        password = inc_password(password)
    return password


if __name__ == '__main__':
    current_password = "cqjxjnds"
    new_password = generate_password(current_password)
    print(f'Part 1: {new_password}')
    newer_password = generate_password(new_password)
    print(f'Part 2: {newer_password}')
