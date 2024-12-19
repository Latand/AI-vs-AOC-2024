def read_input():
    lines = []
    with open("../input.txt") as f:
        for line in f:
            lines.append(line.rstrip("\n"))
    return lines


def parse_input(lines):
    map_lines = []
    i = 0
    while i < len(lines) and lines[i]:
        if "#" in lines[i]:
            map_lines.append(lines[i])
            i += 1
        else:
            break

    # skip blank lines
    while i < len(lines) and lines[i].strip() == "":
        i += 1

    move_lines = lines[i:]
    move_sequence = "".join(move_lines).replace("\n", "").strip()
    move_sequence = "".join(c for c in move_sequence if c in "^v<>")

    return map_lines, move_sequence


def direction_vector(move_char):
    if move_char == "^":
        return (-1, 0)
    elif move_char == "v":
        return (1, 0)
    elif move_char == "<":
        return (0, -1)
    elif move_char == ">":
        return (0, 1)
    return (0, 0)


### PART 1 LOGIC
def find_robot_and_boxes_part1(grid):
    robot_pos = None
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "@":
                robot_pos = (r, c)
    return robot_pos


def simulate_part1(grid, moves):
    R, C = len(grid), len(grid[0])
    robot_pos = find_robot_and_boxes_part1(grid)

    for m in moves:
        dx, dy = direction_vector(m)
        r, c = robot_pos
        nr, nc = r + dx, c + dy

        if not (0 <= nr < R and 0 <= nc < C):
            # Out of bounds, no move
            continue
        if grid[nr][nc] == "#":
            # Wall ahead
            continue

        if grid[nr][nc] == ".":
            # Move robot
            grid[r][c], grid[nr][nc] = ".", "@"
            robot_pos = (nr, nc)
        elif grid[nr][nc] == "O":
            # Push chain of boxes
            box_positions = []
            rr, cc = nr, nc
            while 0 <= rr < R and 0 <= cc < C and grid[rr][cc] == "O":
                box_positions.append((rr, cc))
                rr += dx
                cc += dy
            # rr, cc is next cell after last box
            if not (0 <= rr < R and 0 <= cc < C):
                continue
            if grid[rr][cc] in ["#", "@", "O"]:
                # cannot push
                continue

            # Pushing is possible
            # Clear old positions
            for br, bc in box_positions:
                grid[br][bc] = "."
            # Place boxes shifted
            grid[rr][cc] = "O"
            for i in range(len(box_positions) - 1):
                br, bc = box_positions[i]
                nbr, nbc = br + dx, bc + dy
                grid[nbr][nbc] = "O"

            # Move robot
            grid[r][c] = "."
            grid[nr][nc] = "@"
            robot_pos = (nr, nc)

    return grid


def gps_sum_part1(grid):
    total = 0
    R, C = len(grid), len(grid[0])
    for r in range(R):
        for c in range(C):
            if grid[r][c] == "O":
                total += 100 * r + c
    return total


### PART 2 LOGIC
def scale_up_map(original_grid):
    R = len(original_grid)
    C = len(original_grid[0])
    new_grid = [["" for _ in range(C)] for _ in range(R)]
    for r in range(R):
        for c in range(C):
            ch = original_grid[r][c]
            if ch == "#":
                new_grid[r][c] = "##"
            elif ch == ".":
                new_grid[r][c] = ".."
            elif ch == "O":
                new_grid[r][c] = "[]"
            elif ch == "@":
                new_grid[r][c] = "@."
            else:
                new_grid[r][c] = ".."
    return new_grid


def find_robot_part2(grid):
    R, C = len(grid), len(grid[0])
    for r in range(R):
        for c in range(C):
            if grid[r][c] == "@.":
                return (r, c)
    return None


def simulate_part2(grid, moves):
    # grid: R x C of two-char cells
    R, C = len(grid), len(grid[0])
    robot_pos = find_robot_part2(grid)

    for m in moves:
        dx, dy = direction_vector(m)
        r, c = robot_pos
        nr, nc = r + dx, c + dy

        if not (0 <= nr < R and 0 <= nc < C):
            # out of bounds
            continue
        if grid[nr][nc].startswith("#"):
            continue

        if grid[nr][nc] == "..":
            # move robot
            grid[r][c] = ".."
            grid[nr][nc] = "@."
            robot_pos = (nr, nc)
        elif grid[nr][nc] == "[]":
            # push chain of boxes
            box_positions = []
            rr, cc = nr, nc
            while 0 <= rr < R and 0 <= cc < C and grid[rr][cc] == "[]":
                box_positions.append((rr, cc))
                rr += dx
                cc += dy
            # rr, cc next cell after last box
            if not (0 <= rr < R and 0 <= cc < C):
                continue
            if grid[rr][cc].startswith("#") or grid[rr][cc] in ["@.", "[]"]:
                # blocked
                continue

            # push possible
            for br, bc in box_positions:
                grid[br][bc] = ".."
            grid[rr][cc] = "[]"
            for i in range(len(box_positions) - 1):
                br, bc = box_positions[i]
                nbr, nbc = br + dx, bc + dy
                grid[nbr][nbc] = "[]"

            # move robot
            grid[r][c] = ".."
            grid[nr][nc] = "@."
            robot_pos = (nr, nc)

    return grid


def gps_sum_part2(grid):
    # Convert to char-based lines
    R = len(grid)
    lines = ["".join(grid[r]) for r in range(R)]

    total = 0
    for r in range(R):
        line = lines[r]
        c = 0
        while True:
            c = line.find("[", c)
            if c == -1:
                break
            if c + 1 < len(line) and line[c + 1] == "]":
                # found box
                total += 100 * r + c
                c += 2
            else:
                c += 1
    return total


def part1(data):
    map_lines, moves = data
    grid = [list(line) for line in map_lines]
    grid = simulate_part1(grid, moves)
    return gps_sum_part1(grid)


def part2(data):
    map_lines, moves = data
    original_grid = [list(line) for line in map_lines]
    scaled_grid = scale_up_map(original_grid)
    scaled_grid = simulate_part2(scaled_grid, moves)
    return gps_sum_part2(scaled_grid)


def main():
    lines = read_input()
    data = parse_input(lines)

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
