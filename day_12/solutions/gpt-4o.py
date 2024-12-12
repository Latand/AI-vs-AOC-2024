from collections import deque


def parse_input(filename):
    with open(filename, "r") as f:
        grid = [list(line.strip()) for line in f]
    return grid


def find_regions(grid):
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    regions = []

    def bfs(r, c, plant_type):
        queue = deque([(r, c)])
        region = []
        while queue:
            x, y = queue.popleft()
            if visited[x][y]:
                continue
            visited[x][y] = True
            region.append((x, y))
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < rows
                    and 0 <= ny < cols
                    and not visited[nx][ny]
                    and grid[nx][ny] == plant_type
                ):
                    queue.append((nx, ny))
        return region

    for r in range(rows):
        for c in range(cols):
            if not visited[r][c]:
                region = bfs(r, c, grid[r][c])
                regions.append((grid[r][c], region))
    return regions


def calculate_properties(grid, regions):
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    results = []
    for plant_type, region in regions:
        area = len(region)
        perimeter = 0
        sides = set()

        for r, c in region:
            for i, (dx, dy) in enumerate(directions):
                nx, ny = r + dx, c + dy
                if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == plant_type:
                    continue
                # Perimeter increment
                perimeter += 1
                # Add side for Part 2
                if 0 <= nx < rows and 0 <= ny < cols:
                    if i < 2:  # Vertical
                        sides.add((min(r, nx), c, "v"))
                    else:  # Horizontal
                        sides.add((r, min(c, ny), "h"))
                else:
                    sides.add((r, c, "o"))  # Edge of grid

        results.append((plant_type, area, perimeter, len(sides)))
    return results


def solve(grid):
    regions = find_regions(grid)
    properties = calculate_properties(grid, regions)

    part1_total = sum(area * perimeter for _, area, perimeter, _ in properties)
    part2_total = sum(area * sides for _, area, _, sides in properties)

    return part1_total, part2_total


if __name__ == "__main__":
    grid = parse_input("../input.txt")
    part1_result, part2_result = solve(grid)
    print(f"Part 1 Total Price: {part1_result}")
    print(f"Part 2 Total Price: {part2_result}")
