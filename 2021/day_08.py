from typing import Dict
from collections import Counter

with open("inputs/input8.txt", "r") as f:
    signal_patterns = []
    outputs = []
    for line in f.readlines():
        split_line = line.rstrip().split(" | ")
        signal_patterns.append(split_line[0].split(" "))
        outputs.append(split_line[1].split(" "))

# Part 1: count unique-length digits in outputs
unique_digits_count = 0
for output in outputs:
    for digit in output:
        if len(digit) in (2, 3, 4, 7):
            unique_digits_count += 1
print(f"Day 8, part 1: {unique_digits_count}")

# output segments corresponding to each digit
DIGITS_TO_SEGMENTS = {
    0: set("abcefg"),
    1: set("cf"),
    2: set("acdeg"),
    3: set("acdfg"),
    4: set("bcdf"),
    5: set("abdfg"),
    6: set("abdefg"),
    7: set("acf"),
    8: set("abcdefg"),
    9: set("abcdfg"),
}

SEGMENTS_TO_DIGITS = {
    frozenset(DIGITS_TO_SEGMENTS[k]): k for k in DIGITS_TO_SEGMENTS.keys()
}

# do we have any segments with unique counts across digits?
SEGMENT_COUNTS = Counter()
for digit in DIGITS_TO_SEGMENTS:
    SEGMENT_COUNTS.update(DIGITS_TO_SEGMENTS[digit])
# Counter({'f': 9, 'a': 8, 'c': 8, 'g': 7, 'd': 7, 'b': 6, 'e': 4})
# unique values: 4 -> E, 6 -> B, 9 -> F

running_total = 0

# each display is wired differently, so need to solve each one individually
for display_number, display_pattern in enumerate(signal_patterns):
    # known input -> output (single segment) pairs
    known_segment_mappings: Dict[str, str] = {}
    # known digit -> output set pairs
    known_digits: Dict[int, set] = {}

    possible_segment_mappings: Dict[str, set] = {}

    unknown_patterns = display_pattern

    # find known digits up front
    for pattern in display_pattern:
        if len(pattern) == 2:
            known_digits[1] = set(pattern)
            for c in pattern:
                possible_segment_mappings[c] = set("cf")
        elif len(pattern) == 3:
            known_digits[7] = set(pattern)
            for c in pattern:
                if c not in possible_segment_mappings:
                    possible_segment_mappings[c] = set("acf")
        elif len(pattern) == 4:
            known_digits[4] = set(pattern)
            for c in pattern:
                if c not in possible_segment_mappings:
                    possible_segment_mappings[c] = set("bcdf")
                else:
                    possible_segment_mappings[c] = possible_segment_mappings[c] & set(
                        "bcdf"
                    )
        elif len(pattern) == 7:
            known_digits[8] = set(pattern)
            for c in pattern:
                if c not in possible_segment_mappings:
                    possible_segment_mappings[c] = set("abcdefg")

    def add_known_segment_mapping(input_seg: str, output_seg: str):
        known_segment_mappings[input_seg] = output_seg
        # remove output_seg from
        for seg in possible_segment_mappings:
            possible_segment_mappings[seg] = possible_segment_mappings[seg] - {
                output_seg
            }
        possible_segment_mappings.pop(input_seg)

    def print_debug_state():
        print("###############")
        print(f"known_segment_mappings: {known_segment_mappings}")
        print(f"possible_segment_mappings: {possible_segment_mappings}")
        print(f"known_digits: {known_digits}")
        print("###############")

    def sweep_for_known_mapping():
        print(possible_segment_mappings)
        while possible_segment_mappings:
            for unknown_seg in possible_segment_mappings:
                if len(possible_segment_mappings[unknown_seg]) == 1:
                    output_seg = possible_segment_mappings[unknown_seg].pop()
                    # print(f"Found unambiguous mapping! {unknown_seg} -> {output_seg}")
                    add_known_segment_mapping(unknown_seg, output_seg)
                    break

    # we can find some mappings based on segment counts!
    segment_counts = Counter()
    for digit in display_pattern:
        segment_counts.update(digit)
    for input_segment in segment_counts:
        if segment_counts[input_segment] == 4:
            add_known_segment_mapping(input_segment, "e")
        elif segment_counts[input_segment] == 6:
            add_known_segment_mapping(input_segment, "b")
        elif segment_counts[input_segment] == 9:
            add_known_segment_mapping(input_segment, "f")

    # print_debug_state()

    # segment A: found in 7 and not 1
    for segment in "abcdefg":
        if segment in known_digits[7] and segment not in known_digits[1]:
            add_known_segment_mapping(segment, "a")

    # print_debug_state()

    # we now have enough info to unambiguously find all segments!
    # keep sweeping through possible mappings for ones with only 1 possibility remaining
    sweep_for_known_mapping()
    # print_debug_state()

    # we now have all input -> output segments; figure out what the displayed digits are
    numerical_digits = []
    for digit in outputs[display_number]:
        output_segments = frozenset({known_segment_mappings[s] for s in digit})
        numerical_digits.append(SEGMENTS_TO_DIGITS[output_segments])
    output_number = (
        1000 * numerical_digits[0]
        + 100 * numerical_digits[1]
        + 10 * numerical_digits[2]
        + numerical_digits[3]
    )
    running_total += output_number
    print(running_total)


print(f"Day 8, part 2: {running_total}")
