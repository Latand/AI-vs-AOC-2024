import re


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def part1(data: str) -> int:
    """
    Solution for part 1
    """
    # Parse the input using regex
    robot_pattern = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")
    robots = []
    for line in data.splitlines():
        match = robot_pattern.match(line)
        if match:
            px, py, vx, vy = map(int, match.groups())
            robots.append({"x": px, "y": py, "vx": vx, "vy": vy})

    # Define space dimensions
    width, height = 101, 103

    # Simulate 100 seconds
    for _ in range(100):
        for robot in robots:
            robot["x"] = (robot["x"] + robot["vx"]) % width
            robot["y"] = (robot["y"] + robot["vy"]) % height

    # Define quadrants
    mid_x, mid_y = width // 2, height // 2
    quadrants = {"Q1": 0, "Q2": 0, "Q3": 0, "Q4": 0}

    for robot in robots:
        x, y = robot["x"], robot["y"]
        if x < mid_x and y < mid_y:
            quadrants["Q1"] += 1
        elif x > mid_x and y < mid_y:
            quadrants["Q2"] += 1
        elif x < mid_x and y > mid_y:
            quadrants["Q3"] += 1
        elif x > mid_x and y > mid_y:
            quadrants["Q4"] += 1
        # Robots on the mid lines are not counted

    safety_factor = (
        quadrants["Q1"] * quadrants["Q2"] * quadrants["Q3"] * quadrants["Q4"]
    )
    return safety_factor


def part2(data: str) -> int:
    """
    Solution for part 2
    """
    # Parse the input using regex
    robot_pattern = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")
    robots = []
    for line in data.splitlines():
        match = robot_pattern.match(line)
        if match:
            px, py, vx, vy = map(int, match.groups())
            robots.append({"x": px, "y": py, "vx": vx, "vy": vy})

    # Define space dimensions
    width, height = 101, 103

    # Function to check for Christmas tree pattern
    def is_christmas_tree(robots, width, height):
        grid = [["." for _ in range(width)] for _ in range(height)]
        for robot in robots:
            grid[robot["y"]][robot["x"]] = "#"

        # Simple pattern check (this can be enhanced)
        tree_pattern = ["....#....", "...###...", "..#####..", "...###...", "....#...."]
        pattern_height = len(tree_pattern)
        pattern_width = len(tree_pattern[0])

        for y in range(height - pattern_height + 1):
            for x in range(width - pattern_width + 1):
                match = True
                for dy in range(pattern_height):
                    for dx in range(pattern_width):
                        if tree_pattern[dy][dx] == "#" and grid[y + dy][x + dx] != "#":
                            match = False
                            break
                    if not match:
                        break
                if match:
                    return True
        return False

    seconds = 0
    while True:
        # Move robots
        for robot in robots:
            robot["x"] = (robot["x"] + robot["vx"]) % width
            robot["y"] = (robot["y"] + robot["vy"]) % height
        seconds += 1

        # Check for Christmas tree
        if is_christmas_tree(robots, width, height):
            return seconds


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
