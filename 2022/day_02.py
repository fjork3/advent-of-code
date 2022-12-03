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


ROCK = 1
PAPER = 2
SCISSORS = 3

op_plays_decode = {
    "A": ROCK,
    "B": PAPER,
    "C": SCISSORS
}

my_plays_decode = {
    "X": ROCK,
    "Y": PAPER,
    "Z": SCISSORS
}

results_decode = {
    "X": "loss",
    "Y": "draw",
    "Z": "win"
}


# constrain to range 1-3
def bound_result(result: int) -> int:
    return ((result-1) % 3) + 1


def round_score(op_play: int, my_play: int) -> int:
    score = my_play
    if my_play == op_play:
        score += 3
    elif (my_play - op_play) % 3 == 1:
        score += 6
    return score


# X for lose, Y for draw, Z for win
def round_score_result(op_play: int, result: str) -> int:
    my_play = op_play
    if result == "win":
        my_play = bound_result(op_play + 1)
    elif result == "loss":
        my_play = bound_result(op_play - 1)

    return round_score(op_play, my_play)


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
