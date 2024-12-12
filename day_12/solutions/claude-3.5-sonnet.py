from collections import deque, defaultdict
from typing import List, Set, Tuple, Dict


def find_regions(grid: List[str]) -> Dict[Tuple[str, int], Set[Tuple[int, int]]]:
    """Find all connected regions in the grid and return them as sets of coordinates."""
    rows, cols = len(grid), len(grid[0])
    visited = set()
    regions = {}
    region_count = {}

    def get_neighbors(r: int, c: int) -> List[Tuple[int, int]]:
        neighbors = []
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_r, new_c = r + dr, c + dc
            if 0 <= new_r < rows and 0 <= new_c < cols:
                neighbors.append((new_r, new_c))
        return neighbors

    def bfs(start_r: int, start_c: int, letter: str) -> Set[Tuple[int, int]]:
        region = set()
        queue = deque([(start_r, start_c)])

        while queue:
            r, c = queue.popleft()
            if (r, c) in visited or grid[r][c] != letter:
                continue

            visited.add((r, c))
            region.add((r, c))

            for nr, nc in get_neighbors(r, c):
                if (nr, nc) not in visited and grid[nr][nc] == letter:
                    queue.append((nr, nc))

        return region

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                letter = grid[r][c]
                region = bfs(r, c, letter)
                if region:
                    region_count[letter] = region_count.get(letter, 0) + 1
                    regions[(letter, region_count[letter] - 1)] = region

    return regions


def calculate_perimeter(region: Set[Tuple[int, int]], grid: List[str]) -> int:
    """Calculate the perimeter of a region (part 1)."""
    perimeter = 0
    for r, c in region:
        letter = grid[r][c]
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if (
                nr < 0
                or nr >= len(grid)
                or nc < 0
                or nc >= len(grid[0])
                or grid[nr][nc] != letter
            ):
                perimeter += 1
    return perimeter


def count_straight_lines(region: Set[Tuple[int, int]], grid: List[str]) -> int:
    """Count the number of straight-line segments that make up the region's boundary."""
    rows, cols = len(grid), len(grid[0])
    sides = 0
    visited = set()

    def get_boundary_type(r: int, c: int) -> List[bool]:
        """Return list of [top, right, bottom, left] boundaries."""
        result = []
        # Check top
        result.append(r == 0 or (r - 1, c) not in region)
        # Check right
        result.append(c == cols - 1 or (r, c + 1) not in region)
        # Check bottom
        result.append(r == rows - 1 or (r + 1, c) not in region)
        # Check left
        result.append(c == 0 or (r, c - 1) not in region)
        return result

    def count_segment_starts(r: int, c: int, boundaries: List[bool]) -> int:
        """Count how many line segments start at this cell."""
        count = 0
        top, right, bottom, left = boundaries

        # Check if this is the start of a horizontal segment
        if left and not right:  # Left boundary but not right
            if (r, c, "h") not in visited:
                visited.add((r, c, "h"))
                count += 1
        if right and not left:  # Right boundary but not left
            if (r, c, "h") not in visited:
                visited.add((r, c, "h"))
                count += 1

        # Check if this is the start of a vertical segment
        if top and not bottom:  # Top boundary but not bottom
            if (r, c, "v") not in visited:
                visited.add((r, c, "v"))
                count += 1
        if bottom and not top:  # Bottom boundary but not top
            if (r, c, "v") not in visited:
                visited.add((r, c, "v"))
                count += 1

        # Handle isolated cells (single squares)
        if sum(boundaries) == 4:  # Completely isolated
            count = 4

        return count

    # Process each cell in the region
    for r, c in region:
        boundaries = get_boundary_type(r, c)
        sides += count_segment_starts(r, c, boundaries)

    return sides


def solve_part1(grid: List[str]) -> int:
    """Solve part 1: Calculate total price using area × perimeter."""
    regions = find_regions(grid)
    total_price = 0

    for region in regions.values():
        area = len(region)
        perimeter = calculate_perimeter(region, grid)
        total_price += area * perimeter

    return total_price


def solve_part2(grid: List[str]) -> int:
    """Solve part 2: Calculate total price using area × number of sides."""
    regions = find_regions(grid)
    total_price = 0

    for region in regions.values():
        area = len(region)
        sides = count_straight_lines(region, grid)
        total_price += area * sides

    return total_price


def main():
    # Read input
    with open("../input.txt", "r") as f:
        grid = [line.strip() for line in f.readlines()]

    # Solve both parts
    part1_result = solve_part1(grid)
    part2_result = solve_part2(grid)

    print(f"Part 1: {part1_result}")
    print(f"Part 2: {part2_result}")


if __name__ == "__main__":
    main()
