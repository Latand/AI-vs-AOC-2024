import re
from dataclasses import dataclass
from typing import List, Dict, Tuple
from collections import defaultdict


@dataclass
class Robot:
    x: int
    y: int
    vx: int
    vy: int

    def move(self, width: int, height: int) -> None:
        self.x = (self.x + self.vx) % width
        self.y = (self.y + self.vy) % height


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_robots(data: str) -> List[Robot]:
    pattern = r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)"
    robots = []

    for line in data.splitlines():
        if match := re.match(pattern, line):
            x, y, vx, vy = map(int, match.groups())
            robots.append(Robot(x, y, vx, vy))

    return robots


def get_robot_positions(robots: List[Robot]) -> Dict[Tuple[int, int], int]:
    positions = defaultdict(int)
    for robot in robots:
        positions[(robot.x, robot.y)] += 1
    return positions


def calculate_quadrant_safety(
    positions: Dict[Tuple[int, int], int], width: int, height: int
) -> int:
    quadrants = [0] * 4
    mid_w = width // 2
    mid_h = height // 2

    for (x, y), count in positions.items():
        # Skip robots on the middle lines
        if x == mid_w or y == mid_h:
            continue

        quad_idx = (1 if x > mid_w else 0) + (2 if y > mid_h else 0)
        quadrants[quad_idx] += count

    return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]


def check_christmas_tree(
    positions: Dict[Tuple[int, int], int], width: int, height: int
) -> bool:
    # Define a simple Christmas tree pattern
    # This is a basic example - you might want to adjust based on the actual pattern
    tree_pattern = {
        (width // 2, height // 4),  # Top
        (width // 2 - 1, height // 4 + 1),
        (width // 2, height // 4 + 1),
        (width // 2 + 1, height // 4 + 1),  # Middle
        (width // 2 - 2, height // 4 + 2),
        (width // 2 - 1, height // 4 + 2),
        (width // 2, height // 4 + 2),
        (width // 2 + 1, height // 4 + 2),
        (width // 2 + 2, height // 4 + 2),  # Bottom
        (width // 2, height // 4 + 3),  # Trunk
    }

    robot_positions = set(positions.keys())
    return all(pos in robot_positions for pos in tree_pattern)


def part1(data: str) -> int:
    """
    Simulate robot movement for 100 seconds and calculate safety factor
    """
    WIDTH, HEIGHT = 101, 103
    robots = parse_robots(data)

    # Simulate for 100 seconds
    for _ in range(100):
        for robot in robots:
            robot.move(WIDTH, HEIGHT)

    positions = get_robot_positions(robots)
    return calculate_quadrant_safety(positions, WIDTH, HEIGHT)


def part2(data: str) -> int:
    """
    Find the first time when robots form a Christmas tree pattern
    """
    WIDTH, HEIGHT = 101, 103
    robots = parse_robots(data)

    # We'll check for a reasonable amount of time
    for second in range(10000):  # Adjust this limit as needed
        positions = get_robot_positions(robots)

        if check_christmas_tree(positions, WIDTH, HEIGHT):
            return second

        for robot in robots:
            robot.move(WIDTH, HEIGHT)

    return -1  # If no pattern is found


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
