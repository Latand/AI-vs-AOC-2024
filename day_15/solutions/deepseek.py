def read_input():
    with open("../input.txt") as f:
        lines = f.readlines()
    return lines


def parse_map_and_moves(lines):
    # Find the start and end of the map
    start_map = -1
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "#" * len(stripped):
            if start_map == -1:
                start_map = i
            else:
                end_map = i
                break
    else:
        end_map = len(lines) - 1

    map_lines = lines[start_map : end_map + 1]
    moves = "".join(lines[end_map + 1 :]).strip().replace("\n", "")
    return map_lines, moves


def part1(data):
    lines = data
    map_lines, moves = parse_map_and_moves(lines)

    # Extract the inner map without the top and bottom walls
    grid = [line.strip() for line in map_lines[1:-1]]

    # Find the robot's initial position
    robot_pos = None
    for row_idx, row in enumerate(grid):
        if "@" in row:
            col_idx = row.index("@")
            robot_pos = (row_idx, col_idx)
            break

    # Find all boxes
    boxes = []
    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            if cell == "O":
                boxes.append((row_idx, col_idx))

    # Define movement directions
    move_dir = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}

    # Simulate movements
    for move in moves:
        if move not in move_dir:
            continue  # invalid move, skip
        dr, dc = move_dir[move]
        new_r, new_c = robot_pos[0] + dr, robot_pos[1] + dc
        if new_r < 0 or new_r >= len(grid) or grid[new_r][new_c] == "#":
            continue  # can't move into wall
        if grid[new_r][new_c] == "O":
            # Attempt to push the box
            box_r, box_c = new_r + dr, new_c + dc
            if (
                box_r < 0
                or box_r >= len(grid)
                or box_c < 0
                or box_c >= len(grid[0])
                or grid[box_r][box_c] != "."
            ):
                continue  # can't push into non-empty cell
            # Move the box
            boxes.remove((new_r, new_c))
            boxes.append((box_r, box_c))
            # Move the robot
            robot_pos = (new_r, new_c)
        elif grid[new_r][new_c] == ".":
            # Move the robot
            robot_pos = (new_r, new_c)

    # Calculate GPS coordinates
    sum_gps = 0
    for box in boxes:
        row, col = box
        sum_gps += 100 * row + col
    return sum_gps


def scale_map(map_lines):
    scaled_map = []
    for line in map_lines:
        scaled_line = []
        for char in line.strip():
            if char == "#":
                scaled_line.append("##")
            elif char == "O":
                scaled_line.append("[]")
            elif char == ".":
                scaled_line.append("..")
            elif char == "@":
                scaled_line.append("@.")
            else:
                scaled_line.append(char)
        scaled_map.append("".join(scaled_line))
    return scaled_map


def part2(data):
    lines = data
    map_lines, moves = parse_map_and_moves(lines)

    # Scale up the map
    scaled_map = scale_map(map_lines)

    # Extract the inner map without the top and bottom walls
    grid = [line for line in scaled_map[1:-1]]

    # Find the robot's initial position
    robot_pos = None
    for row_idx, row in enumerate(grid):
        if "@." in row:
            col_idx = row.index("@.")
            robot_pos = (row_idx, col_idx)
            break

    # Find all boxes
    boxes = []
    for row_idx, row in enumerate(grid):
        start = 0
        while start < len(row):
            idx = row.find("[]", start)
            if idx == -1:
                break
            boxes.append((row_idx, idx))
            start = idx + 2  # Each box is two characters

    # Define movement directions
    move_dir = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}

    # Simulate movements
    for move in moves:
        if move not in move_dir:
            continue  # invalid move, skip
        dr, dc = move_dir[move]
        new_r, new_c = robot_pos[0] + dr, robot_pos[1] + dc
        if (
            new_r < 0
            or new_r >= len(grid)
            or (new_c < 0 or new_c >= len(grid[0]) or grid[new_r][new_c] in ["#", "[]"])
        ):
            continue  # can't move into wall or box
        if grid[new_r][new_c] == "[]":
            # Attempt to push the box
            box_r, box_c = new_r + dr, new_c + dc
            if (
                box_c < 0
                or box_c + 1 >= len(grid[0])
                or grid[box_r][box_c : box_c + 2] != ".."
            ):
                continue  # can't push into non-empty cell
            # Move the box
            boxes.remove((new_r, new_c))
            boxes.append((box_r, box_c))
            # Move the robot
            robot_pos = (new_r, new_c)
        elif grid[new_r][new_c] == ".":
            # Move the robot
            robot_pos = (new_r, new_c)

    # Calculate GPS coordinates
    sum_gps = 0
    for box in boxes:
        row, col = box
        sum_gps += 100 * row + col
    return sum_gps


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
