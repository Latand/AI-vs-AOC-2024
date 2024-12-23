from collections import deque


def read_input(filename):
    with open(filename, "r") as f:
        grid = [list(line.strip()) for line in f if line.strip()]
    return grid


def get_neighbors(x, y, max_x, max_y):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Left, Right, Up, Down
    neighbors = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < max_x and 0 <= ny < max_y:
            neighbors.append((nx, ny))
    return neighbors


def flood_fill(grid, x, y, visited, region_id):
    queue = deque()
    queue.append((x, y))
    visited.add((x, y))
    region_cells = [(x, y)]
    plant_type = grid[y][x]

    while queue:
        cx, cy = queue.popleft()
        for nx, ny in get_neighbors(cx, cy, len(grid[0]), len(grid)):
            if (nx, ny) not in visited and grid[ny][nx] == plant_type:
                visited.add((nx, ny))
                queue.append((nx, ny))
                region_cells.append((nx, ny))
    return region_cells, plant_type


def compute_perimeter_and_sides(region_cells, grid):
    perimeter = 0
    boundary_edges = []
    boundary_cells = set()
    for x, y in region_cells:
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < len(grid[0]) and 0 <= ny < len(grid)):
                perimeter += 1
                boundary_cells.add((x, y))
            elif grid[ny][nx] != grid[y][x]:
                perimeter += 1
                boundary_cells.add((x, y))
    # For Part Two: Trace the boundary to compute number of sides
    sides = trace_boundary(boundary_cells, grid)
    return perimeter, sides


def trace_boundary(boundary_cells, grid):
    # Use Moore-Neighbor tracing algorithm
    # Directions: N, NW, W, SW, S, SE, E, NE (clockwise)
    directions = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]
    direction_mapping = {
        (-1, 0): "W",
        (-1, -1): "NW",
        (0, -1): "N",
        (1, -1): "NE",
        (1, 0): "E",
        (1, 1): "SE",
        (0, 1): "S",
        (-1, 1): "SW",
    }
    # Find starting point (boundary cell with minimum coordinates)
    start_cell = min(boundary_cells)
    x0, y0 = start_cell
    boundary = []
    visited = set()
    x, y = x0, y0
    prev_direction = None
    sides = 0
    while True:
        for i in range(len(directions)):
            dx, dy = directions[i]
            nx, ny = x + dx, y + dy
            if (nx, ny) in boundary_cells:
                current_direction = (dx, dy)
                if current_direction != prev_direction:
                    sides += 1
                    prev_direction = current_direction
                boundary.append((x, y))
                visited.add((x, y))
                x, y = nx, ny
                break
        else:
            # No unvisited boundary neighbor found
            break
        if (x, y) == (x0, y0):
            break
    return sides


def calculate_prices(grid):
    max_y = len(grid)
    max_x = len(grid[0])
    visited = set()
    regions = []
    for y in range(max_y):
        for x in range(max_x):
            if (x, y) not in visited:
                region_cells, plant_type = flood_fill(grid, x, y, visited, len(regions))
                regions.append({"cells": region_cells, "plant_type": plant_type})
    total_price_part1 = 0
    total_price_part2 = 0
    for region in regions:
        area = len(region["cells"])
        perimeter, sides = compute_perimeter_and_sides(region["cells"], grid)
        price_part1 = area * perimeter
        price_part2 = area * sides
        total_price_part1 += price_part1
        total_price_part2 += price_part2
    return total_price_part1, total_price_part2


def main():
    grid = read_input("../input.txt")
    part1_price, part2_price = calculate_prices(grid)
    print(f"Total price for Part One: {part1_price}")
    print(f"Total price for Part Two: {part2_price}")


if __name__ == "__main__":
    main()
