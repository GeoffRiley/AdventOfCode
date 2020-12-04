import string

EXPECTED_FIELDS = {
    'byr',  # (Birth Year)
    'iyr',  # (Issue Year)
    'eyr',  # (Expiration Year)
    'hgt',  # (Height)
    'hcl',  # (Hair Color)
    'ecl',  # (Eye Color)
    'pid',  # (Passport ID)
    'cid',  # (Country ID)
}


def validate_year(value: str, min_: int, max_: int) -> bool:
    if value.isdigit():
        return min_ <= int(value) <= max_
    return False


def validate_height(value: str) -> bool:
    units = value[-2:]
    if units == 'cm':
        min_, max_ = 150, 193
    elif units == 'in':
        min_, max_ = 59, 76
    else:
        return False
    value = value[:-2]
    if value.isdigit():
        return min_ <= int(value) <= max_
    return False


def validate_hair_colour(value: str) -> bool:
    return value[0] == '#' and all(ch in string.hexdigits for ch in value[1:].lower())


def validate_eye_colour(value: str) -> bool:
    return value in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}


def validate_passport_id(value: str) -> bool:
    return len(value) == 9 and all(ch in string.digits for ch in value)


VALIDATION_ROUTINES = {
    'hgt': validate_height,
    'hcl': validate_hair_colour,
    'ecl': validate_eye_colour,
    'pid': validate_passport_id
}
YEAR_LIMITS = {
    'byr': (1920, 2002),
    'iyr': (2010, 2020),
    'eyr': (2020, 2030)
}


def validate_field(name: str, value: str) -> bool:
    if name in YEAR_LIMITS:
        return validate_year(value, *YEAR_LIMITS[name])
    if name in VALIDATION_ROUTINES:
        return VALIDATION_ROUTINES[name](value)
    return name == 'cid'


def passport_processing_part1(data: str) -> int:
    records = [dict(entry.split(':') for entry in para.split()) for para in data.split('\n\n')]
    result = 0
    for record in records:
        tester = set(record.keys()) ^ EXPECTED_FIELDS
        if (len(tester) == 0) or (tester == {'cid'}):
            result += 1
    return result


def passport_processing_part2(data: str) -> int:
    records = [dict(entry.split(':') for entry in para.split()) for para in data.split('\n\n')]
    result = 0
    for record in records:
        tester = set(record.keys()) ^ EXPECTED_FIELDS
        if (len(tester) == 0) or (tester == {'cid'}):
            if all(validate_field(k, v) for k, v in record.items()):
                result += 1
    return result


if __name__ == '__main__':
    example_data1 = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""
    example_data2 = """eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007"""
    example_data3 = """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"""
    assert passport_processing_part1(example_data1) == 2
    assert passport_processing_part2(example_data2) == 0
    assert passport_processing_part2(example_data3) == 4

    with open('input.txt') as in_file:
        original = in_file.read()
        part1 = passport_processing_part1(original)
        print(f'Part1: {part1}')
        part2 = passport_processing_part2(original)
        print(f'Part2: {part2}')

        # Part1: 237
        # Part2: 172
