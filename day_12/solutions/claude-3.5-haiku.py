from typing import List, Dict, Set, Tuple


def find_regions(garden_map: List[str]) -> Dict[str, List[Tuple[int, int]]]:
    """Find and group connected garden plots by their plant type."""
    rows, cols = len(garden_map), len(garden_map[0])
    visited = set()
    regions = {}

    def dfs(r: int, c: int, plant_type: str, current_region: Set[Tuple[int, int]]):
        """Depth-first search to find connected plots of the same type."""
        if (
            r < 0
            or r >= rows
            or c < 0
            or c >= cols
            or garden_map[r][c] != plant_type
            or (r, c) in visited
        ):
            return

        visited.add((r, c))
        current_region.add((r, c))

        # Check 4-directional adjacency
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, plant_type, current_region)

    # Find regions for each plant type
    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                plant_type = garden_map[r][c]
                region = set()
                dfs(r, c, plant_type, region)

                if plant_type not in regions:
                    regions[plant_type] = []
                regions[plant_type].append(list(region))

    return regions


def calculate_region_price(region: List[Tuple[int, int]], part2: bool = False) -> int:
    """Calculate the price of a region based on area and perimeter/sides."""
    area = len(region)

    # Convert to set for faster lookup
    region_set = set(region)

    # Directional checks to count unique boundaries
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    sides = 0
    for r, c in region:
        for dr, dc in directions:
            if (r + dr, c + dc) not in region_set:
                sides += 1

    # Part 2 uses number of sides, Part 1 uses perimeter
    return area * sides


def solve(garden_map: List[str], part2: bool = False) -> int:
    """Solve the garden plot fencing challenge."""
    regions = find_regions(garden_map)

    total_price = 0
    for plant_type, plant_regions in regions.items():
        total_price += sum(
            calculate_region_price(region, part2) for region in plant_regions
        )

    return total_price


def main():
    # Read input from file
    with open("../input.txt", "r") as f:
        garden_map = [line.strip() for line in f.readlines()]

    # Solve Part 1
    part1_result = solve(garden_map, part2=False)
    print(f"Part 1 - Total Fence Price: {part1_result}")

    # Solve Part 2
    part2_result = solve(garden_map, part2=True)
    print(f"Part 2 - Total Fence Price with New Calculation: {part2_result}")


if __name__ == "__main__":
    main()
