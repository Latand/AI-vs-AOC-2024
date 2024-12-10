from typing import List, Tuple
import matplotlib.pyplot as plt
import numpy as np
from typing import Set, Dict
from matplotlib.colors import LinearSegmentedColormap


def parse_grid(data: str) -> List[List[int]]:
    """Convert input string to 2D grid of integers."""
    return [[int(c) for c in line] for line in data.splitlines()]


def get_neighbors(x: int, y: int, grid: List[List[int]]) -> List[Tuple[int, int]]:
    """Get valid neighboring positions (up, down, left, right)."""
    neighbors = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up

    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]):
            neighbors.append((new_x, new_y))

    return neighbors


def find_hiking_trails(
    start: Tuple[int, int],
    grid: List[List[int]],
    path: Set[Tuple[int, int]],
    current_height: int,
    cache: Dict[Tuple[int, int, int], int],
) -> int:
    """
    Find number of unique paths from start to height 9 that increase by 1 each step.
    Uses dynamic programming with caching for efficiency.
    """
    x, y = start

    # Cache key includes current position and height to handle different paths
    cache_key = (x, y, current_height)
    if cache_key in cache:
        return cache[cache_key]

    # If we reached height 9, we found a valid path
    if grid[x][y] == 9:
        return 1

    count = 0
    for next_x, next_y in get_neighbors(x, y, grid):
        if (next_x, next_y) not in path and grid[next_x][next_y] == current_height + 1:
            # Add current position to path and explore next positions
            new_path = path | {(next_x, next_y)}
            count += find_hiking_trails(
                (next_x, next_y), grid, new_path, current_height + 1, cache
            )

    cache[cache_key] = count
    return count


def find_trailheads(grid: List[List[int]]) -> List[Tuple[int, int]]:
    """Find all positions with height 0."""
    trailheads = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                trailheads.append((i, j))
    return trailheads


def part1(data: str) -> int:
    """
    Find sum of scores for all trailheads, where score is number of
    reachable height-9 positions.
    """
    grid = parse_grid(data)
    trailheads = find_trailheads(grid)
    total_score = 0

    for start_x, start_y in trailheads:
        # For each trailhead, find reachable height-9 positions
        reachable_nines = set()
        path = {(start_x, start_y)}

        def dfs(x: int, y: int, height: int):
            if grid[x][y] == 9:
                reachable_nines.add((x, y))
                return

            for next_x, next_y in get_neighbors(x, y, grid):
                if (next_x, next_y) not in path and grid[next_x][next_y] == height + 1:
                    path.add((next_x, next_y))
                    dfs(next_x, next_y, height + 1)
                    path.remove((next_x, next_y))

        dfs(start_x, start_y, 0)
        total_score += len(reachable_nines)

    return total_score


def part2(data: str) -> int:
    """
    Find sum of ratings for all trailheads, where rating is number of
    distinct possible paths to any height-9 position.
    """
    grid = parse_grid(data)
    trailheads = find_trailheads(grid)
    total_rating = 0

    for start_x, start_y in trailheads:
        # For each trailhead, count distinct paths using cached DFS
        cache = {}
        paths = find_hiking_trails(
            (start_x, start_y), grid, {(start_x, start_y)}, 0, cache
        )
        total_rating += paths

    return total_rating


def read_input():
    with open("input.txt") as f:
        return f.read().strip()


def get_brown_color(
    height: int, max_height: int = 9
) -> Tuple[float, float, float, float]:
    """Generate a contrasting color based on height."""
    # Use a dark red to burgundy gradient for trails
    dark_red = np.array([139 / 255, 0 / 255, 0 / 255])  # DarkRed
    burgundy = np.array([128 / 255, 0 / 255, 32 / 255])  # Burgundy

    # Calculate color based on height
    t = height / max_height
    color = dark_red * (1 - t) + burgundy * t
    return (*color, 0.8)  # Increased alpha for better visibility


def visualize_trails(data: str, save_path: str | None = None):
    """Create a visualization of the topographic map and hiking trails."""
    grid = parse_grid(data)
    grid_array = np.array(grid)

    # Create custom brown colormap
    light_brown = np.array([210 / 255, 180 / 255, 140 / 255])  # Light brown
    dark_brown = np.array([101 / 255, 67 / 255, 33 / 255])  # Dark brown

    colors = [
        (light_brown[0], light_brown[1], light_brown[2]),
        (dark_brown[0], dark_brown[1], dark_brown[2]),
    ]
    n_bins = 100
    brown_cmap = LinearSegmentedColormap.from_list("custom_brown", colors, N=n_bins)

    plt.figure(figsize=(12, 12))
    plt.imshow(grid_array, cmap=brown_cmap)
    plt.colorbar(label="Height")

    trailheads = find_trailheads(grid)

    # Create a proxy artist for the trails legend
    from matplotlib.lines import Line2D

    trail_proxy = Line2D(
        [0], [0], color=get_brown_color(5), linewidth=1, label="Trails"
    )

    for start_x, start_y in trailheads:
        path = {(start_x, start_y)}

        def visualize_paths(
            x: int, y: int, height: int, trail_points: List[Tuple[int, int]]
        ):
            if grid[x][y] == 9:
                trail_points.append((x, y))
                points = np.array(trail_points)

                # Draw segments with colors based on height
                for i in range(len(points) - 1):
                    pt1, pt2 = points[i : i + 2]
                    height = grid[pt1[0]][pt1[1]]
                    color = get_brown_color(height)
                    plt.plot(
                        [pt1[1], pt2[1]],
                        [pt1[0], pt2[0]],
                        "-",
                        color=color,
                        linewidth=1,
                    )

                trail_points.pop()
                return

            for next_x, next_y in get_neighbors(x, y, grid):
                if (next_x, next_y) not in path and grid[next_x][next_y] == height + 1:
                    path.add((next_x, next_y))
                    trail_points.append((next_x, next_y))
                    visualize_paths(next_x, next_y, height + 1, trail_points)
                    trail_points.pop()
                    path.remove((next_x, next_y))

        visualize_paths(start_x, start_y, 0, [(start_x, start_y)])

    # Mark trailheads
    trailhead_x, trailhead_y = zip(*trailheads)
    trailhead_scatter = plt.plot(
        trailhead_y,
        trailhead_x,
        "o",
        color="white",
        markersize=8,
        label="Trailheads",
        markeredgecolor="black",
    )[0]

    plt.title("Hiking Trails Topographic Map")
    plt.xlabel("X coordinate")
    plt.ylabel("Y coordinate")
    plt.legend(handles=[trail_proxy, trailhead_scatter])
    plt.grid(True, alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    else:
        plt.show()

    plt.close()


if __name__ == "__main__":
    data = read_input()
    # Create both 2D and 3D visualizations
    visualize_trails(data, "hiking_trails_map_2d.png")
