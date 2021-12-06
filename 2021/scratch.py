from typing import List
from collections import Counter

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


# print(f"Day 2: {puzzle2()}")


def puzzle3():
    with open('input3.txt', 'r') as f:
        readings = list(map(lambda x: list(x)[:-1], f.readlines())) # strip newline
    bit_values = list(map(list, zip(*readings)))
    most_common_bits = []
    least_common_bits = []
    for bit_pos in bit_values:
        most_common_bits.append("1" if (bit_pos.count("1") > len(bit_pos)/2) else "0")
        least_common_bits.append("1" if most_common_bits[-1] == "0" else "0")

    gamma = int(''.join(most_common_bits), 2)
    epsilon = int(''.join(least_common_bits), 2)
    # return gamma * epsilon // part 1

    def most_common_bit(readings: list, pos: int, default: str) -> str:
        bit_values = list(map(list, zip(*readings)))
        one_count = bit_values[pos].count("1")
        if one_count > len(readings)/2:
            return "1"
        if one_count == len(readings)/2:
            return default
        return "0"


    def oxygen_rating(readings: list, pos: int) -> str:
        return most_common_bit(readings, pos, "1")

    def co2_rating(readings: list, pos: int) -> str:
        return "1" if oxygen_rating(readings, pos) == "0" else "0"

    oxygen_readings = list(readings)
    pos = 0
    while len(oxygen_readings) > 1 and pos < len(oxygen_readings[0]):
        rating = oxygen_rating(oxygen_readings, pos)
        oxygen_readings = [x for x in oxygen_readings if x[pos] == rating]
        pos += 1
    oxygen = oxygen_readings[0]
    oxygen = int(''.join(oxygen), 2)

    co2_readings = list(readings)
    pos = 0
    while len(co2_readings) > 1 and pos < len(co2_readings[0]):
        rating = co2_rating(co2_readings, pos)
        co2_readings = [x for x in co2_readings if x[pos] == rating]
        pos += 1
    co2 = co2_readings[0]
    co2 = int(''.join(co2), 2)

    return oxygen * co2


# print(f"Day 3: {puzzle3()}")

def puzzle4():

    def is_bingo_board_solved(board: list) -> bool:
        for row in board:
            if all([x < 0 for x in row]):
                return True
        for col in zip(*board):
            if all([x < 0 for x in col]):
                return True
        return False

    def score_board(board: list) -> int:
        if not is_bingo_board_solved(board):
            return -1
        board = [[max(0, x) for x in row] for row in board]
        return sum([sum(row) for row in board])

    # Update internal state for number being called
    def call_number(num: int):
        for j, board in enumerate(bingo_boards):
            bingo_boards[j] = [[-1 if x == num else x for x in row] for row in board]

    with open('input4.txt', 'r') as f:
        called_numbers = map(int, f.readline().split(","))
        bingo_boards = []
        while f.readline():
            next_square = []
            for i in range(5):
                next_square.append([int(x) for x in f.readline().split(" ") if x])
            bingo_boards.append(next_square)

    # Part 1: win first
    # for num in called_numbers:
    #     call_number(num)
    #     for board in bingo_boards:
    #         result = score_board(board)
    #         if result >= 0:
    #             return result * num
    # return None # SOMETHING HAS GONE WRONG

    # Part 2: win last
    for num in called_numbers:
        call_number(num)
        bingo_boards = [board for board in bingo_boards if score_board(board) < 0] # keep unsolved boards
        if len(bingo_boards) == 1:
            # finish out the last board, then score it
            next_num = 0
            while score_board(bingo_boards[0]) < 0:
                next_num = called_numbers.__next__()    # DON'T DO THIS
                call_number(next_num)

            return score_board(bingo_boards[0]) * next_num


# print(f"Day 4: {puzzle4()}")

def puzzle5() -> int:
    class LineSegment:
        def __init__(self, inputline: str):
            point1, point2 = inputline.split(" -> ")
            x1, y1 = point1.split(",")
            x2, y2 = point2.split(",")
            self.x1 = int(x1)
            self.y1 = int(y1)
            self.x2 = int(x2)
            self.y2 = int(y2)

        def is_orthogonal(self):
            return (self.x1 == self.x2) or (self.y1 == self.y2)

        def covered_points(self) -> List[tuple]:
            if self.x1 == self.x2:
                y_start, y_end = min(self.y1, self.y2), max(self.y1, self.y2)
                return [(self.x1, y) for y in range(y_start, y_end + 1)]
            if self.y1 == self.y2:
                x_start, x_end = min(self.x1, self.x2), max(self.x1, self.x2)
                return [(x, self.y1) for x in range(x_start, x_end + 1)]

            # diagonal lines
            line_length = abs(self.x1 - self.x2)
            x_step_dir = 1 if self.x1 < self.x2 else -1
            y_step_dir = 1 if self.y1 < self.y2 else -1
            return [(self.x1 + (i * x_step_dir), self.y1 + (i * y_step_dir)) for i in range(line_length + 1)]


    def segments_to_cover(segments: List[LineSegment]) -> Counter:
        covered_points = Counter()
        for segment in segments:
            covered_points.update(segment.covered_points())
        return covered_points

    with open('input5.txt', 'r') as f:
        line_segments = [LineSegment(line.rstrip()) for line in f]



    # part 1: orthogonal only
    # orthogonal_segments = [segment for segment in line_segments if segment.is_orthogonal()]
    # covered_points = segments_to_cover(orthogonal_segments)
    # return len([point for point in covered_points if covered_points[point] > 1])

    # part 2: all segments
    covered_points = segments_to_cover(line_segments)
    return len([point for point in covered_points if covered_points[point] > 1])


# print(f"Day 5: {puzzle5()}")

def puzzle6():
    def advance_day(fish: dict) -> dict:
        # each counter decreases by 1
        # all fish at 0 reset to 6 and spawn a new fish at 8
        new_fish = {}
        new_fish[8] = fish[0]
        for i in range(1, 9):
            new_fish[i-1] = fish[i]
        new_fish[6] += fish[0]
        return new_fish

    with open('input6.txt', 'r') as f:
        starting_timers = list(map(int, f.readline().split(",")))

    fish = Counter(starting_timers)
    # num_days = 80 # part 1
    num_days = 256 # part 2
    for i in range(num_days):
        fish = advance_day(fish)
    return sum(fish[key] for key in fish.keys())

print(f"Day 6: {puzzle6()}")
