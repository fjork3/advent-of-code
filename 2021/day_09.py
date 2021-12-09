from collections import Counter, defaultdict, deque
from typing import Dict, List, Tuple

from numpy import prod

with open("inputs/input9.txt", "r") as f:
    board: List[List[int]] = []
    for line in f.readlines():
        board.append([int(x) for x in line.rstrip()])


def coords_in_board(row: int, col: int):
    return 0 <= row < len(board) and 0 <= col < len(board[0])


def get_neighbors(row: int, col: int):
    return filter(
        lambda x: coords_in_board(*x),
        [(row, col - 1), (row, col + 1), (row - 1, col), (row + 1, col)],
    )


def is_local_minima(row: int, col: int) -> bool:
    height = board[row][col]
    for n_row, n_col in get_neighbors(row, col):
        if board[n_row][n_col] <= height:
            return False
    return True


# part 1: find all local minima (strictly smaller than orthogonal neighbors)
# also seed part 2 with basin origins
risk_level = 0
basin_origins: List[Tuple[int, int]] = []
for row in range(len(board)):
    for col in range(len(board[0])):
        if is_local_minima(row, col):
            risk_level += board[row][col] + 1
            basin_origins.append((row, col))

print(f"Day 9, part 1: {risk_level}")


# part 2: find all distinct basins
# perform BFS, starting with origin points
point_to_basin_origin: Dict[Tuple[int, int], Tuple[int, int]] = {}
# True if point has already been put into expansion queue, or definitely not of interest
visited: Dict[Tuple[int, int], bool] = defaultdict(bool)
search_queue: deque = deque()
for origin in basin_origins:
    visited[origin] = True
    point_to_basin_origin[origin] = origin
    search_queue.append(origin)


# perform a BFS
# - add all points that feed into this one to the search queue
# - discard definitely not of interest (i.e. 9s)
while search_queue:
    current = search_queue.popleft()
    row, col = current
    height = board[row][col]
    for neighbor in get_neighbors(row, col):
        if not visited[neighbor]:
            n_row, n_col = neighbor
            n_height = board[n_row][n_col]
            if n_height == 9:
                # will never be of interest; mark and move on
                visited[neighbor] = True
            elif n_height > height:
                # neighbor will flow into this point; join the same basin and search out
                visited[neighbor] = True
                point_to_basin_origin[neighbor] = point_to_basin_origin[current]
                search_queue.append(neighbor)

# reverse mapping to get all points with the same basin origin
basin_sizes = Counter(point_to_basin_origin.values())
output = prod([x[1] for x in basin_sizes.most_common(3)])
print(f"Day 9, part 2: {output}")
