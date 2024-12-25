def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def part1(data: str) -> int:
    """
    Solution for part 1
    """
    grid = [list(row) for row in data.splitlines()]
    rows = len(grid)
    cols = len(grid[0])

    # Find starting position
    start_pos = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "^":
                start_pos = (r, c)
                break
        if start_pos:
            break

    visited = set()
    current_pos = start_pos
    direction = 0  # 0: up, 1: right, 2: down, 3: left

    while 0 <= current_pos[0] < rows and 0 <= current_pos[1] < cols:
        visited.add(current_pos)

        # Check for obstacle in front
        next_r, next_c = current_pos
        if direction == 0:
            next_r -= 1
        elif direction == 1:
            next_c += 1
        elif direction == 2:
            next_r += 1
        elif direction == 3:
            next_c -= 1

        if 0 <= next_r < rows and 0 <= next_c < cols and grid[next_r][next_c] == "#":
            direction = (direction + 1) % 4  # Turn right
        else:
            current_pos = (next_r, next_c)  # Move forward

    return len(visited)


def part2(data: str) -> int:
    """
    Solution for part 2
    """
    grid = [list(row) for row in data.splitlines()]
    rows = len(grid)
    cols = len(grid[0])

    # Find starting position
    start_pos = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "^":
                start_pos = (r, c)
                break
        if start_pos:
            break

    def simulate(obstruction_pos):
        temp_grid = [row[:] for row in grid]
        temp_grid[obstruction_pos[0]][obstruction_pos[1]] = "#"

        visited = set()
        path = []
        current_pos = start_pos
        direction = 0

        while 0 <= current_pos[0] < rows and 0 <= current_pos[1] < cols:
            if current_pos in visited:
                return True
            visited.add(current_pos)
            path.append(current_pos)
            next_r, next_c = current_pos
            if direction == 0:
                next_r -= 1
            elif direction == 1:
                next_c += 1
            elif direction == 2:
                next_r += 1
            elif direction == 3:
                next_c -= 1

            if (
                0 <= next_r < rows
                and 0 <= next_c < cols
                and temp_grid[next_r][next_c] == "#"
            ):
                direction = (direction + 1) % 4
            else:
                current_pos = (next_r, next_c)
        return False

    possible_obstructions = set()
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "." and (r, c) != start_pos:
                if simulate((r, c)):
                    possible_obstructions.add((r, c))

    return len(possible_obstructions)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
