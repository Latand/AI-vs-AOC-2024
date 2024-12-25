from collections import defaultdict
from typing import List, Set, Tuple, Dict
import math


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_grid(data: str) -> Dict[str, List[Tuple[int, int]]]:
    """Parse the input grid and return a dictionary mapping frequencies to antenna positions."""
    frequencies = defaultdict(list)
    lines = data.split("\n")
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != ".":
                frequencies[char].append((x, y))
    return frequencies


def is_collinear(p1: Tuple[int, int], p2: Tuple[int, int], p3: Tuple[int, int]) -> bool:
    """Check if three points are collinear."""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    # Using the cross product method to check collinearity
    return (y2 - y1) * (x3 - x1) == (y3 - y1) * (x2 - x1)


def distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> float:
    """Calculate the Euclidean distance between two points."""
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def get_antinodes_part1(
    antennas: List[Tuple[int, int]], grid_bounds: Tuple[int, int]
) -> Set[Tuple[int, int]]:
    """Find antinodes for part 1 (one antenna twice as far as the other)."""
    width, height = grid_bounds
    antinodes = set()

    if len(antennas) < 2:
        return antinodes

    # Check all possible pairs of antennas
    for i, a1 in enumerate(antennas):
        for j, a2 in enumerate(antennas[i + 1 :], i + 1):
            # For each point in the grid
            for x in range(width):
                for y in range(height):
                    point = (x, y)
                    if point == a1 or point == a2:
                        continue

                    # Check if point is collinear with the two antennas
                    if is_collinear(a1, a2, point):
                        d1 = distance(point, a1)
                        d2 = distance(point, a2)
                        # Check if one distance is twice the other
                        if abs(d1 - 2 * d2) < 0.0001 or abs(d2 - 2 * d1) < 0.0001:
                            antinodes.add(point)

    return antinodes


def get_antinodes_part2(
    antennas: List[Tuple[int, int]], grid_bounds: Tuple[int, int]
) -> Set[Tuple[int, int]]:
    """Find antinodes for part 2 (any collinear points)."""
    width, height = grid_bounds
    antinodes = set()

    if len(antennas) < 2:
        return antinodes

    # Add antenna positions as potential antinodes
    antenna_set = set(antennas)

    # Check all possible triplets of points
    for x in range(width):
        for y in range(height):
            point = (x, y)
            # Count how many pairs of antennas this point is collinear with
            collinear_count = 0

            for i, a1 in enumerate(antennas):
                if collinear_count > 0:  # We've already found a collinear pair
                    break

                for a2 in antennas[i + 1 :]:
                    if point != a1 and point != a2 and is_collinear(point, a1, a2):
                        collinear_count += 1
                        break

            if collinear_count > 0 or point in antenna_set:
                antinodes.add(point)

    return antinodes


def get_grid_bounds(frequencies: Dict[str, List[Tuple[int, int]]]) -> Tuple[int, int]:
    """Calculate the grid bounds from the antenna positions."""
    max_x = max_y = 0
    for positions in frequencies.values():
        for x, y in positions:
            max_x = max(max_x, x + 1)
            max_y = max(max_y, y + 1)
    return max_x, max_y


def part1(data: str) -> int:
    """Solution for part 1"""
    frequencies = parse_grid(data)
    grid_bounds = get_grid_bounds(frequencies)

    # Get all antinodes for each frequency
    all_antinodes = set()
    for freq_antennas in frequencies.values():
        antinodes = get_antinodes_part1(freq_antennas, grid_bounds)
        all_antinodes.update(antinodes)

    return len(all_antinodes)


def part2(data: str) -> int:
    """Solution for part 2"""
    frequencies = parse_grid(data)
    grid_bounds = get_grid_bounds(frequencies)

    # Get all antinodes for each frequency
    all_antinodes = set()
    for freq_antennas in frequencies.values():
        antinodes = get_antinodes_part2(freq_antennas, grid_bounds)
        all_antinodes.update(antinodes)

    return len(all_antinodes)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
