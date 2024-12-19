def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_map_and_moves(data: str):
    # Parse the warehouse map and move instructions
    lines = data.splitlines()

    # Separate map lines from moves.
    # The map lines are at the start until we reach a line not consisting of '#' and the warehouse characters.
    # After that, the lines form the moves (possibly broken across multiple lines).

    # Find where the map ends. We'll assume the map is always a rectangle enclosed by '#'.
    map_lines = []
    i = 0
    while i < len(lines) and "#" in lines[i]:
        map_lines.append(lines[i])
        i += 1

    # The remaining lines are moves. Concatenate them into one string, ignoring newlines.
    moves_str = "".join(lines[i:])

    return map_lines, moves_str


def find_robot_and_boxes(warehouse):
    robot = None
    boxes = []
    for r, row in enumerate(warehouse):
        for c, ch in enumerate(row):
            if ch == "@":
                robot = (r, c)
            elif ch == "O":
                boxes.append((r, c))
    return robot, boxes


def can_push(warehouse, boxes_set, start, direction, W, H):
    # Attempt to push boxes starting from 'start' in the given direction.
    # direction is a delta (dr, dc)
    dr, dc = direction
    # We'll find all consecutive boxes in the direction of push.
    chain = []
    r, c = start
    while (r, c) in boxes_set:
        chain.append((r, c))
        r += dr
        c += dc

    # Now 'r,c' is the first empty space or wall after the chain.
    # Check if the position after the last box in the chain is empty.
    # If it is a wall '#' or out of bounds, we cannot push.
    if warehouse[r][c] == "#":
        return False
    return True


def push_boxes(warehouse, boxes_set, start, direction):
    # Actually push boxes in the given direction
    dr, dc = direction
    # Find chain
    chain = []
    r, c = start
    while (r, c) in boxes_set:
        chain.append((r, c))
        r += dr
        c += dc

    # Push from last to first to avoid overwriting positions
    for br, bc in reversed(chain):
        boxes_set.remove((br, bc))
        boxes_set.add((br + dr, bc + dc))


def simulate_part1(warehouse, moves):
    H = len(warehouse)
    W = len(warehouse[0])

    robot, boxes = find_robot_and_boxes(warehouse)
    boxes_set = set(boxes)

    dir_map = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}

    for m in moves:
        dr, dc = dir_map[m]
        nr = robot[0] + dr
        nc = robot[1] + dc

        if warehouse[nr][nc] == "#":
            # Can't move
            continue
        if (nr, nc) in boxes_set:
            # Need to push
            if can_push(warehouse, boxes_set, (nr, nc), (dr, dc), W, H):
                # Push is possible
                push_boxes(warehouse, boxes_set, (nr, nc), (dr, dc))
                # Move robot
                robot = (nr, nc)
            else:
                # Can't push
                continue
        else:
            # Empty space
            robot = (nr, nc)

    # Compute sum of GPS
    # The GPS coordinate: row*100 + col
    result = sum(r * 100 + c for (r, c) in boxes_set)
    return result


def scale_warehouse(warehouse):
    # For part 2, we need to transform the warehouse:
    # '#' -> '##'
    # 'O' -> '[]'
    # '.' -> '..'
    # '@' -> '@.'
    new_warehouse = []
    for row in warehouse:
        new_row = ""
        for ch in row:
            if ch == "#":
                new_row += "##"
            elif ch == "O":
                new_row += "[]"
            elif ch == ".":
                new_row += ".."
            elif ch == "@":
                new_row += "@."
            else:
                new_row += ch * 2  # Fallback if unexpected character
        new_warehouse.append(new_row)
    return new_warehouse


def find_robot_and_boxes_part2(warehouse):
    # Now boxes are represented by '[]' pairs horizontally.
    # Robot is still '@'.
    robot = None
    boxes = []
    H = len(warehouse)
    W = len(warehouse[0])
    # We'll consider a box's position as the top-left bracket of the '[]'.
    for r in range(H):
        c = 0
        while c < W:
            if warehouse[r][c] == "@":
                robot = (r, c)
                c += 1
            elif c + 1 < W and warehouse[r][c : c + 2] == "[]":
                boxes.append((r, c))
                c += 2
            else:
                c += 1
    return robot, boxes


def can_push_part2(warehouse, boxes_set, start, direction, W, H):
    # Similar to part 1, but boxes span two columns horizontally.
    # We'll still store and push them by their top-left coordinate.

    dr, dc = direction
    chain = []
    r, c = start
    while (r, c) in boxes_set:
        chain.append((r, c))
        r += dr
        c += dc

    # Check the space after last box in chain
    # Each box occupies two horizontal cells. We must ensure that both cells after pushing are free.
    # But effectively, checking the top-left cell's next position for a wall or overlap is enough
    # because we know if the top-left is pushing into a wall or another box, it's invalid.

    # The position (r, c) is where we want the next box to be placed. Check if it's valid:
    if warehouse[r][c] == "#":
        return False
    # Also check the next cell horizontally if dc != 0. If pushing horizontally, we must check that
    # the cell to the right of the landing position is also free (not a wall).
    if dc != 0:
        if warehouse[r][c + 1] == "#":
            return False
    return True


def push_boxes_part2(warehouse, boxes_set, start, direction):
    dr, dc = direction
    chain = []
    r, c = start
    while (r, c) in boxes_set:
        chain.append((r, c))
        r += dr
        c += dc

    for br, bc in reversed(chain):
        boxes_set.remove((br, bc))
        boxes_set.add((br + dr, bc + dc))


def simulate_part2(warehouse, moves):
    H = len(warehouse)
    W = len(warehouse[0])

    robot, boxes = find_robot_and_boxes_part2(warehouse)
    boxes_set = set(boxes)

    dir_map = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}

    def is_wall(r, c):
        return warehouse[r][c] == "#"

    for m in moves:
        dr, dc = dir_map[m]
        nr = robot[0] + dr
        nc = robot[1] + dc

        # Check what's at nr,nc
        cell = warehouse[nr][nc]

        # If top-left cell of next position is a wall, can't move
        if cell == "#":
            continue

        # Check if we're pushing a box.
        if (nr, nc) in boxes_set:
            if can_push_part2(warehouse, boxes_set, (nr, nc), (dr, dc), W, H):
                push_boxes_part2(warehouse, boxes_set, (nr, nc), (dr, dc))
                robot = (nr, nc)
            else:
                continue
        else:
            # Just move robot
            robot = (nr, nc)

    # Compute sum of GPS for boxes
    # For part 2, the GPS coordinate is still (row*100+col) using the top-left corner of the box.
    result = sum(r * 100 + c for (r, c) in boxes_set)
    return result


def part1(data: str) -> int:
    map_lines, moves = parse_map_and_moves(data)
    warehouse = map_lines
    return simulate_part1(warehouse, moves)


def part2(data: str) -> int:
    map_lines, moves = parse_map_and_moves(data)
    warehouse = map_lines
    scaled_warehouse = scale_warehouse(warehouse)
    return simulate_part2(scaled_warehouse, moves)


def main():
    data = read_input()
    result1 = part1(data)
    print(f"Part 1: {result1}")
    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
