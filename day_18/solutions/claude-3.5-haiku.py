from collections import deque


def read_input():
    with open("../input.txt") as f:
        return [tuple(map(int, line.strip().split(","))) for line in f]


def part1(falling_bytes: list[tuple[int, int]]) -> int:
    # Grid size for the actual problem
    GRID_SIZE = 71

    # Create grid with initial state
    grid = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]

    # Mark corrupted bytes in grid
    for x, y in falling_bytes[:1024]:
        grid[y][x] = True

    # Breadth-first search to find shortest path
    def bfs() -> int:
        start = (0, 0)
        end = (GRID_SIZE - 1, GRID_SIZE - 1)

        # Possible moves: up, down, left, right
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        queue = deque([(start, 0)])
        visited = set([start])

        while queue:
            (x, y), steps = queue.popleft()

            if (x, y) == end:
                return steps

            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                # Check grid boundaries and if not corrupted
                if (
                    0 <= nx < GRID_SIZE
                    and 0 <= ny < GRID_SIZE
                    and not grid[ny][nx]
                    and (nx, ny) not in visited
                ):
                    queue.append(((nx, ny), steps + 1))
                    visited.add((nx, ny))

        return -1  # No path found

    return bfs()


def part2(falling_bytes: list[tuple[int, int]]) -> str:
    # Grid size for the actual problem
    GRID_SIZE = 71

    # Function to check if path exists
    def path_exists(corrupted_grid):
        # Breadth-first search to check path
        queue = deque([(0, 0)])
        visited = set([(0, 0)])

        while queue:
            x, y = queue.popleft()

            if x == GRID_SIZE - 1 and y == GRID_SIZE - 1:
                return True

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy

                if (
                    0 <= nx < GRID_SIZE
                    and 0 <= ny < GRID_SIZE
                    and not corrupted_grid[ny][nx]
                    and (nx, ny) not in visited
                ):
                    queue.append((nx, ny))
                    visited.add((nx, ny))

        return False

    # Initialize grid
    grid = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]

    # Find first byte that blocks path
    for x, y in falling_bytes[1024:]:
        grid[y][x] = True
        if not path_exists(grid):
            return f"{x},{y}"

    return "No blocking byte found"


def main():
    falling_bytes = read_input()

    result1 = part1(falling_bytes)
    print(f"Part 1: {result1}")

    result2 = part2(falling_bytes)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
