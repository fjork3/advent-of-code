import re

DAY_NUMBER = 1


def read_input():
    with open(f"inputs/input{DAY_NUMBER:0>2}.txt", "r") as f:
        return f.readlines()


def part_one():
    data = read_input()
    # print(data)
    # first_and_last = re.compile(r'^\w*(\d).*(\d)\w*$')
    # return sum(int("".join(first_and_last.search(d).groups())) for d in data)
    total = 0
    for d in data:
        digits = re.compile('\d').findall(d)
        total += int(f'{digits[0]}{digits[-1]}')
    return total

lookup = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
}
def str_to_digit(d):
    try:
        return int(d)
    except ValueError:
        return lookup[d]


def part_two():
    data = read_input()
    total = 0

    for d in data:
        digits = re.compile(r'(?=(\d|one|two|three|four|five|six|seven|eight|nine))').findall(d)
        total += int(f'{str_to_digit(digits[0])}{str_to_digit(digits[-1])}')
    return total


print(f"Day {DAY_NUMBER}, part 1: {part_one()}")
print(f"Day {DAY_NUMBER}, part 2: {part_two()}")
