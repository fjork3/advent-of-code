from typing import Dict, Set


class Node:
    def __init__(self, name: str):
        self.name = name
        self.is_large = name.isupper()
        self.connections: Set[Node] = set()

    def __str__(self):
        connections = ",".join([n.name for n in self.connections])
        return f"Node {self.name}: connects to {connections}"

    def add_connection(self, node):
        self.connections.add(node)


def read_input() -> Dict[str, Node]:
    nodes: Dict[str, Node] = {}
    with open("inputs/input12.txt", "r") as f:
        for line in f.readlines():
            a, b = line.rstrip().split("-")
            if a not in nodes:
                nodes[a] = Node(a)
            if b not in nodes:
                nodes[b] = Node(b)
            nodes[a].add_connection(nodes[b])
            nodes[b].add_connection(nodes[a])
    return nodes


# find all graph traversals
def part_one():
    nodes = read_input()
    visited_paths: Set[str] = set()
    complete_paths = 0

    def visit_node(node: str, path: str):
        nonlocal complete_paths
        new_path = f"{path},{node}"
        if new_path in visited_paths:
            return
        if node == "end":
            complete_paths += 1
            return
        visited_paths.add(new_path)
        nodes_in_path = path.split(",")
        for neighbor in nodes[node].connections:
            # skip small caves we've already visited on this path
            if neighbor.name not in nodes_in_path or neighbor.is_large:
                visit_node(neighbor.name, new_path)

    for node in nodes["start"].connections:
        visit_node(node.name, "start")
    return complete_paths


# find all graph traversals, but we can visit one small cave twice
def part_two():
    nodes = read_input()
    visited_paths: Set[str] = set()
    complete_paths = 0
    debug_complete_paths = []

    def visit_node(node: str, path: str, repeat_taken: bool):
        nonlocal complete_paths
        new_path = f"{path},{node}"
        if new_path in visited_paths:
            return
        if node == "end":
            complete_paths += 1
            debug_complete_paths.append(new_path)
            return
        # can't visit the start node more than once
        if node == "start":
            return
        visited_paths.add(new_path)
        nodes_in_path = path.split(",")
        for neighbor in nodes[node].connections:
            # don't repeat more than one small node
            if neighbor.name in nodes_in_path and not neighbor.is_large and repeat_taken:
                continue
            # if not visited or large, visit as normal (keeping status about taken repeat)
            if neighbor.name not in nodes_in_path or neighbor.is_large:
                visit_node(neighbor.name, new_path, repeat_taken)
            # otherwise, we're taking our one repeat node; mark that for future visits
            else:
                visit_node(neighbor.name, new_path, True)

    for node in nodes["start"].connections:
        visit_node(node.name, "start", False)

    return complete_paths


print(f"Day 12, part 1: {part_one()}")
print(f"Day 12, part 2: {part_two()}")
