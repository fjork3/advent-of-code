def puzzle1(windowsize: int) -> int:
    with open('input1.txt', 'r') as f:
        depths = f.readlines()
        depths = [int(x) for x in depths]
        diffs = [depths[i+windowsize] - depths[i] for i in range(len(depths)-windowsize)]
        return sum([x > 0 for x in diffs])

# print(f"Day 1, part 1: {puzzle1(1)}")
# print(f"Day 1, part 2: {puzzle1(3)}")

def puzzle2() -> int:
    with open('input2.txt', 'r') as f:
        commands = map(lambda x: x.split(" "), f.readlines())
    x_pos = 0
    y_pos = 0
    aim = 0
    for (dir, step) in commands:
        step = int(step)
        if dir == "forward":
            x_pos += step
            y_pos += step * aim
        elif dir == "up":
            aim -= step
        elif dir == "down":
            aim += step

    return x_pos * y_pos


print(f"Day 2: {puzzle2()}")
