def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def part1(data: str) -> int:
    """
    Solution for part 1
    """
    bytes_positions = [tuple(map(int, line.split(","))) for line in data.splitlines()]
    grid_size = 70
    grid = [["." for _ in range(grid_size + 1)] for _ in range(grid_size + 1)]

    for x, y in bytes_positions[:12]:  # Simulate the first 12 bytes
        grid[y][x] = "#"

    # Implement BFS or DFS to find the shortest path from (0,0) to (6,6)
    from collections import deque

    def is_valid(x, y):
        return 0 <= x <= grid_size and 0 <= y <= grid_size and grid[y][x] == "."

    queue = deque([(0, 0, 0)])  # (x, y, steps)
    visited = set((0, 0))

    while queue:
        x, y, steps = queue.popleft()
        if (x, y) == (6, 6):
            return steps

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny) and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny, steps + 1))

    return -1  # If no path found


def part2(data: str) -> str:
    """
    Solution for part 2
    """
    bytes_positions = [tuple(map(int, line.split(","))) for line in data.splitlines()]
    grid_size = 70
    grid = [["." for _ in range(grid_size + 1)] for _ in range(grid_size + 1)]

    for i, (x, y) in enumerate(bytes_positions):
        grid[y][x] = "#"
        # Check if there's still a path to (6,6)
        if i >= 12:  # Start checking after the first 12 bytes
            if not can_reach_exit(grid):
                return f"{x},{y}"

    return "No byte blocks the path"


def can_reach_exit(grid):
    from collections import deque

    queue = deque([(0, 0)])
    visited = set((0, 0))
    grid_size = len(grid) - 1

    while queue:
        x, y = queue.popleft()
        if (x, y) == (6, 6):
            return True

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if (
                0 <= nx <= grid_size
                and 0 <= ny <= grid_size
                and grid[ny][nx] == "."
                and (nx, ny) not in visited
            ):
                visited.add((nx, ny))
                queue.append((nx, ny))

    return False


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
