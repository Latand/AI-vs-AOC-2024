def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_map(data: str):
    """
    Parses the input data into a 2D grid.
    """
    return [list(line) for line in data.splitlines()]


def calculate_regions(grid, rows, cols, calculate_sides=False):
    """
    Calculates regions, areas, and perimeter or sides based on the flag `calculate_sides`.
    """
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    regions = []

    def dfs(x, y, plant_type):
        stack = [(x, y)]
        area = 0
        measure = 0  # Perimeter or sides, based on flag
        while stack:
            cx, cy = stack.pop()
            if visited[cx][cy]:
                continue
            visited[cx][cy] = True
            area += 1
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < rows and 0 <= ny < cols:
                    if not visited[nx][ny]:
                        if grid[nx][ny] == plant_type:
                            stack.append((nx, ny))
                        else:
                            measure += 1
                else:
                    measure += 1
        if calculate_sides:
            # Each plot contributes its own 4 sides, minus overlapping edges
            measure = area * 4 - measure
        return area, measure

    for i in range(rows):
        for j in range(cols):
            if not visited[i][j]:
                area, measure = dfs(i, j, grid[i][j])
                regions.append((area, measure))
    return regions


def part1(data: str) -> int:
    """
    Solution for part 1: Calculate total cost based on area and perimeter.
    """
    grid = parse_map(data)
    rows, cols = len(grid), len(grid[0])
    regions = calculate_regions(grid, rows, cols, calculate_sides=False)
    return sum(area * perimeter for area, perimeter in regions)


def part2(data: str) -> int:
    """
    Solution for part 2: Calculate total cost based on area and number of sides.
    """
    grid = parse_map(data)
    rows, cols = len(grid), len(grid[0])
    regions = calculate_regions(grid, rows, cols, calculate_sides=True)
    return sum(area * sides for area, sides in regions)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
