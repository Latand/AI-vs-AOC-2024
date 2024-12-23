from collections import deque


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def bfs(data: str, allow_cheat: bool) -> int:
    grid = [list(line) for line in data.splitlines()]
    start = end = None
    rows, cols = len(grid), len(grid[0])

    # Locate start (S) and end (E) positions
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "S":
                start = (r, c)
            elif grid[r][c] == "E":
                end = (r, c)

    # Directions for moving in the grid
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    queue = deque([(start[0], start[1], 0, False)])  # (row, col, time, used_cheat)
    visited = set()

    while queue:
        r, c, time, used_cheat = queue.popleft()

        if (r, c) == end:
            return time

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] == "." or grid[nr][nc] == "E":
                    if (nr, nc, used_cheat) not in visited:
                        visited.add((nr, nc, used_cheat))
                        queue.append((nr, nc, time + 1, used_cheat))
                elif grid[nr][nc] == "#" and allow_cheat and not used_cheat:
                    # Use cheat to go through the wall
                    if (nr, nc, True) not in visited:
                        visited.add((nr, nc, True))
                        queue.append((nr, nc, time + 1, True))

    return float("inf")  # If no path is found


def part1(data: str) -> int:
    """
    Solution for part 1
    """
    return bfs(data, allow_cheat=False)


def part2(data: str) -> int:
    """
    Solution for part 2
    """
    return bfs(data, allow_cheat=True)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
