def read_input() -> list:
    with open("../input.txt") as f:
        lines = f.read().strip().split("\n")
    byte_positions = [tuple(map(int, line.split(","))) for line in lines if line]
    return byte_positions


def simulate_bytes(byte_positions: list, grid_size: int = 70, limit: int = None) -> set:
    corrupted = set()
    for idx, (x, y) in enumerate(byte_positions):
        corrupted.add((x, y))
        if limit is not None and idx + 1 == limit:
            break
    return corrupted


def find_shortest_path(corrupted: set, grid_size: int = 70) -> int:
    from collections import deque

    start = (0, 0)
    end = (grid_size, grid_size)
    if start in corrupted or end in corrupted:
        return -1

    queue = deque([(start, 0)])
    visited = set([start])

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        current, steps = queue.popleft()
        if current == end:
            return steps

        for dx, dy in directions:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx <= grid_size and 0 <= ny <= grid_size:
                neighbor = (nx, ny)
                if neighbor not in corrupted and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, steps + 1))
    return -1


def part1(byte_positions: list) -> int:
    corrupted = simulate_bytes(byte_positions, grid_size=6, limit=12)
    path_length = find_shortest_path(corrupted, grid_size=6)
    return path_length if path_length != -1 else "No path found"


def part2(byte_positions: list) -> str:
    corrupted = set()
    grid_size = 6
    for idx, (x, y) in enumerate(byte_positions):
        corrupted.add((x, y))
        if find_shortest_path(corrupted, grid_size=grid_size) == -1:
            return f"{x},{y}"
    return "Path always exists"


def main():
    byte_positions = read_input()

    result1 = part1(byte_positions)
    print(f"Part 1: {result1}")

    result2 = part2(byte_positions)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
