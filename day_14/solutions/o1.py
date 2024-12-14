import re


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_data(data: str):
    # Lines like: p=0,4 v=3,-3
    # Use regex to extract integers
    pattern = re.compile(r"p=(-?\d+),(-?\d+)\s+v=(-?\d+),(-?\d+)")
    robots = []
    for line in data.strip().split("\n"):
        m = pattern.match(line.strip())
        if not m:
            continue
        x, y, vx, vy = map(int, m.groups())
        robots.append((x, y, vx, vy))
    return robots


def simulate(robots, width, height, seconds):
    # Simulate given number of seconds with wrapping
    # positions and velocities are integers
    # After each second: x = (x + vx) mod width, y = (y + vy) mod height
    new_positions = []
    for x, y, vx, vy in robots:
        nx = (x + vx * seconds) % width
        ny = (y + vy * seconds) % height
        new_positions.append((nx, ny))
    return new_positions


def part1(data: str) -> int:
    """
    After 100 seconds, count the robots in each quadrant.
    Width=101, Height=103
    Quadrants defined by the center lines:
    - Horizontal center line: x = 50 (0-based indexing from 0..100)
    - Vertical center line: y = 51 (0-based indexing from 0..102)
    Robots exactly on these lines don't count in any quadrant.
    Quadrant numbering for reference:
    Q2 | Q1
    --+--
    Q3 | Q4
    """
    width = 101
    height = 103
    robots = parse_data(data)
    positions_100 = simulate(robots, width, height, 100)

    q1 = q2 = q3 = q4 = 0
    for x, y in positions_100:
        if x == 50 or y == 51:
            continue
        # x>50 means right half, x<50 means left half
        # y<51 means upper half, y>51 means lower half
        if x > 50 and y < 51:
            q1 += 1
        elif x < 50 and y < 51:
            q2 += 1
        elif x < 50 and y > 51:
            q3 += 1
        elif x > 50 and y > 51:
            q4 += 1

    safety_factor = q1 * q2 * q3 * q4
    return safety_factor


def part2(data: str) -> int:
    """
    We suspect that at some second, the robots form a special Easter egg pattern (e.g. a Christmas tree).
    Without the actual target pattern given, we need a strategy:
    - We'll guess that the puzzle (as hinted) is related to observing a recognizable pattern at some time.
    - Typically, such puzzles might require checking consecutive time steps until the arrangement spells out something visually recognizable.
    - We'll simulate until a certain stable pattern emerges or until a small bounding box of points forms.

    A heuristic approach:
    1. Simulate the robots over time.
    2. For each second, compute the bounding box of all robot positions.
    3. The moment the bounding box is minimal (or below a certain area threshold), it's likely the "tree" pattern is formed.
    4. Return that time.

    This is a common approach for similar puzzles (like Advent of Code 2018 day 10).
    We'll implement that heuristic: keep simulating until bounding box starts growing again,
    then the minimal area configuration is the Easter egg.

    Note: The puzzle states "very rarely, ... arrange themselves into a picture." We'll assume minimal bounding box method.

    We'll brute force from t=0 upwards until we see bounding box start growing again.
    """
    width = 101
    height = 103
    robots = parse_data(data)

    # Function to get bounding box area
    def bounding_box_area(positions):
        xs = [x for x, y in positions]
        ys = [y for x, y in positions]
        return (max(xs) - min(xs) + 1) * (max(ys) - min(ys) + 1)

    t = 0
    best_t = 0
    prev_area = None
    smallest_area = None
    increasing_count = 0

    while True:
        positions = simulate(robots, width, height, t)
        area = bounding_box_area(positions)
        if smallest_area is None or area < smallest_area:
            smallest_area = area
            best_t = t
            increasing_count = 0
        else:
            # If area not improved, increment counter
            # If this happens several times in a row, we assume we've passed the pattern
            increasing_count += 1
            if increasing_count > 50:
                # Stop after no improvement for a while
                break
        t += 1
        if t > 10000:
            # Safety stop if no pattern emerges
            break

    # best_t is the second at which pattern is minimal (likely the Easter egg)
    return best_t


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
