from collections import Counter, defaultdict
from typing import Dict, Tuple


def read_input() -> Tuple[str, Dict]:
    with open("inputs/input14.txt", "r") as f:
        sequence = f.readline().rstrip()
        f.readline()
        insertions = {}
        while line := f.readline():
            pair, insert = line.rstrip().split(" -> ")
            insertions[pair] = insert
    return sequence, insertions


def step_brute_force(sequence: str, insertions: Dict):
    output = ""
    for i in range(len(sequence)):
        output += sequence[i]
        if sequence[i : i + 2] in insertions:
            output += insertions[sequence[i : i + 2]]
    return output


def step_pairs(insertions: Dict, counts: Counter) -> Counter:
    # what happens when we do a pair insertion?
    # - if it's in the substitution list, that count goes down by 1 and the overlap counts go up by 1
    # - if it's not in the substitution list, no counts change
    new_counts = counts.copy()
    for pair in counts:
        if pair in insertions:
            n = counts[pair]
            new_counts[pair[0] + insertions[pair]] += n
            new_counts[insertions[pair] + pair[1]] += n
            new_counts[pair] -= n
    return new_counts


def part_one():
    # small enough to brute force quickly
    sequence, insertions = read_input()
    for i in range(10):
        sequence = step_brute_force(sequence, insertions)
    # most common element minus least common
    counts = Counter(sequence)
    return max(counts.values()) - min(counts.values())


def part_two():
    sequence, insertions = read_input()

    pair_counts = Counter(["".join(p) for p in zip(sequence, sequence[1:])])
    for _ in range(40):
        pair_counts = step_pairs(insertions, pair_counts)

    # count only first letter of each pair, to avoid double-counting overlap
    counts = defaultdict(int)
    for pair in pair_counts:
        counts[pair[0]] += pair_counts[pair]
    # final letter isn't part of any pairs (any never changes), account for that
    counts[sequence[-1]] += 1
    print(counts)

    return max(counts.values()) - min(counts.values())


print(f"Day 14, part 1: {part_one()}")
print(f"Day 14, part 2: {part_two()}")
