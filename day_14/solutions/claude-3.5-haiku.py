import re
from typing import List, Tuple
from collections import defaultdict


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_robots(data: str) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """Parse robot positions and velocities using regex"""
    robot_pattern = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")
    return [
        ((int(x), int(y)), (int(vx), int(vy)))
        for x, y, vx, vy in robot_pattern.findall(data)
    ]


def simulate_robots(
    robots: List[Tuple[Tuple[int, int], Tuple[int, int]]],
    width: int,
    height: int,
    seconds: int,
) -> List[Tuple[int, int]]:
    """Simulate robot movements with wrapping"""
    final_positions = []

    for (x, y), (vx, vy) in robots:
        # Calculate final position with wrapping
        final_x = (x + vx * seconds) % width
        final_y = (y + vy * seconds) % height
        final_positions.append((final_x, final_y))

    return final_positions


def part1(data: str) -> int:
    """Calculate safety factor"""
    robots = parse_robots(data)
    width, height = 101, 103
    final_positions = simulate_robots(robots, width, height, 100)

    # Count robots in quadrants
    quadrant_counts = [0, 0, 0, 0]
    for x, y in final_positions:
        if x < width // 2 and y < height // 2:
            quadrant_counts[0] += 1
        elif x > width // 2 and y < height // 2:
            quadrant_counts[1] += 1
        elif x < width // 2 and y > height // 2:
            quadrant_counts[2] += 1
        elif x > width // 2 and y > height // 2:
            quadrant_counts[3] += 1

    # Calculate safety factor
    return (
        quadrant_counts[0]
        * quadrant_counts[1]
        * quadrant_counts[2]
        * quadrant_counts[3]
    )


def part2(data: str) -> int:
    """Find the time when robots form a Christmas tree pattern"""
    robots = parse_robots(data)
    width, height = 101, 103

    def is_christmas_tree(final_positions):
        """Creative check for Christmas tree formation"""
        # Treat positions as a 2D grid
        grid = defaultdict(int)
        for x, y in final_positions:
            grid[(x, y)] += 1

        # Look for a tree-like pattern
        # This is a creative interpretation of a tree formation
        tree_shape = [
            (0, 0),  # trunk bottom
            (0, -1),  # trunk middle
            (0, -2),  # trunk top
            (-1, -3),  # left branch
            (1, -3),  # right branch
            (0, -3),  # top branch
        ]

        # Normalize positions
        min_x = min(x for x, _ in final_positions)
        min_y = min(y for _, y in final_positions)
        normalized = {(x - min_x, y - min_y) for x, y in final_positions}

        # Check if tree pattern exists
        return all(
            (x, y) in normalized
            or sum(grid.get((x + min_x, y + min_y), 0) for x, y in tree_shape) > 5
            for x, y in tree_shape
        )

    # Search for Christmas tree formation
    for seconds in range(1, 100000):  # Reasonable upper bound
        final_positions = simulate_robots(robots, width, height, seconds)
        if is_christmas_tree(final_positions):
            return seconds

    return -1  # No formation found


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1 - Safety Factor: {result1}")

    result2 = part2(data)
    print(f"Part 2 - Seconds to Christmas Tree Formation: {result2}")


if __name__ == "__main__":
    main()
