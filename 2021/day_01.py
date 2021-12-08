def puzzle1(windowsize: int) -> int:
    with open("inputs/input1.txt", "r") as f:
        depths = f.readlines()
        depths = [int(x) for x in depths]
        diffs = [
            depths[i + windowsize] - depths[i] for i in range(len(depths) - windowsize)
        ]
        return sum([x > 0 for x in diffs])


print(f"Day 1, part 1: {puzzle1(1)}")
print(f"Day 1, part 2: {puzzle1(3)}")
