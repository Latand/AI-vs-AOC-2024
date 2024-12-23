def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def part1(data: str) -> int:
    """
    Solution for part 1
    """
    from collections import deque

    grid = [list(line) for line in data.splitlines()]
    rows, cols = len(grid), len(grid[0])
    start = end = None

    # Find start (S) and end (E) positions
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "S":
                start = (r, c)
            elif grid[r][c] == "E":
                end = (r, c)
    if not start or not end:
        return 0  # Invalid grid

    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    cheats = 0

    # BFS to find all possible cheats that save at least 100 picoseconds
    queue = deque()
    queue.append((start[0], start[1], 0, False))  # row, col, time, cheated

    visited = {}

    while queue:
        r, c, time, cheated = queue.popleft()

        if (r, c, cheated) in visited:
            continue
        visited[(r, c, cheated)] = time

        if (r, c) == end:
            if cheated and time <= 100:
                cheats += 1
            continue

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                cell = grid[nr][nc]
                if cell != "#" or cheated:
                    queue.append((nr, nc, time + 1, cheated))
                elif not cheated:
                    # Activate cheat for 2 picoseconds
                    queue.append((nr, nc, time + 1, True))

    return cheats


def part2(data: str) -> int:
    """
    Solution for part 2
    """
    from collections import deque

    grid = [list(line) for line in data.splitlines()]
    rows, cols = len(grid), len(grid[0])
    start = end = None

    # Find start (S) and end (E) positions
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "S":
                start = (r, c)
            elif grid[r][c] == "E":
                end = (r, c)
    if not start or not end:
        return 0  # Invalid grid

    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    cheats = 0

    # BFS to find all possible cheats that save at least 100 picoseconds with updated rules
    queue = deque()
    queue.append(
        (start[0], start[1], 0, False, 0)
    )  # row, col, time, cheated, cheat_time

    visited = {}

    while queue:
        r, c, time, cheated, cheat_time = queue.popleft()

        if (r, c, cheated, cheat_time) in visited:
            continue
        visited[(r, c, cheated, cheat_time)] = time

        if (r, c) == end:
            if cheated and time <= 100:
                cheats += 1
            continue

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                cell = grid[nr][nc]
                if cell != "#":
                    queue.append((nr, nc, time + 1, cheated, cheat_time))
                elif not cheated and cheat_time < 20:
                    # Activate or continue cheat
                    queue.append((nr, nc, time + 1, True, cheat_time + 1))

    return cheats


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
