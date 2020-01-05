from hashlib import md5


def find_password(key: str, zero_count: int = 5) -> str:
    i = 0
    pwd = ''
    target = '0' * zero_count
    while len(pwd) < 8:
        i += 1
        dig = md5((key + str(i)).encode()).hexdigest()
        if dig.startswith(target):
            pwd += dig[5]
    return pwd


def find_password2(key: str, zero_count: int = 5) -> str:
    i = 0
    pwd = {}
    target = '0' * zero_count
    while len(pwd) < 8:
        i += 1
        dig = md5((key + str(i)).encode()).hexdigest()
        if dig.startswith(target):
            loc = dig[5]
            if '0' <= loc <= '7' and loc not in pwd:
                pwd[loc] = dig[6]
    return ''.join(c[1] for c in sorted(pwd.items(), key=lambda x: x[0]))


if __name__ == '__main__':
    x = find_password('ugkcyxxp')
    print(f'Part 1: {x}')
    # Part 1: d4cd2ee1
    y = find_password2('ugkcyxxp')
    print(f'Part 2: {y}')
    # Part 2: f2c730e5
