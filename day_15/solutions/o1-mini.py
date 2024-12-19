def read_input() -> str:
    with open("../input.txt") as f:
        return f.read().strip()


def part1(data: str) -> int:
    """
    Predict the motion of the robot and boxes in the warehouse.
    After the robot is finished moving, calculate the sum of all boxes' GPS coordinates.
    """
    warehouse, moves = parse_input(data)
    robot_pos = find_robot(warehouse)
    boxes = find_boxes(warehouse)

    for move in moves:
        robot_pos, boxes = execute_move(robot_pos, boxes, move, warehouse)

    return calculate_gps_sum(boxes)


def part2(data: str) -> int:
    """
    Predict the motion of the robot and boxes in the scaled-up warehouse.
    After the robot is finished moving, calculate the sum of all boxes' final GPS coordinates.
    """
    warehouse, moves = parse_input(data, scale_up=True)
    robot_pos = find_robot(warehouse)
    boxes = find_boxes(warehouse)

    for move in moves:
        robot_pos, boxes = execute_move(robot_pos, boxes, move, warehouse, scaled=True)

    return calculate_gps_sum(boxes, scaled=True)


def parse_input(data: str, scale_up: bool = False):
    lines = data.splitlines()
    warehouse = []
    moves = []
    parsing_map = True
    move_chars = {"^", "v", "<", ">"}

    for line in lines:
        if parsing_map:
            if set(line).issubset(move_chars):
                parsing_map = False
            else:
                warehouse.append(line)
                continue
        if not parsing_map:
            moves.extend([char for char in line if char in move_chars])

    if scale_up:
        warehouse = scale_warehouse(warehouse)

    return warehouse, moves


def scale_warehouse(warehouse: list[str]) -> list[str]:
    scaled = []
    for line in warehouse:
        scaled_line = ""
        for char in line:
            if char == "#":
                scaled_line += "##"
            elif char == "O":
                scaled_line += "[]"
            elif char == ".":
                scaled_line += ".."
            elif char == "@":
                scaled_line += "@."
            else:
                scaled_line += char
        scaled.append(scaled_line)
    return scaled


def find_robot(warehouse: list[str]) -> tuple[int, int]:
    for y, line in enumerate(warehouse):
        x = line.find("@")
        if x != -1:
            return (y, x)
    raise ValueError("Robot not found in the warehouse map.")


def find_boxes(warehouse: list[str]) -> set:
    boxes = set()
    for y, line in enumerate(warehouse):
        for x, char in enumerate(line):
            if char == "O" or char == "[":
                boxes.add((y, x))
    return boxes


def execute_move(
    robot_pos: tuple[int, int],
    boxes: set,
    move: str,
    warehouse: list[str],
    scaled: bool = False,
) -> tuple:
    direction = move
    dy, dx = 0, 0
    if direction == "^":
        dy, dx = -1, 0
    elif direction == "v":
        dy, dx = 1, 0
    elif direction == "<":
        dy, dx = 0, -1
    elif direction == ">":
        dy, dx = 0, 1

    new_robot_pos = (robot_pos[0] + dy, robot_pos[1] + dx)

    if new_robot_pos in boxes:
        # Attempt to push the box
        new_box_pos = (new_robot_pos[0] + dy, new_robot_pos[1] + dx)
        if is_move_valid(new_box_pos, warehouse, boxes, scaled):
            boxes.remove(new_robot_pos)
            boxes.add(new_box_pos)
            return new_robot_pos, boxes
        else:
            # Movement blocked
            return robot_pos, boxes
    else:
        if is_move_valid(new_robot_pos, warehouse, boxes, scaled):
            return new_robot_pos, boxes
        else:
            return robot_pos, boxes


def is_move_valid(
    pos: tuple[int, int], warehouse: list[str], boxes: set, scaled: bool
) -> bool:
    y, x = pos
    if y < 0 or y >= len(warehouse) or x < 0 or x >= len(warehouse[0]):
        return False
    if warehouse[y][x] == "#":
        return False
    if pos in boxes:
        return False
    return True


def calculate_gps_sum(boxes: set, scaled: bool = False) -> int:
    total = 0
    for y, x in boxes:
        if scaled and isinstance(x, int):
            # For scaled up, distance is to the closest edge of the box
            gps = 100 * y + (x // 2)
        else:
            gps = 100 * y + x
        total += gps
    return total


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
