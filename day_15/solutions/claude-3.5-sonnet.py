from typing import List, Tuple, Set


def parse_input(data: str) -> Tuple[List[List[str]], str]:
    """Parse input into grid and moves."""
    parts = data.split("\n\n")
    grid = [list(line) for line in parts[0].splitlines()]
    moves = "".join(parts[1].split())  # Remove newlines from moves
    return grid, moves


def find_robot(grid: List[List[str]]) -> Tuple[int, int]:
    """Find the robot's position in the grid."""
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == "@":
                return y, x
    raise ValueError("Robot not found in grid")


def find_boxes(grid: List[List[str]]) -> Set[Tuple[int, int]]:
    """Find all box positions in the grid."""
    boxes = set()
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == "O" or cell == "[" or cell == "]":  # Handle both parts
                boxes.add((y, x))
    return boxes


def move_direction(direction: str) -> Tuple[int, int]:
    """Convert direction character to movement delta."""
    return {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}[direction]


def calculate_gps(
    boxes: Set[Tuple[int, int]], grid: List[List[str]], part2: bool = False
) -> int:
    """Calculate GPS coordinates sum for all boxes."""
    total = 0
    for y, x in boxes:
        if part2:
            # For part 2, only count positions where '[' appears
            if grid[y][x] == "[":
                total += 100 * y + x
        else:
            total += 100 * y + x
    return total


def is_valid_move(grid: List[List[str]], y: int, x: int) -> bool:
    """Check if a position is valid (not a wall)."""
    if not (0 <= y < len(grid) and 0 <= x < len(grid[0])):
        return False
    return grid[y][x] != "#"


def part1(data: str) -> int:
    """Solution for part 1"""
    grid, moves = parse_input(data)
    robot_pos = find_robot(grid)
    boxes = find_boxes(grid)

    for move in moves:
        dy, dx = move_direction(move)
        new_y, new_x = robot_pos[0] + dy, robot_pos[1] + dx

        if not is_valid_move(grid, new_y, new_x):
            continue

        if (new_y, new_x) in boxes:
            # Try to push box
            box_new_y, box_new_x = new_y + dy, new_x + dx
            if (
                not is_valid_move(grid, box_new_y, box_new_x)
                or (box_new_y, box_new_x) in boxes
            ):
                continue
            # Move box
            boxes.remove((new_y, new_x))
            boxes.add((box_new_y, box_new_x))

        # Move robot
        grid[robot_pos[0]][robot_pos[1]] = "."
        grid[new_y][new_x] = "@"
        robot_pos = (new_y, new_x)

    return calculate_gps(boxes, grid)


def expand_grid(grid: List[List[str]]) -> List[List[str]]:
    """Expand the grid for part 2."""
    new_grid = []
    for row in grid:
        new_row = []
        for cell in row:
            if cell == "#":
                new_row.extend(["#", "#"])
            elif cell == "O":
                new_row.extend(["[", "]"])
            elif cell == ".":
                new_row.extend([".", "."])
            elif cell == "@":
                new_row.extend(["@", "."])
        new_grid.append(new_row)
    return new_grid


def part2(data: str) -> int:
    """Solution for part 2"""
    grid, moves = parse_input(data)
    # Expand the grid
    grid = expand_grid(grid)
    robot_pos = find_robot(grid)
    boxes = set()

    # Find box positions (now represented as '[]' pairs)
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == "[":
                boxes.add((y, x))

    for move in moves:
        dy, dx = move_direction(move)
        new_y, new_x = robot_pos[0] + dy, robot_pos[1] + dx

        if not is_valid_move(grid, new_y, new_x):
            continue

        if (new_y, new_x) in boxes or grid[new_y][new_x] == "]":
            # Try to push box
            box_new_y, box_new_x = new_y + dy, new_x + dx
            if (
                not is_valid_move(grid, box_new_y, box_new_x)
                or (box_new_y, box_new_x) in boxes
            ):
                continue
            # Move box (handle both [ and ] characters)
            if (new_y, new_x) in boxes:
                boxes.remove((new_y, new_x))
                boxes.add((box_new_y, box_new_x))
                grid[new_y][new_x] = "."
                grid[new_y][new_x + 1] = "."
                grid[box_new_y][box_new_x] = "["
                grid[box_new_y][box_new_x + 1] = "]"

        # Move robot
        grid[robot_pos[0]][robot_pos[1]] = "."
        grid[new_y][new_x] = "@"
        robot_pos = (new_y, new_x)

    return calculate_gps(boxes, grid, True)


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
