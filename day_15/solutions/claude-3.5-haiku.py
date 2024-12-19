def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_map(data_lines):
    """Parse the initial warehouse map."""
    grid = []
    robot_pos = None
    boxes = []

    for y, line in enumerate(data_lines):
        row = list(line)
        grid.append(row)
        for x, char in enumerate(row):
            if char == "@":
                robot_pos = (x, y)
            elif char == "O":
                boxes.append((x, y))

    return grid, robot_pos, boxes


def is_valid_move(grid, pos):
    """Check if the position is within the grid and not a wall."""
    x, y = pos
    return 0 <= y < len(grid) and 0 <= x < len(grid[y]) and grid[y][x] != "#"


def try_move(grid, robot_pos, boxes, direction):
    """
    Attempt to move the robot and push boxes.
    Returns new robot position, new boxes positions, and whether move was successful.
    """
    # Directional move offsets: left, right, up, down
    moves = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}
    dx, dy = moves[direction]
    new_robot_x, new_robot_y = robot_pos[0] + dx, robot_pos[1] + dy

    # Check if robot can move to the new position
    if not is_valid_move(grid, (new_robot_x, new_robot_y)):
        return robot_pos, boxes, False

    # Check if the new position has a box
    box_at_new_pos = (new_robot_x, new_robot_y) in boxes

    if box_at_new_pos:
        # Try to push the box
        pushed_box_x, pushed_box_y = new_robot_x + dx, new_robot_y + dy

        # Check if pushing the box is valid
        if (
            not is_valid_move(grid, (pushed_box_x, pushed_box_y))
            or (pushed_box_x, pushed_box_y) in boxes
        ):
            return robot_pos, boxes, False

        # Remove old box position and add new box position
        boxes.remove((new_robot_x, new_robot_y))
        boxes.append((pushed_box_x, pushed_box_y))

    return (new_robot_x, new_robot_y), boxes, True


def solve_warehouse(data, part2=False):
    """Solve warehouse robot movement puzzle."""
    data_lines = data.splitlines()

    # Use modified parsing for part 2
    if part2:
        # Resize the map
        resized_lines = []
        for line in data_lines:
            new_line = "".join(
                [
                    "##"
                    if c == "#"
                    else "[]"
                    if c == "O"
                    else ".."
                    if c == "."
                    else "@."
                    if c == "@"
                    else c * 2
                    for c in line
                ]
            )
            resized_lines.append(new_line)
        data_lines = resized_lines

    grid, robot_pos, boxes = parse_map(data_lines)
    moves = "".join(data_lines[0].split("\n")[1:])

    for move in moves:
        robot_pos, boxes, success = try_move(grid, robot_pos, boxes, move)

    # Calculate GPS coordinates
    return sum(100 * (y + 1) + (x + 1) for x, y in boxes)


def part1(data: str) -> int:
    """Solution for part 1."""
    return solve_warehouse(data)


def part2(data: str) -> int:
    """Solution for part 2 with resized warehouse."""
    return solve_warehouse(data, part2=True)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
