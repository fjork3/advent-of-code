from typing import List

DAY_NUMBER = 1


def read_input() -> List[List[int]]:
    with open(f"inputs/input{DAY_NUMBER:0>2}.txt", "r") as f:
        current_elf: List[int] = []
        elves: List[List[int]] = []
        for cal in f.readlines():
            if cal != "\n":
                current_elf.append(int(cal))
            else:
                elves.append(current_elf)
                current_elf = []
    return elves


# max calories for one elf
def part_one(elves: List[List[int]]) -> int:
    return max([sum(elf) for elf in elves])


# total calories of top 3 elves
def part_two(elves: List[List[int]]):
    cals = [sum(elf) for elf in elves]
    cals.sort(reverse=True)
    return sum(cals[0:3])


elves = read_input()
print(f"Day {DAY_NUMBER}, part 1: {part_one(elves)}")
print(f"Day {DAY_NUMBER}, part 2: {part_two(elves)}")
