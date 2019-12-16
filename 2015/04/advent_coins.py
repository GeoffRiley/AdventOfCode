from hashlib import md5


def mine(secret: str, zero_count=5) -> int:
    i = 0
    target = '0' * zero_count
    while True:
        i += 1
        dig = md5((secret + str(i)).encode()).hexdigest()
        if dig.startswith(target):
            return i


if __name__ == '__main__':
    key = 'bgvyzdsv'
    print(f'Part1: {mine(key)}')
    print(f'Part2: {mine(key, 6)}')
