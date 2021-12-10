from math import floor
from typing import List

with open("inputs/input10.txt", "r") as f:
    lines: List[str] = [line.rstrip() for line in f.readlines()]

illegal_char_score = {")": 3, "]": 57, "}": 1197, ">": 25137}
autocomplete_char_score = {")": 1, "]": 2, "}": 3, ">": 4}

opening_chars = "([{<"
closing_chars = ")]}>"
closing_to_opening = {")": "(", "]": "[", "}": "{", ">": "<"}
opening_to_closing = {"(": ")", "[": "]", "{": "}", "<": ">"}


def illegal_char_in_line(line: str):
    pending_opening_chars = []
    for c in line:
        if c in opening_chars:
            pending_opening_chars.append(c)
        else:
            if closing_to_opening[c] != pending_opening_chars.pop():
                return c
    return None


def part_one():
    running_score = 0
    for line in lines:
        illegal_char = illegal_char_in_line(line)
        if illegal_char is not None:
            running_score += illegal_char_score[illegal_char]
    return running_score


def part_two():
    incomplete_lines = [line for line in lines if illegal_char_in_line(line) is None]
    line_scores = []
    for line in incomplete_lines:
        pending_opening_chars = []
        for c in line:
            if c in opening_chars:
                pending_opening_chars.append(c)
            else:
                pending_opening_chars.pop()
        line_score = 0
        while pending_opening_chars:
            c = pending_opening_chars.pop()
            line_score *= 5
            line_score += autocomplete_char_score[opening_to_closing[c]]
        line_scores.append(line_score)
    line_scores.sort()
    # return median element
    return line_scores[floor(len(line_scores) / 2)]


print(f"Day 10, part 1: {part_one()}")
print(f"Day 10, part 2: {part_two()}")
