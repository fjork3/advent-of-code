from __future__ import annotations

import math
from typing import Dict, Set, Tuple

import numpy as np


def read_input() -> np.array:
    with open("inputs/input15.txt", "r") as f:
        board = [[int(c) for c in line.rstrip()] for line in f.readlines()]

    return np.asarray(board)


def coords_in_board(row: int, col: int, max_rows: int, max_cols: int) -> bool:
    return 0 <= row < max_rows and 0 <= col < max_cols


def get_neighbors(row: int, col: int, max_rows: int, max_cols: int):
    return filter(
        lambda x: coords_in_board(*x, max_rows, max_cols),
        [(row, col - 1), (row, col + 1), (row - 1, col), (row + 1, col)],
    )


# we gonna Dijkstra's it
# just kidding, A*
class Node:
    def __init__(self, row, col, risk):
        self.cumulative_risk = math.inf
        self.row = row
        self.col = col
        self.risk = risk
        self.is_end = False
        self.neighbors: Set[Node] = set()

    def add_neighbor(self, neighbor: Node):
        self.neighbors.add(neighbor)

    def visit_node(self, unvisited: Set[Node], visited: Set[Node]) -> None:
        for neighbor in self.neighbors:
            if neighbor in visited:
                continue
            neighbor.cumulative_risk = min(
                self.cumulative_risk + neighbor.risk, neighbor.cumulative_risk
            )
            unvisited.add(neighbor)
        unvisited.remove(self)
        visited.add(self)

    # tightest guaranteed lower bound on cost from current spot to end
    def weight_heuristic(self, rows, cols) -> int:
        return self.cumulative_risk + (rows - self.row + cols - self.col)


# Run A* algorithm, with start and end nodes pre-marked
def run_a_star(nodes: Dict[Tuple[int, int], Node]) -> int:
    # for speed of finding next node, we only want to consider nodes with a non-infinite weight when possible
    unvisited_nodes: Set[Node] = set()
    visited_nodes: Set[Node] = set()
    unvisited_nodes.add(nodes[0, 0])

    max_row = max(nodes.keys(), key=lambda x: x[1])[1]
    max_col = max(nodes.keys(), key=lambda x: x[0])[0]

    def next_node(unvisited: Set[Node]) -> Node:
        return min(
            unvisited,
            key=lambda x: x.cumulative_risk + x.weight_heuristic(max_row, max_col),
        )

    while unvisited_nodes:
        n = next_node(unvisited_nodes)
        if n.is_end:
            return int(n.cumulative_risk)
        n.visit_node(unvisited_nodes, visited_nodes)


def part_one() -> int:
    board = read_input()
    all_nodes: Dict[Tuple[int, int], Node] = {}

    # initialize empty nodes and mark start/end
    for row, col in np.ndindex(board.shape):
        all_nodes[row, col] = Node(row, col, board[row][col])
    all_nodes[0, 0].cumulative_risk = 0
    all_nodes[99, 99].is_end = True

    # add neighbors
    for row, col in np.ndindex(board.shape):
        for n_row, n_col in get_neighbors(row, col, 100, 100):
            all_nodes[row, col].add_neighbor(all_nodes[n_row, n_col])

    return run_a_star(all_nodes)


# input is actually tiled 5x in each direction; 1 tile left or right adds 1 risk, wrapping mod 9
def part_two() -> int:
    base_board = read_input()
    all_nodes: Dict[Tuple[int, int], Node] = {}

    # tile out duplicated board, with offset based on tiling
    board = np.empty((500, 500), np.int8)
    for tile_y in range(0, 5):
        for tile_x in range(0, 5):
            new_tile: np.array = base_board + tile_x + tile_y
            new_tile = ((new_tile - 1) % 9) + 1
            board[
                100 * tile_y : 100 * (tile_y + 1), 100 * tile_x : 100 * (tile_x + 1)
            ] = new_tile

    # initialize empty nodes and mark start/end
    for row, col in np.ndindex(board.shape):
        all_nodes[row, col] = Node(row, col, board[row][col])
    all_nodes[0, 0].cumulative_risk = 0
    all_nodes[499, 499].is_end = True

    # add neighbors
    for row, col in np.ndindex(board.shape):
        for n_row, n_col in get_neighbors(row, col, 500, 500):
            all_nodes[row, col].add_neighbor(all_nodes[n_row, n_col])

    return run_a_star(all_nodes)


print(f"Day 15, part 1: {part_one()}")
print(f"Day 15, part 2: {part_two()}")
