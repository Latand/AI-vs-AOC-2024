def read_input():
    with open("input.txt") as f:
        return f.read().rstrip("\n")


def turn_right(direction):
    # direction is one of '^', '>', 'v', '<'
    if direction == "^":
        return ">"
    elif direction == ">":
        return "v"
    elif direction == "v":
        return "<"
    elif direction == "<":
        return "^"
    return direction


def direction_vector(direction):
    if direction == "^":
        return (-1, 0)
    elif direction == "v":
        return (1, 0)
    elif direction == "<":
        return (0, -1)
    elif direction == ">":
        return (0, 1)
    return (0, 0)


def part1(data: str) -> int:
    grid = data.splitlines()

    # Find guard initial position and direction
    start_pos = None
    start_dir = None
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch in "^v<>":
                start_pos = (r, c)
                start_dir = ch
                break
        if start_pos is not None:
            break

    visited = set([start_pos])
    pos = start_pos
    direction = start_dir

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    while True:
        # Check what is ahead
        dr, dc = direction_vector(direction)
        ahead_r, ahead_c = pos[0] + dr, pos[1] + dc

        # If next step leaves the map, break
        if not (0 <= ahead_r < rows and 0 <= ahead_c < cols):
            break

        # If there's an obstacle ahead, turn right
        if grid[ahead_r][ahead_c] == "#":
            direction = turn_right(direction)
            continue

        # Otherwise, move forward
        pos = (ahead_r, ahead_c)
        visited.add(pos)

    return len(visited)


def part2(data: str) -> int:
    # Without additional instructions, let's just return 0 or implement later.
    return 0


if __name__ == "__main__":
    data = read_input()
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))
