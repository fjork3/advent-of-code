from collections import Counter


def puzzle6():
    def advance_day(fish: dict) -> dict:
        # each counter decreases by 1
        # all fish at 0 reset to 6 and spawn a new fish at 8
        new_fish = {}
        new_fish[8] = fish[0]
        for i in range(1, 9):
            new_fish[i - 1] = fish[i]
        new_fish[6] += fish[0]
        return new_fish

    with open("inputs/input06.txt", "r") as f:
        starting_timers = list(map(int, f.readline().split(",")))

    fish = Counter(starting_timers)
    # num_days = 80 # part 1
    num_days = 256  # part 2
    for i in range(num_days):
        fish = advance_day(fish)
    return sum(fish[key] for key in fish.keys())


print(f"Day 6: {puzzle6()}")
