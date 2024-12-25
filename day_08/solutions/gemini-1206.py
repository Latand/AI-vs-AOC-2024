import math
from collections import defaultdict
from typing import Tuple


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def get_antennas(data: str) -> dict:
    antennas = defaultdict(list)
    for y, line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            if char != ".":
                antennas[char].append((x, y))
    return antennas


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def is_between(p1: Tuple[int, int], p2: Tuple[int, int], p3: Tuple[int, int]) -> bool:
    """Check if point p2 is between p1 and p3."""
    if p1[0] == p3[0]:  # Vertical line
        return p1[0] == p2[0] and min(p1[1], p3[1]) <= p2[1] <= max(p1[1], p3[1])
    if p1[1] == p3[1]:  # Horizontal line
        return p1[1] == p2[1] and min(p1[0], p3[0]) <= p2[0] <= max(p1[0], p3[0])

    # Check if p2 is on the line segment defined by p1 and p3
    return (
        (p2[0] - p1[0]) * (p3[1] - p1[1]) == (p3[0] - p1[0]) * (p2[1] - p1[1])
        and min(p1[0], p3[0]) <= p2[0] <= max(p1[0], p3[0])
        and min(p1[1], p3[1]) <= p2[1] <= max(p1[1], p3[1])
    )


def dist_sq(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    """Calculate the squared distance between two points."""
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


def part1(data: str) -> int:
    """
    Solution for part 1
    """
    antennas = get_antennas(data)
    width = len(data.splitlines()[0])
    height = len(data.splitlines())
    antinodes = set()

    for freq, locations in antennas.items():
        for i in range(len(locations)):
            for j in range(i + 1, len(locations)):
                x1, y1 = locations[i]
                x2, y2 = locations[j]

                # Calculate antinode positions
                antinode1 = (2 * x1 - x2, 2 * y1 - y2)
                antinode2 = (2 * x2 - x1, 2 * y2 - y1)

                # Check if antinode is within bounds and not already counted
                if 0 <= antinode1[0] < width and 0 <= antinode1[1] < height:
                    antinodes.add(antinode1)
                if 0 <= antinode2[0] < width and 0 <= antinode2[1] < height:
                    antinodes.add(antinode2)

    return len(antinodes)


def part2(data: str) -> int:
    """
    Solution for part 2
    """
    antennas = get_antennas(data)
    width = len(data.splitlines()[0])
    height = len(data.splitlines())
    antinodes = set()

    for freq, locations in antennas.items():
        if len(locations) < 2:
            continue

        for i in range(len(locations)):
            for j in range(i + 1, len(locations)):
                x1, y1 = locations[i]
                x2, y2 = locations[j]

                dx = x2 - x1
                dy = y2 - y1
                g = gcd(abs(dx), abs(dy))
                dx //= g
                dy //= g

                # Iterate along the line to find antinodes
                for k in range(-100, 101):
                    if k == 0:
                        continue
                    new_x = x1 + k * dx
                    new_y = y1 + k * dy

                    if 0 <= new_x < width and 0 <= new_y < height:
                        antinodes.add((new_x, new_y))

    return len(antinodes)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
