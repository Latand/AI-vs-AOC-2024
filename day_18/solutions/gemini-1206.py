import heapq


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_input(data):
    return [tuple(map(int, line.split(","))) for line in data.split("\n")]


def is_valid(x, y, grid_size):
    return 0 <= x < grid_size and 0 <= y < grid_size


def find_path(grid, start, end):
    heap = [(0, start)]
    visited = set()
    while heap:
        cost, (x, y) = heapq.heappop(heap)
        if (x, y) == end:
            return cost
        if (x, y) in visited:
            continue
        visited.add((x, y))
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny, len(grid)) and grid[ny][nx] == 0:
                heapq.heappush(heap, (cost + 1, (nx, ny)))
    return -1


def part1(data: str) -> int:
    """
    Solution for part 1
    """
    bytes_data = parse_input(data)
    grid_size = 71
    grid = [[0] * grid_size for _ in range(grid_size)]
    for x, y in bytes_data[:1024]:
        grid[y][x] = 1
    return find_path(grid, (0, 0), (grid_size - 1, grid_size - 1))


def part2(data: str) -> str:
    """
    Solution for part 2
    """
    bytes_data = parse_input(data)
    grid_size = 71
    for i in range(1, len(bytes_data)):
        grid = [[0] * grid_size for _ in range(grid_size)]
        for x, y in bytes_data[:i]:
            grid[y][x] = 1
        if find_path(grid, (0, 0), (grid_size - 1, grid_size - 1)) == -1:
            return f"{bytes_data[i][0]},{bytes_data[i][1]}"
    return ""


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
