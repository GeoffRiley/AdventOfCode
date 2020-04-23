def firewall_rules(inp, part1=True):
    ips = list(sorted(tuple(int(x) for x in line.split('-')) for line in inp))
    if part1:
        while ips[0][1] >= ips[1][0] - 1:
            temp = ips.pop(1)
            ips[0] = (ips[0][0], max(temp[1], ips[0][1]))
        return ips[0][1] + 1
    else:
        merged = []
        for rnge in ips:
            if not merged:
                merged.append(rnge)
            else:
                lower = merged[-1]
                if rnge[0] <= lower[1]:
                    merged[-1] = (lower[0], (max(lower[1], rnge[1])))
                else:
                    merged.append(rnge)
        ip_count = 0
        for a, b in zip(merged, merged[1:]):
            ip_count += (b[0] - a[1]) - 1
        return ip_count


if __name__ == '__main__':
    with open('input.txt') as ip_file:
        ip_list = ip_file.read().splitlines(keepends=False)
        print(f'Day 20, part 1: {firewall_rules(ip_list)}')
        print(f'Day 20, part 2: {firewall_rules(ip_list, False)}')
        # Day 20, part 1: 17348574
        # Day 20, part 2: 104
