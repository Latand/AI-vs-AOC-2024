from collections import deque


def read_input():
    with open("../input.txt") as f:
        return [tuple(map(int, line.strip().split(","))) for line in f if line.strip()]


def bfs(start, end, corrupted, grid_size):
    queue = deque()
    queue.append((start[0], start[1], 0))
    visited = set()
    visited.add((start[0], start[1]))
    while queue:
        x, y, steps = queue.popleft()
        if (x, y) == end:
            return steps
        moves = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for nx, ny in moves:
            if 0 <= nx < grid_size and 0 <= ny < grid_size:
                if (nx, ny) not in corrupted and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny, steps + 1))
    return None  # No path found


def part1(data):
    corrupted = set(data[:1024])
    path_length = bfs((0, 0), (70, 70), corrupted, 71)
    return path_length


def part2(data):
    corrupted = set()
    # Initial check
    if bfs((0, 0), (70, 70), corrupted, 71) is None:
        return "No initial path exists."
    for byte in data:
        corrupted.add(byte)
        if bfs((0, 0), (70, 70), corrupted, 71) is None:
            return f"{byte[0]},{byte[1]}"
    return "All bytes processed, path still exists."


def main():
    data = read_input()
    # Part one
    result1 = part1(data)
    print(f"Part 1: {result1}")
    # Part two
    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
