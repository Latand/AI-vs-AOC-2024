from collections import deque


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def part1(data: str) -> int:
    """
    Solution for part 1
    """
    maze = [list(line) for line in data.splitlines()]
    start, end = (0, 0), (0, 0)
    for r in range(len(maze)):
        for c in range(len(maze[r])):
            if maze[r][c] == "S":
                start = (r, c)
            elif maze[r][c] == "E":
                end = (r, c)

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
    queue = deque([(start[0], start[1], 0)])  # (row, col, score)
    visited = set()
    visited.add(start)

    while queue:
        r, c, score = queue.popleft()
        if (r, c) == end:
            return score  # Return the score when reaching the end

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]) and maze[nr][nc] != "#":
                if (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc, score + 1))

    return -1  # If no path found


def part2(data: str) -> int:
    """
    Solution for part 2
    """
    maze = [list(line) for line in data.splitlines()]
    start, end = (0, 0), (0, 0)
    for r in range(len(maze)):
        for c in range(len(maze[r])):
            if maze[r][c] == "S":
                start = (r, c)
            elif maze[r][c] == "E":
                end = (r, c)

    best_paths = set()
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
    queue = deque([(start[0], start[1], 0)])  # (row, col, score)
    visited = set()
    visited.add(start)

    while queue:
        r, c, score = queue.popleft()
        if (r, c) == end:
            best_paths.add((r, c))  # Add end to best paths
            continue

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]) and maze[nr][nc] != "#":
                if (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc, score + 1))
                    best_paths.add((nr, nc))  # Track all visited paths

    return len(best_paths)  # Return the count of best path tiles


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
