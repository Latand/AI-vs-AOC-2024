from collections import deque


def read_input():
    with open("input.txt") as f:
        return f.read().strip()


def bfs_count_trailheads(
    map_data: list[list[int]], start: tuple[int, int]
) -> tuple[int, int]:
    """Perform BFS to count reachable heights of 9 and distinct trails."""
    queue = deque([start])
    visited = set()
    score = 0
    rating = 0
    trail_count = {}

    while queue:
        x, y = queue.popleft()
        if (x, y) in visited:
            continue
        visited.add((x, y))

        if map_data[x][y] == 9:
            score += 1
            rating += trail_count.get((x, y), 0)
            continue

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < len(map_data)
                and 0 <= ny < len(map_data[0])
                and map_data[nx][ny] == map_data[x][y] + 1
            ):
                queue.append((nx, ny))
                trail_count[(nx, ny)] = trail_count.get((nx, ny), 0) + 1

    return score, rating


def part1(data: str) -> int:
    """Solve part 1 of the puzzle."""
    map_data = [list(map(int, line)) for line in data.splitlines()]
    total_score = 0

    for i in range(len(map_data)):
        for j in range(len(map_data[0])):
            if map_data[i][j] == 0:  # Trailhead
                score, _ = bfs_count_trailheads(map_data, (i, j))
                total_score += score

    return total_score


def part2(data: str) -> int:
    """Solve part 2 of the puzzle."""
    map_data = [list(map(int, line)) for line in data.splitlines()]
    total_rating = 0

    for i in range(len(map_data)):
        for j in range(len(map_data[0])):
            if map_data[i][j] == 0:  # Trailhead
                _, rating = bfs_count_trailheads(map_data, (i, j))
                total_rating += rating

    return total_rating


if __name__ == "__main__":
    data = read_input()

    print("Part 1:", part1(data))
    print("Part 2:", part2(data))
