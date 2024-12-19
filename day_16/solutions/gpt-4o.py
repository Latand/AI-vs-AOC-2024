from collections import deque


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_maze(data: str):
    maze = [list(line) for line in data.splitlines()]
    start = None
    end = None
    for y, row in enumerate(maze):
        for x, char in enumerate(row):
            if char == "S":
                start = (x, y)
            elif char == "E":
                end = (x, y)
    return maze, start, end


def get_neighbors(x, y, maze):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and maze[ny][nx] != "#":
            yield nx, ny


def bfs_shortest_path(maze, start, end):
    queue = deque([(start, 0)])  # (position, score)
    visited = set()
    visited.add(start)
    while queue:
        (x, y), score = queue.popleft()
        if (x, y) == end:
            return score
        for nx, ny in get_neighbors(x, y, maze):
            if (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), score + 1))
    return float("inf")


def part1(data: str) -> int:
    """
    Solution for part 1
    """
    maze, start, end = parse_maze(data)
    return bfs_shortest_path(maze, start, end)


def part2(data: str) -> int:
    """
    Solution for part 2
    """
    maze, start, end = parse_maze(data)
    # For part 2, we need to find all tiles that are part of any best path
    # This can be done by running BFS from the end to all reachable tiles
    queue = deque([end])
    visited = set()
    visited.add(end)
    while queue:
        x, y = queue.popleft()
        for nx, ny in get_neighbors(x, y, maze):
            if (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))
    # Count all non-wall tiles that are reachable
    return sum(
        1
        for y, row in enumerate(maze)
        for x, char in enumerate(row)
        if char != "#" and (x, y) in visited
    )


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
