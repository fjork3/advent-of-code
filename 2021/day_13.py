from typing import Set


def read_input():
    points = set()
    folds = []
    with open("inputs/input13.txt", "r") as f:
        for line in f.readlines():
            if "," in line:
                coords = line.rstrip().split(",")
                points.add((int(coords[0]), int(coords[1])))
            elif "fold" in line:
                fold = line.rstrip().split(" ")[-1].split("=")
                folds.append([fold[0], int(fold[1])])
    return points, folds


def perform_fold(points: set, axis: str, at: int) -> Set:
    new_points = set()
    for x, y in points:
        if axis == "x":
            if x < at:
                new_points.add((x, y))
            else:
                new_x = at - (x - at)
                new_points.add((new_x, y))
        if axis == "y":
            if y < at:
                new_points.add((x, y))
            else:
                new_y = at - (y - at)
                new_points.add((x, new_y))
    return new_points


def part_one():
    points, folds = read_input()
    return len(perform_fold(points, *folds[0]))


def part_two():
    points, folds = read_input()
    for fold in folds:
        points = perform_fold(points, *fold)
    # convert to visual matrix
    max_x = max([point[0] for point in points])
    max_y = max([point[1] for point in points])
    output = []
    for y in range(max_y+1):
        output.append([])
        for x in range(max_x+1):
            output[y].append(" ")

    for x, y in points:
        output[y][x] = "*"

    return "\n".join(["".join(line) for line in output])


print(f"Day 13, part 1: {part_one()}")
print(f"Day 13, part 2: \n{part_two()}")
