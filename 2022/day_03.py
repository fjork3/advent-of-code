import string
from typing import List

DAY_NUMBER = 3


def read_input():
    rucksacks = []
    with open(f"inputs/input{DAY_NUMBER:0>2}.txt", "r") as f:
        for line in f.readlines():
            rucksacks.append(line.strip("\n"))
    return rucksacks


def letter_to_priority(c: str) -> int:
    if c in string.ascii_lowercase:
        return ord(c) - ord("a") + 1
    return ord(c) - ord("A") + 27


def part_one(rucksacks: List[str]) -> int:
    priority = 0
    for r in rucksacks:
        seen = set()
        left = r[0:len(r)//2]
        for c in left:
            seen.add(c)
        for c in r[len(r)//2:]:
            if c in seen:
                priority += letter_to_priority(c)
                break
    return priority


def part_two(rucksacks: List[str]) -> int:
    priority = 0
    for i in range(len(rucksacks)//3):
        r1, r2, r3 = rucksacks[3*i:3*i + 3]
        seen = set()
        seen2 = set()
        for c in r1:
            seen.add(c)
        for c in r2:
            if c in seen:
                seen2.add(c)
        for c in r3:
            if c in seen and c in seen2:
                priority += letter_to_priority(c)
                break
    return priority


rucksacks = read_input()
print(f"Day {DAY_NUMBER}, part 1: {part_one(rucksacks)}")
print(f"Day {DAY_NUMBER}, part 2: {part_two(rucksacks)}")
