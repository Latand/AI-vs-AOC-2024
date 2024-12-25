def read_map():
    with open("../input.txt") as f:
        return [line.rstrip("\n") for line in f]


def find_start(map):
    for row_idx, row in enumerate(map):
        if "^" in row or "v" in row or ">" in row or "<" in row:
            col_idx = (
                row.index("^")
                if "^" in row
                else row.index("v")
                if "v" in row
                else row.index(">")
                if ">" in row
                else row.index("<")
            )
            direction = row[col_idx]
            return (row_idx, col_idx), direction
    return None, None


def is_within(map, pos):
    row, col = pos
    return 0 <= row < len(map) and 0 <= col < len(map[0])


def simulate_path(map, start_pos, start_dir):
    directions = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}
    turn_right = {"^": ">", ">": "v", "v": "<", "<": "^"}
    visited = set()
    visited.add(start_pos)
    current_pos = start_pos
    direction = start_dir
    while True:
        row, col = current_pos
        dr, dc = directions[direction]
        front_pos = (row + dr, col + dc)
        if is_within(map, front_pos):
            if map[front_pos[0]][front_pos[1]] == "#":
                # There's an obstacle, turn right
                direction = turn_right[direction]
            else:
                # Move forward
                current_pos = front_pos
                visited.add(current_pos)
        else:
            # Move forward out of the map
            break
    return visited


def part1(map):
    start_pos, start_dir = find_start(map)
    visited = simulate_path(map, start_pos, start_dir)
    return len(visited)


def simulate_path_with_obstruction(map, obstruction_pos):
    new_map = [list(row) for row in map]
    new_map[obstruction_pos[0]][obstruction_pos[1]] = "#"
    start_pos, start_dir = find_start(new_map)
    if start_pos == obstruction_pos:
        return False  # Obstruction cannot be placed at starting position
    directions = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}
    turn_right = {"^": ">", ">": "v", "v": "<", "<": "^"}
    seen = set()
    current_pos = start_pos
    direction = start_dir
    while True:
        state = (current_pos, direction)
        if state in seen:
            return True  # Loop detected
        seen.add(state)
        row, col = current_pos
        dr, dc = directions[direction]
        front_pos = (row + dr, col + dc)
        if is_within(new_map, front_pos):
            if new_map[front_pos[0]][front_pos[1]] == "#":
                # There's an obstacle, turn right
                direction = turn_right[direction]
            else:
                # Move forward
                current_pos = front_pos
        else:
            # Move forward out of the map
            break
    return False  # Guard leaves the map


def part2(map):
    rows = len(map)
    cols = len(map[0]) if rows > 0 else 0
    obstruction_positions = []
    for row in range(rows):
        for col in range(cols):
            if map[row][col] == ".":
                obstruction_pos = (row, col)
                # Add obstruction and simulate
                loops = simulate_path_with_obstruction(map, obstruction_pos)
                if loops:
                    obstruction_positions.append(obstruction_pos)
    return len(obstruction_positions)


def main():
    map = read_map()
    result1 = part1(map)
    print(f"Part 1: {result1}")
    result2 = part2(map)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
