def read_input():
    with open("input.txt") as f:
        return f.read().strip()


from collections import deque
from functools import lru_cache


def part1(data: str) -> int:
    """Solve part 1 of the puzzle."""
    grid = [list(map(int, line)) for line in data.splitlines()]
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    trailheads = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 0]
    total_score = 0

    for trailhead in trailheads:
        visited = [[False for _ in range(cols)] for _ in range(rows)]
        q = deque()
        q.append(trailhead)
        visited[trailhead[0]][trailhead[1]] = True
        reachable_nines = set()

        while q:
            r, c = q.popleft()
            current_height = grid[r][c]

            # If current position is height 9, add to reachable set
            if current_height == 9:
                reachable_nines.add((r, c))
                continue  # No need to go further from height 9

            # Explore neighbors
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    neighbor_height = grid[nr][nc]
                    if neighbor_height == current_height + 1 and not visited[nr][nc]:
                        visited[nr][nc] = True
                        q.append((nr, nc))

        total_score += len(reachable_nines)

    return total_score


def part2(data: str) -> int:
    """Solve part 2 of the puzzle."""
    grid = [list(map(int, line)) for line in data.splitlines()]
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    trailheads = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 0]

    # Memoization cache for number of paths from each position
    @lru_cache(maxsize=None)
    def count_paths(r, c):
        current_height = grid[r][c]
        if current_height == 9:
            return 1  # One path ending here

        total = 0
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbor_height = grid[nr][nc]
                if neighbor_height == current_height + 1:
                    total += count_paths(nr, nc)
        return total

    total_rating = 0
    for trailhead in trailheads:
        total_rating += count_paths(trailhead[0], trailhead[1])

    return total_rating


if __name__ == "__main__":
    data = read_input()

    print("Part 1:", part1(data))
    print("Part 2:", part2(data))
