from dataclasses import dataclass
from typing import Dict, List
from numpy import prod

DAY_NUMBER = 2

@dataclass
class CubeGame:
    id: int
    pulls: List[Dict[str, int]]

    def valid_game(self):
        return all(pull.get('red', 0) <= 12 and
                   pull.get('green', 0) <= 13 and
                   pull.get('blue', 0) <= 14
                   for pull in self.pulls)

    def min_cubes(self) -> Dict[str, int]:
        return {color: max(pull.get(color, 0) for pull in self.pulls) for color in ['red', 'green', 'blue']}

    def power(self) -> int:
        return prod(list(self.min_cubes().values()))


def read_input():
    games: List[CubeGame] = []
    with open(f"inputs/input{DAY_NUMBER:0>2}.txt", "r") as f:
        for game in f.read().splitlines():
            id, gamestr = game.split(":")
            id = int(id.split(" ")[-1])
            pulls = []
            for pull in gamestr.split(";"):
                colors = {p.strip().split(" ")[1]: int(p.strip().split(" ")[0]) for p in pull.split(",")}
                pulls.append(colors)

            games.append(CubeGame(id=id, pulls=pulls))
    return games


def part_one():
    games = read_input()
    total_id = 0

    for game in games:
        if game.valid_game():
            total_id += game.id

    return total_id


def part_two():
    games = read_input()
    return sum(game.power() for game in games)


print(f"Day {DAY_NUMBER}, part 1: {part_one()}")
print(f"Day {DAY_NUMBER}, part 2: {part_two()}")
