import sys
from collections import deque


def read_input():
    with open("../input.txt") as f:
        return [list(line.strip()) for line in f.readlines()]


def get_neighbors(r, c, rows, cols):
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in dirs:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            yield nr, nc


def bfs_region(grid, visited, start_r, start_c, rows, cols):
    queue = deque()
    queue.append((start_r, start_c))
    visited.add((start_r, start_c))
    region = set()
    region.add((start_r, start_c))
    region_type = grid[start_r][start_c]
    while queue:
        r, c = queue.popleft()
        for nr, nc in get_neighbors(r, c, rows, cols):
            if (nr, nc) not in visited and grid[nr][nc] == region_type:
                visited.add((nr, nc))
                region.add((nr, nc))
                queue.append((nr, nc))
    return region


def calculate_perimeter_part1(region, grid, rows, cols):
    perimeter = 0
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
                perimeter += 1
    return perimeter


def calculate_straight_sections(region, grid, rows, cols):
    # Find the starting boundary cell
    min_r, min_c = min(region)
    start = min_r, min_c
    # Define movement directions in clockwise order
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
    # Initialize traversal
    current_dir = 0  # Start with right
    straight_sections = 1  # At least one straight section
    visited_boundary = set()
    prev_r, prev_c = start
    cr, cc = start
    while True:
        visited_boundary.add((cr, cc))
        # Determine next direction
        found = False
        for i in range(4):
            nd = (current_dir + i) % 4
            dr, dc = dirs[nd]
            nr, nc = cr + dr, cc + dc
            if (nr, nc) in region and (nr, nc) not in visited_boundary:
                # Turn to this direction
                if i != 0:
                    straight_sections += 1
                current_dir = nd
                prev_r, prev_c = cr, cc
                cr, cc = nr, nc
                found = True
                break
        if not found:
            break
        if (cr, cc) == start and len(visited_boundary) > 1:
            break
    return straight_sections


def main():
    grid = read_input()
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    visited = set()
    total_price_part1 = 0
    total_price_part2 = 0
    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                region = bfs_region(grid, visited, r, c, rows, cols)
                area = len(region)
                # Part 1: Calculate perimeter
                perimeter_part1 = calculate_perimeter_part1(region, grid, rows, cols)
                price_part1 = area * perimeter_part1
                total_price_part1 += price_part1
                # Part 2: Calculate number of straight sections
                straight_sections = calculate_straight_sections(
                    region, grid, rows, cols
                )
                price_part2 = area * straight_sections
                total_price_part2 += price_part2
    print(f"Part 1 Total Price: {total_price_part1}")
    print(f"Part 2 Total Price: {total_price_part2}")


if __name__ == "__main__":
    main()
