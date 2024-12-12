def calculate_region_data(grid):
    """
    Calculates the area, perimeter, and sides of each region in the grid.

    Args:
        grid: A list of strings representing the garden plot map.

    Returns:
        A dictionary where keys are plant types and values are lists of tuples,
        each tuple containing (area, perimeter, sides) for a region of that type.
    """
    rows = len(grid)
    cols = len(grid[0])
    visited = set()
    regions = {}

    def dfs(row, col, plant_type, region_data):
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or (row, col) in visited
            or grid[row][col] != plant_type
        ):
            return

        visited.add((row, col))
        region_data["area"] += 1

        # Check neighbors for perimeter and sides calculation
        neighbors = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
        ]
        for nr, nc in neighbors:
            if (
                nr < 0
                or nr >= rows
                or nc < 0
                or nc >= cols
                or grid[nr][nc] != plant_type
            ):
                region_data["perimeter"] += 1

                # Sides calculation: Only increment if it's a new side
                if nr == row - 1:  # Up
                    if (row, col, "up") not in region_data["sides_set"]:
                        region_data["sides"] += 1
                        region_data["sides_set"].add((row, col, "up"))
                elif nr == row + 1:  # Down
                    if (row, col, "down") not in region_data["sides_set"]:
                        region_data["sides"] += 1
                        region_data["sides_set"].add((row, col, "down"))
                elif nc == col - 1:  # Left
                    if (row, col, "left") not in region_data["sides_set"]:
                        region_data["sides"] += 1
                        region_data["sides_set"].add((row, col, "left"))
                elif nc == col + 1:  # Right
                    if (row, col, "right") not in region_data["sides_set"]:
                        region_data["sides"] += 1
                        region_data["sides_set"].add((row, col, "right"))

        for nr, nc in neighbors:
            dfs(nr, nc, plant_type, region_data)

    for row in range(rows):
        for col in range(cols):
            if (row, col) not in visited:
                plant_type = grid[row][col]
                region_data = {
                    "area": 0,
                    "perimeter": 0,
                    "sides": 0,
                    "sides_set": set(),
                }
                dfs(row, col, plant_type, region_data)

                if plant_type not in regions:
                    regions[plant_type] = []
                regions[plant_type].append(
                    (
                        region_data["area"],
                        region_data["perimeter"],
                        region_data["sides"],
                    )
                )

    return regions


def solve_part1(grid):
    """
    Calculates the total price of fencing all regions using area * perimeter.

    Args:
        grid: A list of strings representing the garden plot map.

    Returns:
        The total price of fencing.
    """
    regions = calculate_region_data(grid)
    total_price = 0
    for plant_type, region_list in regions.items():
        for area, perimeter, _ in region_list:
            total_price += area * perimeter
    return total_price


def solve_part2(grid):
    """
    Calculates the total price of fencing all regions using area * sides.

    Args:
        grid: A list of strings representing the garden plot map.

    Returns:
        The total price of fencing.
    """
    regions = calculate_region_data(grid)
    total_price = 0
    for plant_type, region_list in regions.items():
        for area, _, sides in region_list:
            total_price += area * sides
    return total_price


if __name__ == "__main__":
    with open("../input.txt", "r") as f:
        grid = [line.strip() for line in f]

    part1_price = solve_part1(grid)
    print(f"Part 1: Total price of fencing (area * perimeter) = {part1_price}")

    part2_price = solve_part2(grid)
    print(f"Part 2: Total price of fencing (area * sides) = {part2_price}")
