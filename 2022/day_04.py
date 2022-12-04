from typing import List, Tuple

DAY_NUMBER = 4


class Assignment:
    def __init__(self, a: str):
        r = a.split("-")
        self.start = int(r[0])
        self.end = int(r[1])


def contains(a1: Assignment, a2: Assignment) -> bool:
    return (a1.start <= a2.start and a1.end >= a2.end) or (a2.start <= a1.start and a2.end >= a1.end)


def overlaps(a1: 'Assignment', a2: 'Assignment') -> bool:
    return contains(a1, a2) or (a2.start <= a1.start <= a2.end) or (a2.start <= a1.end <= a2.end)


def read_input():
    pairs = []
    with open(f"inputs/input{DAY_NUMBER:0>2}.txt", "r") as f:
        for line in f.read().splitlines():
            elves = line.split(",")
            pairs.append((Assignment(elves[0]), Assignment(elves[1])))
    return pairs


def part_one(pairs: List[Tuple[Assignment, Assignment]]):
    return sum(contains(e[0], e[1]) for e in pairs)


def part_two(pairs):
    return sum(overlaps(e[0], e[1]) for e in pairs)

pairs = read_input()
print(f"Day {DAY_NUMBER}, part 1: {part_one(pairs)}")
print(f"Day {DAY_NUMBER}, part 2: {part_two(pairs)}")
