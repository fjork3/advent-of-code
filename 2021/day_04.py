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

    with open("inputs/input4.txt", "r") as f:
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
        bingo_boards = [
            board for board in bingo_boards if score_board(board) < 0
        ]  # keep unsolved boards
        if len(bingo_boards) == 1:
            # finish out the last board, then score it
            next_num = 0
            while score_board(bingo_boards[0]) < 0:
                next_num = called_numbers.__next__()  # DON'T DO THIS
                call_number(next_num)

            return score_board(bingo_boards[0]) * next_num


print(f"Day 4: {puzzle4()}")
