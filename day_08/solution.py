from collections import defaultdict
from typing import Tuple, Set


def read_input():
    with open("input.txt") as f:
        return f.read().strip()


def gcd(a: int, b: int) -> int:
    """Compute the greatest common divisor of a and b."""
    while b:
        a, b = b, a % b
    return abs(a)


def canonical_line(p1: Tuple[int, int], p2: Tuple[int, int]) -> Tuple[int, int, int]:
    """
    Return the canonical representation of the line passing through points p1 and p2.
    The line is represented as (A, B, C) where A*x + B*y + C = 0,
    and A, B, C are normalized such that gcd(A, B, C) = 1 and A >= 0.
    """
    (x1, y1) = p1
    (x2, y2) = p2
    A = y2 - y1
    B = x1 - x2
    C = x2 * y1 - x1 * y2

    # Normalize the coefficients
    g = gcd(gcd(A, B), C)
    if g != 0:
        A //= g
        B //= g
        C //= g

    # Ensure A is non-negative for a unique representation
    if A < 0 or (A == 0 and B < 0):
        A *= -1
        B *= -1
        C *= -1

    return (A, B, C)


def get_points_on_line(
    A: int, B: int, C: int, width: int, height: int
) -> Set[Tuple[int, int]]:
    """
    Given a line in canonical form Ax + By + C = 0, return all grid positions
    that lie on this line within the grid boundaries.
    """
    points = set()

    if B != 0:
        for x in range(width):
            y = (-A * x - C) / B
            if y.is_integer():
                y_int = int(y)
                if 0 <= y_int < height:
                    points.add((x, y_int))

    if A != 0:
        for y in range(height):
            x = (-B * y - C) / A
            if x.is_integer():
                x_int = int(x)
                if 0 <= x_int < width:
                    points.add((x_int, y))

    return points


def part1(data: str) -> int:
    """Solve part 1 of the puzzle."""
    grid = data.split("\n")
    height = len(grid)
    width = max(len(row) for row in grid)

    freq_map = defaultdict(list)

    # Collect antenna positions grouped by their frequency
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c != ".":
                freq_map[c].append((x, y))

    antinodes = set()

    # For each frequency, compute antinodes based on antenna pairs
    for freq, antennas in freq_map.items():
        n = len(antennas)
        if n < 2:
            continue  # Need at least two antennas to form antinodes
        for i in range(n):
            for j in range(i + 1, n):
                A = antennas[i]
                B = antennas[j]

                # Calculate Antinode C: 2 * B - A
                Cx = 2 * B[0] - A[0]
                Cy = 2 * B[1] - A[1]

                # Calculate Antinode D: 2 * A - B
                Dx = 2 * A[0] - B[0]
                Dy = 2 * A[1] - B[1]

                # Check if Antinode C is within bounds
                if 0 <= Cx < width and 0 <= Cy < height:
                    antinodes.add((Cx, Cy))

                # Check if Antinode D is within bounds
                if 0 <= Dx < width and 0 <= Dy < height:
                    antinodes.add((Dx, Dy))

    return len(antinodes)


def part2(data: str) -> int:
    """Solve part 2 of the puzzle."""
    grid = data.split("\n")
    height = len(grid)
    width = max(len(row) for row in grid)

    freq_map = defaultdict(list)

    # Collect antenna positions grouped by their frequency
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c != ".":
                freq_map[c].append((x, y))

    antinodes = set()

    # Process each frequency separately
    for freq, antennas in freq_map.items():
        n = len(antennas)
        if n < 2:
            continue  # Only frequencies with two or more antennas create antinodes

        lines_seen = set()

        # Iterate over all unique pairs to determine lines
        for i in range(n):
            for j in range(i + 1, n):
                p1 = antennas[i]
                p2 = antennas[j]
                line = canonical_line(p1, p2)
                if line not in lines_seen:
                    lines_seen.add(line)
                    A, B, C = line
                    points_on_line = get_points_on_line(A, B, C, width, height)
                    antinodes.update(points_on_line)

    return len(antinodes)


if __name__ == "__main__":
    data = read_input()

    print("Part 1:", part1(data))
    print("Part 2:", part2(data))
