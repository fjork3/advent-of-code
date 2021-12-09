from collections import Counter
from typing import List


def puzzle5() -> int:
    class LineSegment:
        def __init__(self, inputline: str):
            point1, point2 = inputline.split(" -> ")
            x1, y1 = point1.split(",")
            x2, y2 = point2.split(",")
            self.x1 = int(x1)
            self.y1 = int(y1)
            self.x2 = int(x2)
            self.y2 = int(y2)

        def is_orthogonal(self):
            return (self.x1 == self.x2) or (self.y1 == self.y2)

        def covered_points(self) -> List[tuple]:
            if self.x1 == self.x2:
                y_start, y_end = min(self.y1, self.y2), max(self.y1, self.y2)
                return [(self.x1, y) for y in range(y_start, y_end + 1)]
            if self.y1 == self.y2:
                x_start, x_end = min(self.x1, self.x2), max(self.x1, self.x2)
                return [(x, self.y1) for x in range(x_start, x_end + 1)]

            # diagonal lines
            line_length = abs(self.x1 - self.x2)
            x_step_dir = 1 if self.x1 < self.x2 else -1
            y_step_dir = 1 if self.y1 < self.y2 else -1
            return [
                (self.x1 + (i * x_step_dir), self.y1 + (i * y_step_dir))
                for i in range(line_length + 1)
            ]

    def segments_to_cover(segments: List[LineSegment]) -> Counter:
        covered_points = Counter()
        for segment in segments:
            covered_points.update(segment.covered_points())
        return covered_points

    with open("inputs/input5.txt", "r") as f:
        line_segments = [LineSegment(line.rstrip()) for line in f]

    # part 1: orthogonal only
    # orthogonal_segments = [segment for segment in line_segments if segment.is_orthogonal()]
    # covered_points = segments_to_cover(orthogonal_segments)
    # return len([point for point in covered_points if covered_points[point] > 1])

    # part 2: all segments
    covered_points = segments_to_cover(line_segments)
    return len([point for point in covered_points if covered_points[point] > 1])


print(f"Day 5: {puzzle5()}")
