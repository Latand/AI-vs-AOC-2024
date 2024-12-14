import re
from collections import defaultdict


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_input(data):
    pattern = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")
    robots = []
    for line in data.splitlines():
        match = pattern.match(line)
        if match:
            px, py, vx, vy = map(int, match.groups())
            robots.append(((px, py), (vx, vy)))
    return robots


def move_robots(robots, time, width, height):
    positions = []
    for (px, py), (vx, vy) in robots:
        new_x = (px + vx * time) % width
        new_y = (py + vy * time) % height
        positions.append((new_x, new_y))
    return positions


def count_quadrants(positions, width, height):
    mid_x, mid_y = width // 2, height // 2
    quadrants = [0, 0, 0, 0]  # Top-left, Top-right, Bottom-left, Bottom-right

    for x, y in positions:
        if x == mid_x or y == mid_y:
            continue
        if x < mid_x and y < mid_y:
            quadrants[0] += 1
        elif x >= mid_x and y < mid_y:
            quadrants[1] += 1
        elif x < mid_x and y >= mid_y:
            quadrants[2] += 1
        elif x >= mid_x and y >= mid_y:
            quadrants[3] += 1

    return quadrants


def find_easter_egg(robots, width, height):
    time = 0
    while True:
        positions = move_robots(robots, time, width, height)
        min_x = min(x for x, y in positions)
        max_x = max(x for x, y in positions)
        min_y = min(y for x, y in positions)
        max_y = max(y for x, y in positions)

        # Check if robots form a small, dense area
        if max_x - min_x < 20 and max_y - min_y < 20:
            grid = defaultdict(lambda: ".")
            for x, y in positions:
                grid[(x, y)] = "#"

            # Print the grid
            print(f"Time: {time}")
            for y in range(min_y, max_y + 1):
                print("".join(grid[(x, y)] for x in range(min_x, max_x + 1)))
            return time

        time += 1


def part1(data):
    robots = parse_input(data)
    positions = move_robots(robots, 100, 101, 103)
    quadrants = count_quadrants(positions, 101, 103)
    return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]


def part2(data):
    robots = parse_input(data)
    return find_easter_egg(robots, 101, 103)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
