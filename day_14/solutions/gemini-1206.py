import re
from collections import defaultdict


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_robots(data: str):
    robots = []
    for line in data.splitlines():
        match = re.match(r"p=(\d+),(\d+) v=(\-?\d+),(\-?\d+)", line)
        if match:
            px, py, vx, vy = map(int, match.groups())
            robots.append(((px, py), (vx, vy)))
    return robots


def simulate_robots(robots, width, height, time):
    grid = defaultdict(int)
    for (px, py), (vx, vy) in robots:
        new_x = (px + vx * time) % width
        new_y = (py + vy * time) % height
        grid[(new_x, new_y)] += 1
    return grid


def calculate_safety_factor(grid, width, height):
    q1, q2, q3, q4 = 0, 0, 0, 0
    mid_x = width // 2
    mid_y = height // 2
    for (x, y), count in grid.items():
        if x < mid_x and y < mid_y:
            q1 += count
        elif x > mid_x and y < mid_y:
            q2 += count
        elif x < mid_x and y > mid_y:
            q3 += count
        elif x > mid_x and y > mid_y:
            q4 += count
    return q1 * q2 * q3 * q4


def part1(data: str) -> int:
    """
    Solution for part 1
    """
    robots = parse_robots(data)
    width = 101
    height = 103
    time = 100
    grid = simulate_robots(robots, width, height, time)
    return calculate_safety_factor(grid, width, height)


def is_christmas_tree(grid, width, height):
    """
    Checks if the robot configuration vaguely resembles a Christmas tree.
    This is a very loose approximation based on the idea of a central trunk
    and branches spreading out, with more robots towards the center and bottom.
    """
    total_robots = sum(grid.values())
    if total_robots < 10:
        return False

    mid_x = width // 2
    mid_y = height // 2
    trunk_count = 0
    branch_count = 0
    bottom_count = 0

    for (x, y), count in grid.items():
        if abs(x - mid_x) <= 1 and y > mid_y:
            trunk_count += count
        if abs(x - mid_x) <= height - y and y <= mid_y:
            branch_count += count

        if y > mid_y:
            bottom_count += count

    return (
        trunk_count > total_robots * 0.1
        and branch_count > total_robots * 0.2
        and bottom_count > total_robots * 0.4
    )


def part2(data: str) -> int:
    """
    Solution for part 2
    """
    robots = parse_robots(data)
    width = 101
    height = 103
    for time in range(1, 10000):
        grid = simulate_robots(robots, width, height, time)
        if is_christmas_tree(grid, width, height):
            return time
    return -1


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
