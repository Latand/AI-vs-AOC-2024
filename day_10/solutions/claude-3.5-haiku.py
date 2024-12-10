def read_input():
    with open("input.txt") as f:
        return [list(map(int, line)) for line in f.read().splitlines()]


def find_trailheads(grid):
    trailheads = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                trailheads.append((i, j))
    return trailheads


def count_reachable_9s(grid, trailhead):
    queue = [trailhead]
    visited = set([trailhead])
    count = 0
    while queue:
        x, y = queue.pop(0)
        if grid[x][y] == 9:
            count += 1
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < len(grid)
                and 0 <= ny < len(grid[0])
                and grid[nx][ny] == grid[x][y] + 1
                and (nx, ny) not in visited
            ):
                queue.append((nx, ny))
                visited.add((nx, ny))
    return count


def count_distinct_trails(grid, trailhead):
    queue = [trailhead]
    visited = set([trailhead])
    count = 0
    while queue:
        x, y = queue.pop(0)
        if grid[x][y] == 9:
            count += 1
        else:
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < len(grid)
                    and 0 <= ny < len(grid[0])
                    and grid[nx][ny] == grid[x][y] + 1
                    and (nx, ny) not in visited
                ):
                    queue.append((nx, ny))
                    visited.add((nx, ny))
    return count


def part1(data):
    grid = data
    trailheads = find_trailheads(grid)
    return sum(count_reachable_9s(grid, trailhead) for trailhead in trailheads)


def part2(data):
    grid = data
    trailheads = find_trailheads(grid)
    return sum(count_distinct_trails(grid, trailhead) for trailhead in trailheads)


if __name__ == "__main__":
    data = read_input()
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))
