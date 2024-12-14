import re


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_robots(data):
    pattern = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")
    robots = []
    for line in data.splitlines():
        match = pattern.match(line)
        if match:
            x, y, vx, vy = map(int, match.groups())
            robots.append((x, y, vx, vy))
    return robots


def simulate_positions(robots, time, width, height):
    positions = []
    for robot in robots:
        x, y, vx, vy = robot
        x = (x + vx * time) % width
        y = (y + vy * time) % height
        positions.append((x, y))
    return positions


def count_quadrants(positions, width, height):
    mid_x = width // 2
    mid_y = height // 2
    q1 = q2 = q3 = q4 = 0
    for x, y in positions:
        if x < mid_x and y < mid_y:
            q1 += 1
        elif x > mid_x and y < mid_y:
            q2 += 1
        elif x < mid_x and y > mid_y:
            q3 += 1
        elif x > mid_x and y > mid_y:
            q4 += 1
    return q1, q2, q3, q4


def part1(data):
    robots = parse_robots(data)
    width = 101
    height = 103
    positions = simulate_positions(robots, 100, width, height)
    q1, q2, q3, q4 = count_quadrants(positions, width, height)
    safety_factor = q1 * q2 * q3 * q4
    return safety_factor


def bounding_box_area(positions, width, height):
    xs, ys = zip(*positions)
    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)
    return (max_x - min_x) * (max_y - min_y)


def find_min_time(robots, max_time=1000):
    width = 101
    height = 103
    min_area = float("inf")
    best_time = 0
    for time in range(max_time):
        positions = simulate_positions(robots, time, width, height)
        area = bounding_box_area(positions, width, height)
        if area < min_area:
            min_area = area
            best_time = time
    return best_time


def part2(data):
    robots = parse_robots(data)
    return find_min_time(robots)


def main():
    data = read_input()
    result1 = part1(data)
    print(f"Part 1: {result1}")
    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
