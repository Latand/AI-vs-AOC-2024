from collections import deque


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_map(data: str):
    grid = [list(line) for line in data.splitlines()]
    start = end = None
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == "S":
                start = (r, c)
            elif val == "E":
                end = (r, c)
    return grid, start, end


def bfs(grid, start, end, cheat=False):
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    queue = deque([(start, 0, 0)])  # (position, steps, cheats_used)
    visited = set()
    visited.add((start, 0))  # (position, cheats_used)

    while queue:
        (r, c), steps, cheats_used = queue.popleft()
        if (r, c) == end:
            return steps

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] == "." or grid[nr][nc] == "E":
                    if ((nr, nc), cheats_used) not in visited:
                        visited.add(((nr, nc), cheats_used))
                        queue.append(((nr, nc), steps + 1, cheats_used))
                elif cheat and cheats_used < 1:
                    if ((nr, nc), cheats_used + 1) not in visited:
                        visited.add(((nr, nc), cheats_used + 1))
                        queue.append(((nr, nc), steps + 1, cheats_used + 1))
    return float("inf")


def part1(data: str) -> int:
    """
    Solution for part 1
    """
    grid, start, end = parse_map(data)
    return bfs(grid, start, end)


def part2(data: str) -> int:
    """
    Solution for part 2
    """
    grid, start, end = parse_map(data)
    return bfs(grid, start, end, cheat=True)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
