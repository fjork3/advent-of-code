from collections import Counter, defaultdict
from typing import Dict, Tuple


def read_input() -> Tuple[str, Dict]:
    with open("inputs/input14.txt", "r") as f:
        sequence = f.readline().rstrip()
        f.readline()
        insertions = defaultdict(str)
        while line := f.readline():
            pair, insert = line.rstrip().split(" -> ")
            insertions[pair] = insert
    return sequence, insertions


def step(sequence: str, insertions: Dict):
    output = ""
    for i in range(len(sequence)):
        output += sequence[i]
        output += insertions[
            sequence[i : i + 2]
        ]  # will insert empty string if not in listed pairs
    # DEBUG
    print(f"step complete! new polymer size: {len(output)}")
    return output


def part_one():
    sequence, insertions = read_input()
    for i in range(10):
        sequence = step(sequence, insertions)
    # most common element minus least common
    counts = Counter(sequence)
    return max(counts.values()) - min(counts.values())


def part_two():
    sequence, insertions = read_input()
    for i in range(40):
        sequence = step(sequence, insertions)
    # most common element minus least common
    counts = Counter(sequence)
    return max(counts.values()) - min(counts.values())


print(f"Day 14, part 1: {part_one()}")
print(f"Day 14, part 2: {part_two()}")
