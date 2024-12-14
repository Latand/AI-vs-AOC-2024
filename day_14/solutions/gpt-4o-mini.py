import re


# Function to parse the input using regex
def parse_input(data: str):
    pattern = r"p=([-\d]+),([-\d]+) v=([-\d]+),([-\d]+)"
    robots = []
    for line in data.splitlines():
        match = re.match(pattern, line)
        if match:
            x, y, vx, vy = map(int, match.groups())
            robots.append({"position": (x, y), "velocity": (vx, vy)})
    return robots


# Function to simulate the robots' movement for a given number of seconds
def simulate_robots(robots, seconds):
    for _ in range(seconds):
        for robot in robots:
            px, py = robot["position"]
            vx, vy = robot["velocity"]
            new_x = (px + vx) % 101  # Wrap around horizontally
            new_y = (py + vy) % 103  # Wrap around vertically
            robot["position"] = (new_x, new_y)
    return robots


# Function for Part 1: Calculate safety factor after 100 seconds
def part1(robots):
    # Simulate robots' movement for 100 seconds
    robots = simulate_robots(robots, 100)

    # Create a grid to store robot counts at each position
    grid = [[0] * 101 for _ in range(103)]  # Grid of size 101x103

    # Count the robots at each position
    for robot in robots:
        x, y = robot["position"]
        grid[y][x] += 1

    # Count the robots in the quadrants
    top_left = sum(grid[y][x] for y in range(51) for x in range(51))
    top_right = sum(grid[y][x] for y in range(51) for x in range(51, 101))
    bottom_left = sum(grid[y][x] for y in range(51, 103) for x in range(51))
    bottom_right = sum(grid[y][x] for y in range(51, 103) for x in range(51, 101))

    # Multiply the quadrants to get the safety factor
    safety_factor = top_left * top_right * bottom_left * bottom_right
    return safety_factor


# Function for Part 2: Find the earliest time when the robots form the Easter egg (Christmas tree shape)
def part2(robots):
    # Brute-force search for the minimum time when robots form a recognizable shape
    for seconds in range(10000):
        robots = simulate_robots(robots, 1)

        # Check for the Christmas tree shape (you could adapt this check based on the real pattern)
        grid = [["." for _ in range(101)] for _ in range(103)]
        for robot in robots:
            x, y = robot["position"]
            grid[y][x] = "#"

        # Check if the grid matches the shape of a Christmas tree
        # Example: You could look for a triangle or some other specific pattern.
        if is_christmas_tree(grid):
            return seconds

    return -1  # If no tree is found within the time limit


# Placeholder function to check if the grid forms a Christmas tree pattern
def is_christmas_tree(grid):
    # Here, implement a more sophisticated method to detect the Christmas tree pattern.
    # For example, checking the pixel arrangement or using machine learning for pattern recognition.
    return False


# Main function
def main():
    with open("../input.txt") as f:
        data = f.read().strip()

    robots = parse_input(data)

    result1 = part1(robots)
    print(f"Part 1: {result1}")

    result2 = part2(robots)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
