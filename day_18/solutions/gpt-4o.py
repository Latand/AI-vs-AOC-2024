from collections import deque


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_input(data: str):
    return [tuple(map(int, line.split(","))) for line in data.splitlines()]


def is_within_bounds(x, y, size=70):
    return 0 <= x <= size and 0 <= y <= size


def bfs(start, end, grid, size=70):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    queue = deque([(start, 0)])
    visited = set([start])

    while queue:
        (x, y), steps = queue.popleft()
        if (x, y) == end:
            return steps

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (
                is_within_bounds(nx, ny, size)
                and (nx, ny) not in visited
                and not grid[nx][ny]
            ):
                visited.add((nx, ny))
                queue.append(((nx, ny), steps + 1))
    return -1


def part1(data: str) -> int:
    byte_positions = parse_input(data)
    grid_size = 70
    grid = [[False] * (grid_size + 1) for _ in range(grid_size + 1)]

    for x, y in byte_positions[:1024]:
        grid[x][y] = True

    return bfs((0, 0), (grid_size, grid_size), grid)


def part2(data: str) -> str:
    byte_positions = parse_input(data)
    grid_size = 70
    grid = [[False] * (grid_size + 1) for _ in range(grid_size + 1)]

    for i, (x, y) in enumerate(byte_positions):
        grid[x][y] = True
        if bfs((0, 0), (grid_size, grid_size), grid) == -1:
            return f"{x},{y}"

    return "No blocking byte found"


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
