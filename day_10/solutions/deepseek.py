from collections import deque


def read_input():
    with open("../input.txt") as f:
        return [list(map(int, line.strip())) for line in f.readlines()]


def part1(grid):
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    trailheads = [(i, j) for i in range(rows) for j in range(cols) if grid[i][j] == 0]

    total_score = 0
    for th in trailheads:
        visited = set()
        queue = deque([th])
        current_height = grid[th[0]][th[1]]
        while queue:
            x, y = queue.popleft()
            if grid[x][y] == 9:
                visited.add((x, y))
                continue
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols:
                    if grid[nx][ny] == grid[x][y] + 1 and (nx, ny) not in visited:
                        queue.append((nx, ny))
        total_score += len(visited)
    return total_score


def part2(grid):
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    dp = [[0 for _ in range(cols)] for _ in range(rows)]

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 9:
                dp[i][j] = 1

    heights = sorted(set(cell for row in grid for cell in row), reverse=True)
    for h in heights:
        if h == 9:
            continue
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == h:
                    for dx, dy in directions:
                        ni, nj = i + dx, j + dy
                        if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] == h + 1:
                            dp[i][j] += dp[ni][nj]

    trailheads = [(i, j) for i in range(rows) for j in range(cols) if grid[i][j] == 0]
    total_rating = sum(dp[i][j] for i, j in trailheads)
    return total_rating


def main():
    grid = read_input()
    result1 = part1(grid)
    print(f"Part 1: {result1}")
    result2 = part2(grid)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
