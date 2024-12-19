from collections import deque


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_input(data: str):
    # Each line: "X,Y"
    coords = []
    for line in data.splitlines():
        x_str, y_str = line.split(",")
        x, y = int(x_str), int(y_str)
        coords.append((x, y))
    return coords


def bfs(grid, start, end):
    # grid is a set of corrupted (blocked) cells
    # BFS from start to end, return steps or -1 if no path
    if start in grid or end in grid:
        return -1
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    visited = set([start])
    queue = deque([(start, 0)])  # (position, distance)
    while queue:
        (cx, cy), dist = queue.popleft()
        if (cx, cy) == end:
            return dist
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx <= 70 and 0 <= ny <= 70:
                if (nx, ny) not in grid and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), dist + 1))
    return -1


def part1(data: str) -> int:
    coords = parse_input(data)
    # Place the first 1024 bytes
    corrupted = set(coords[:1024])
    # Compute the shortest path
    return bfs(corrupted, (0, 0), (70, 70))


def part2(data: str) -> str:
    coords = parse_input(data)
    corrupted = set()
    # We add one by one and check for path existence
    for i, c in enumerate(coords):
        corrupted.add(c)
        dist = bfs(corrupted, (0, 0), (70, 70))
        if dist == -1:
            # This is the first byte that breaks the path
            return f"{c[0]},{c[1]}"
    # If never breaks the path (unlikely), return something indicative
    return "-1,-1"


def main():
    data = read_input()
    result1 = part1(data)
    print(f"Part 1: {result1}")
    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
