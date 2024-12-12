from collections import deque


def read_input():
    with open("../input.txt") as f:
        return [line.strip() for line in f.readlines()]


def get_neighbors(r, c, rows, cols):
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in dirs:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            yield nr, nc


def bfs(start_r, start_c, grid, visited, rows, cols, plant_type):
    queue = deque()
    queue.append((start_r, start_c))
    visited[start_r][start_c] = True
    region = []

    while queue:
        r, c = queue.popleft()
        region.append((r, c))
        for nr, nc in get_neighbors(r, c, rows, cols):
            if not visited[nr][nc] and grid[nr][nc] == plant_type:
                visited[nr][nc] = True
                queue.append((nr, nc))

    area = len(region)
    perimeter = 0
    for r, c in region:
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if (
                nr < 0
                or nr >= rows
                or nc < 0
                or nc >= cols
                or grid[nr][nc] != plant_type
            ):
                perimeter += 1
    return area, perimeter, region


def calculate_sides(region, grid, rows, cols):
    edges = set()
    for r, c in region:
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if (
                nr < 0
                or nr >= rows
                or nc < 0
                or nc >= cols
                or grid[nr][nc] != grid[r][c]
            ):
                if dr == -1 and dc == 0:
                    edges.add(((r, c), "top"))
                elif dr == 1 and dc == 0:
                    edges.add(((r, c), "bottom"))
                elif dr == 0 and dc == -1:
                    edges.add(((r, c), "left"))
                elif dr == 0 and dc == 1:
                    edges.add(((r, c), "right"))

    edges = list(edges)
    if not edges:
        return 0

    # Sort edges to traverse them in order
    # This is a simplified approach and may not work for all shapes
    # A more robust approach would be needed for complex shapes
    edges_sorted = sorted(edges, key=lambda x: (x[0][0], x[0][1]))
    current_pos, current_dir = edges_sorted[0]
    sides = 1
    directions = {"top": (0, -1), "bottom": (0, 1), "left": (-1, 0), "right": (1, 0)}

    current_dir_vector = directions[current_dir]
    for i in range(1, len(edges_sorted)):
        pos, dir = edges_sorted[i]
        dir_vector = directions[dir]
        if dir_vector != current_dir_vector:
            sides += 1
            current_dir_vector = dir_vector

    return sides


def part1(grid):
    rows, cols = len(grid), len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    total_price = 0
    for r in range(rows):
        for c in range(cols):
            if not visited[r][c]:
                plant_type = grid[r][c]
                area, perimeter, _ = bfs(r, c, grid, visited, rows, cols, plant_type)
                price = area * perimeter
                total_price += price
    return total_price


def part2(grid):
    rows, cols = len(grid), len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    total_price = 0
    for r in range(rows):
        for c in range(cols):
            if not visited[r][c]:
                plant_type = grid[r][c]
                _, _, region = bfs(r, c, grid, visited, rows, cols, plant_type)
                area = len(region)
                sides = calculate_sides(region, grid, rows, cols)
                price = area * sides
                total_price += price
    return total_price


def main():
    grid = read_input()
    if not grid:
        print("No input grid provided.")
        return
    result1 = part1(grid)
    print(f"Part 1: {result1}")
    result2 = part2(grid)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
