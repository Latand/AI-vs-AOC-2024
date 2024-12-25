def read_input():
    with open("../input.txt") as f:
        return [line.strip() for line in f.readlines()]


# Directions: Up, Right, Down, Left
DIRECTIONS = ["U", "R", "D", "L"]
DIR_VECTORS = {"U": (-1, 0), "R": (0, 1), "D": (1, 0), "L": (0, -1)}


def turn_right(current_dir):
    idx = DIRECTIONS.index(current_dir)
    return DIRECTIONS[(idx + 1) % 4]


def simulate_guard(maps, obstruction=None):
    # Find the starting position and direction
    for r, row in enumerate(maps):
        for c, val in enumerate(row):
            if val in ["^", ">", "v", "<"]:
                start_pos = (r, c)
                if val == "^":
                    direction = "U"
                elif val == ">":
                    direction = "R"
                elif val == "v":
                    direction = "D"
                elif val == "<":
                    direction = "L"
                break
        else:
            continue
        break
    else:
        raise ValueError("Guard starting position not found.")

    # Apply obstruction if provided
    if obstruction:
        orow, ocol = obstruction
        if (orow, ocol) != start_pos:
            # Replace the cell with obstruction
            maps = [list(row) for row in maps]
            maps[orow][ocol] = "#"
            maps = ["".join(row) for row in maps]

    visited = set()
    pos = start_pos
    dir = direction
    visited.add(pos)

    while True:
        dr, dc = DIR_VECTORS[dir]
        next_r, next_c = pos[0] + dr, pos[1] + dc

        # Check if next position is out of bounds
        if not (0 <= next_r < len(maps) and 0 <= next_c < len(maps[0])):
            break

        # Check if next position is an obstruction
        if maps[next_r][next_c] == "#":
            # Turn right
            dir = turn_right(dir)
        else:
            # Move forward
            pos = (next_r, next_c)
            visited.add(pos)

    return visited


def part1(data: list) -> int:
    """
    Simulate the guard's movement and count distinct positions visited before leaving the map.
    """
    visited_positions = simulate_guard(data)
    return len(visited_positions)


def part2(data: list) -> int:
    """
    Determine the number of positions where adding an obstruction would cause the guard to loop indefinitely.
    """
    possible_obstructions = []
    # Identify all empty positions except the guard's starting position
    for r, row in enumerate(data):
        for c, val in enumerate(row):
            if val == ".":
                possible_obstructions.append((r, c))

    loop_count = 0

    for obstruction in possible_obstructions:
        # Simulate guard movement with the obstruction
        try:
            visited = simulate_guard(data, obstruction=obstruction)
            # To detect a loop, we can check if the guard never leaves the map
            # If the simulation completes, it means the guard left the map
            # Hence, only count obstructions that prevent the guard from leaving
            # Since simulate_guard returns when the guard leaves, we skip these
            continue
        except:
            # If an error occurs (e.g., no movement), consider it a loop
            loop_count += 1
            continue

    # Alternatively, implement a more accurate loop detection
    # Here's an improved approach:

    # First, find all possible obstruction positions (excluding starting position and existing obstructions)
    possible_obstructions = []
    for r, row in enumerate(data):
        for c, val in enumerate(row):
            if val == "." and not (data[r][c] in ["^", ">", "v", "<"]):
                possible_obstructions.append((r, c))

    loop_count = 0

    for obstruction in possible_obstructions:
        # Create a modified map with the obstruction
        modified_map = [list(row) for row in data]
        modified_map[obstruction[0]][obstruction[1]] = "#"
        modified_map = ["".join(row) for row in modified_map]

        # Find the starting position and direction
        for r, row in enumerate(modified_map):
            for c, val in enumerate(row):
                if val in ["^", ">", "v", "<"]:
                    start_pos = (r, c)
                    if val == "^":
                        direction = "U"
                    elif val == ">":
                        direction = "R"
                    elif val == "v":
                        direction = "D"
                    elif val == "<":
                        direction = "L"
                    break
            else:
                continue
            break
        else:
            continue  # No starting position found

        # Simulate guard movement with loop detection
        visited_states = set()
        pos = start_pos
        dir = direction

        while True:
            state = (pos, dir)
            if state in visited_states:
                # Loop detected
                loop_count += 1
                break
            visited_states.add(state)

            dr, dc = DIR_VECTORS[dir]
            next_r, next_c = pos[0] + dr, pos[1] + dc

            # Check if next position is out of bounds
            if not (
                0 <= next_r < len(modified_map) and 0 <= next_c < len(modified_map[0])
            ):
                break  # Guard leaves the map

            # Check if next position is an obstruction
            if modified_map[next_r][next_c] == "#":
                # Turn right
                dir = turn_right(dir)
            else:
                # Move forward
                pos = (next_r, next_c)

    return loop_count


def main():
    data = read_input()
    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    main()
