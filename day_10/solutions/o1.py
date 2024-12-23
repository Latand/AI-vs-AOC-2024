def read_input():
    with open("input.txt") as f:
        return f.read().strip()


def get_neighbors(x, y, width, height):
    """Returns the valid neighbors (up/down/left/right) of a cell (x, y)."""
    neighbors = []
    if x > 0:
        neighbors.append((x - 1, y))  # Left
    if x < width - 1:
        neighbors.append((x + 1, y))  # Right
    if y > 0:
        neighbors.append((x, y - 1))  # Up
    if y < height - 1:
        neighbors.append((x, y + 1))  # Down
    return neighbors


def part1(data: str) -> int:
    """Solve part 1 of the puzzle."""
    # Parse the input into a grid
    grid_lines = data.strip().splitlines()
    grid = []
    for line in grid_lines:
        grid.append([int(c) for c in line])

    height = len(grid)
    width = len(grid[0])

    # Find all trailheads (positions with height 0)
    trailheads = []
    for y in range(height):
        for x in range(width):
            if grid[y][x] == 0:
                trailheads.append((x, y))

    total_score = 0

    for trailhead in trailheads:
        x0, y0 = trailhead
        # Positions at each height reachable from the trailhead
        positions_at_height = {h: set() for h in range(10)}
        positions_at_height[grid[y0][x0]].add((x0, y0))

        # For heights from 1 to 9
        for h in range(1, 10):
            for x, y in positions_at_height[h - 1]:
                # Check neighbors
                for nx, ny in get_neighbors(x, y, width, height):
                    if grid[ny][nx] == h:
                        positions_at_height[h].add((nx, ny))

        # The score is the number of unique positions at height 9
        score = len(positions_at_height[9])
        total_score += score

    return total_score


def part2(data: str) -> int:
    """Solve part 2 of the puzzle."""
    # Parse the input into a grid
    grid_lines = data.strip().splitlines()
    grid = []
    for line in grid_lines:
        grid.append([int(c) for c in line])

    height = len(grid)
    width = len(grid[0])

    # Find all trailheads (positions with height 0)
    trailheads = []
    for y in range(height):
        for x in range(width):
            if grid[y][x] == 0:
                trailheads.append((x, y))

    total_rating = 0

    for trailhead in trailheads:
        x0, y0 = trailhead
        # Initialize ways to reach each position
        ways = {}
        ways[(x0, y0)] = 1  # We have one way to reach the trailhead

        # For heights from current height up to 9
        for h in range(1, 10):
            # Positions at height h
            positions_at_h = []
            for y in range(height):
                for x in range(width):
                    if grid[y][x] == h:
                        positions_at_h.append((x, y))

            for x, y in positions_at_h:
                total_ways = 0
                # Check neighbors at height h - 1
                for nx, ny in get_neighbors(x, y, width, height):
                    if grid[ny][nx] == h - 1 and (nx, ny) in ways:
                        total_ways += ways[(nx, ny)]
                if total_ways > 0:
                    ways[(x, y)] = total_ways

        # The rating is the sum of ways to reach positions at height 9
        rating = sum(ways[pos] for pos in ways if grid[pos[1]][pos[0]] == 9)
        total_rating += rating

    return total_rating


if __name__ == "__main__":
    data = read_input()

    print("Part 1:", part1(data))
    print("Part 2:", part2(data))
