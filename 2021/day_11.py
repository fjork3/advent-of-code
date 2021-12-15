from collections import defaultdict
from typing import Dict, List, Tuple


def read_input() -> Dict[Tuple[int, int], int]:
    with open("inputs/input11.txt", "r") as f:
        board: List[List[int]] = [
            [int(x) for x in line.rstrip()] for line in f.readlines()
        ]
        return {
            (row, col): board[row][col]
            for row in range(len(board))
            for col in range(len(board[0]))
        }


def coords_in_board(row: int, col: int):
    max_row = 10
    max_col = 10
    return 0 <= row < max_row and 0 <= col < max_col


def get_neighbors(row: int, col: int):
    return filter(
        lambda x: coords_in_board(*x),
        [(row + x, col + y) for x in (-1, 0, 1) for y in (-1, 0, 1)],
    )


# modify internal state for one time step, and return number of octopi that flashed
def step(board: Dict[Tuple[int, int], int]) -> int:
    flashed = defaultdict(bool)
    # increase energy of all octopi by 1, then see if they trigger and cascade
    for (row, col) in board:
        board[(row, col)] += 1
        maybe_flash(row, col, flashed, board)

    # reset all flashed octopi
    flashed_octopi = 0
    for row, col in flashed:
        if flashed[(row, col)]:
            board[(row, col)] = 0
            flashed_octopi += 1
    return flashed_octopi


# process potential flashing, then mark as flashed
def maybe_flash(row: int, col: int, flashed: dict, board: Dict[Tuple[int, int], int]):
    if not flashed[(row, col)] and board[(row, col)] > 9:
        flashed[(row, col)] = True
        for n_row, n_col in get_neighbors(row, col):
            board[(n_row, n_col)] += 1
            if board[(n_row, n_col)] > 9:
                maybe_flash(n_row, n_col, flashed, board)


def part_one() -> int:
    board = read_input()
    flashes = 0
    for _ in range(100):
        flashes += step(board)
    return flashes


def part_two() -> int:
    board = read_input()
    total_octopi = len(board)
    t = 1  # assume always at least 1 step
    while step(board) < total_octopi:
        t += 1
    return t


print(f"Day 11, part 1: {part_one()}")
print(f"Day 11, part 2: {part_two()}")
