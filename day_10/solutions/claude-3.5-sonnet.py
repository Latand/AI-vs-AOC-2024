from typing import List, Set, Tuple, Dict


def read_input():
    with open("input.txt") as f:
        return f.read().strip()


def parse_grid(data: str) -> List[List[int]]:
    """Convert input string to 2D grid of integers."""
    return [[int(c) for c in line] for line in data.splitlines()]


def get_neighbors(x: int, y: int, grid: List[List[int]]) -> List[Tuple[int, int]]:
    """Get valid neighboring positions (up, down, left, right)."""
    neighbors = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up

    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]):
            neighbors.append((new_x, new_y))

    return neighbors


def find_hiking_trails(
    start: Tuple[int, int],
    grid: List[List[int]],
    path: Set[Tuple[int, int]],
    current_height: int,
    cache: Dict[Tuple[int, int, int], int],
) -> int:
    """
    Find number of unique paths from start to height 9 that increase by 1 each step.
    Uses dynamic programming with caching for efficiency.
    """
    x, y = start

    # Cache key includes current position and height to handle different paths
    cache_key = (x, y, current_height)
    if cache_key in cache:
        return cache[cache_key]

    # If we reached height 9, we found a valid path
    if grid[x][y] == 9:
        return 1

    count = 0
    for next_x, next_y in get_neighbors(x, y, grid):
        if (next_x, next_y) not in path and grid[next_x][next_y] == current_height + 1:
            # Add current position to path and explore next positions
            new_path = path | {(next_x, next_y)}
            count += find_hiking_trails(
                (next_x, next_y), grid, new_path, current_height + 1, cache
            )

    cache[cache_key] = count
    return count


def find_trailheads(grid: List[List[int]]) -> List[Tuple[int, int]]:
    """Find all positions with height 0."""
    trailheads = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                trailheads.append((i, j))
    return trailheads


def part1(data: str) -> int:
    """
    Find sum of scores for all trailheads, where score is number of
    reachable height-9 positions.
    """
    grid = parse_grid(data)
    trailheads = find_trailheads(grid)
    total_score = 0

    for start_x, start_y in trailheads:
        # For each trailhead, find reachable height-9 positions
        reachable_nines = set()
        path = {(start_x, start_y)}

        def dfs(x: int, y: int, height: int):
            if grid[x][y] == 9:
                reachable_nines.add((x, y))
                return

            for next_x, next_y in get_neighbors(x, y, grid):
                if (next_x, next_y) not in path and grid[next_x][next_y] == height + 1:
                    path.add((next_x, next_y))
                    dfs(next_x, next_y, height + 1)
                    path.remove((next_x, next_y))

        dfs(start_x, start_y, 0)
        total_score += len(reachable_nines)

    return total_score


def part2(data: str) -> int:
    """
    Find sum of ratings for all trailheads, where rating is number of
    distinct possible paths to any height-9 position.
    """
    grid = parse_grid(data)
    trailheads = find_trailheads(grid)
    total_rating = 0

    for start_x, start_y in trailheads:
        # For each trailhead, count distinct paths using cached DFS
        cache = {}
        paths = find_hiking_trails(
            (start_x, start_y), grid, {(start_x, start_y)}, 0, cache
        )
        total_rating += paths

    return total_rating


if __name__ == "__main__":
    data = read_input()
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))
