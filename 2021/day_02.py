def puzzle2() -> int:
    with open("inputs/input02.txt", "r") as f:
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
