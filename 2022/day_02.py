DAY_NUMBER = 2


def read_input():
    op_plays = []
    my_plays = []
    with open(f"inputs/input{DAY_NUMBER:0>2}.txt", "r") as f:
        for game in f.read().splitlines():
            throws = game.split(" ")
            op_plays.append(throws[0])
            my_plays.append(throws[1])
    return op_plays, my_plays

score_map = {
    "rock": 1,
    "paper": 2,
    "scissors": 3
}

win_map = {
    "rock": "scissors",
    "paper": "rock",
    "scissors": "paper"
}

op_plays_decode = {
    "A": "rock",
    "B": "paper",
    "C": "scissors"
}

my_plays_decode = {
    "X": "rock",
    "Y": "paper",
    "Z": "scissors"
}

results_decode = {
    "X": "loss",
    "Y": "draw",
    "Z": "win"
}


def round_score(op_play: str, my_play: str) -> int:
    if op_play == my_play:
        return 3 + score_map[my_play]
    if op_play == win_map[my_play]:
        return 6 + score_map[my_play]
    return score_map[my_play]


# X for lose, Y for draw, Z for win
def round_score_result(op_play: str, result: str) -> int:
    if result == "draw":
        return 3 + score_map[op_play]
    if result == "win":
        return 6 + 1 + ((score_map[op_play] + 1) % 3)
    return 1 + ((score_map[op_play] - 1) % 3)


def part_one():
    op_plays, my_plays = read_input()
    score = 0
    for i in range(len(my_plays)):
        score += round_score(op_plays_decode[op_plays[i]], my_plays_decode[my_plays[i]])
    return score


def part_two():
    op_plays, my_plays = read_input()
    score = 0
    for i in range(len(my_plays)):
        score += round_score_result(op_plays_decode[op_plays[i]], results_decode[my_plays[i]])
    return score


print(f"Day {DAY_NUMBER}, part 1: {part_one()}")
print(f"Day {DAY_NUMBER}, part 2: {part_two()}")
