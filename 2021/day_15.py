from __future__ import annotations

import math
from typing import Dict, Set, Tuple

# based on provided input
MAX_ROW = 100
MAX_COL = 100


def read_input():
    with open("inputs/input15.txt", "r") as f:
        board = [[int(c) for c in line.rstrip()] for line in f.readlines()]

    return board


def coords_in_board(row: int, col: int):
    return 0 <= row < MAX_ROW and 0 <= col < MAX_COL


def get_neighbors(row: int, col: int):
    return filter(
        lambda x: coords_in_board(*x),
        [(row, col - 1), (row, col + 1), (row - 1, col), (row + 1, col)],
    )


# we gonna Dijkstra's it
class Node:
    def __init__(self, risk):
        self.cumulative_risk = math.inf
        self.risk = risk
        self.is_end = False
        self.neighbors: Set[Node] = set()

    def add_neighbor(self, neighbor: Node):
        self.neighbors.add(neighbor)

    def visit_node(self, unvisited: Set[Node]):
        if self.is_end:
            return self.cumulative_risk
        for neighbor in self.neighbors:
            if neighbor in unvisited:
                neighbor.cumulative_risk = min(
                    self.cumulative_risk + neighbor.risk, neighbor.cumulative_risk
                )
        unvisited.remove(self)
        return None

    def __repr__(self):
        return f"Node: cumulative_risk: {self.cumulative_risk}, risk: {self.risk}, is_end: {self.is_end}, neighbors: {len(self.neighbors)}"


def next_node(unvisited: Set[Node]):
    return min(unvisited, key=lambda x: x.cumulative_risk)


def part_one():
    board = read_input()
    all_nodes: Dict[Tuple[int, int], Node] = {}
    for row in range(len(board)):
        for col in range(len(board[0])):
            all_nodes[row, col] = Node(board[row][col])
    all_nodes[0, 0].cumulative_risk = 0
    all_nodes[MAX_ROW-1, MAX_COL-1].is_end = True

    for row in range(len(board)):
        for col in range(len(board[0])):
            for n_row, n_col in get_neighbors(row, col):
                all_nodes[row, col].add_neighbor(all_nodes[n_row, n_col])

    unvisited_nodes: Set[Node] = set(all_nodes.values())
    while unvisited_nodes:
        n = next_node(unvisited_nodes)
        if n.visit_node(unvisited_nodes) is not None:
            return n.cumulative_risk


# input is actually tiled 5x in each direction; 1 tile left or right adds 1 risk, wrapping mod 9
def part_two():
    board = read_input()
    all_nodes: Dict[Tuple[int, int], Node] = {}
    for row in range(len(board)):
        for col in range(len(board[0])):
            for tile_x in range(5):
                for tile_y in range(5):
                    base_risk = board[row][col]
                    risk = (base_risk + tile_x + tile_y) % 9
                    if risk == 0:
                        risk = 9
                    all_nodes[row + MAX_ROW*tile_y, col + MAX_COL*tile_x] = Node(risk)
    all_nodes[0, 0].cumulative_risk = 0
    all_nodes[499, 499].is_end = True
    unvisited_nodes: Set[Node] = set(all_nodes.values())
    while unvisited_nodes:
        n = next_node(unvisited_nodes)
        if n.visit_node(unvisited_nodes) is not None:
            return n.cumulative_risk


print(f"Day 15, part 1: {part_one()}")
print(f"Day 15, part 2: {part_two()}")
