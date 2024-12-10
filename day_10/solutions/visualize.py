from typing import List, Tuple
import matplotlib.pyplot as plt
import numpy as np
from typing import Set, Dict


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


def visualize_trails(data: str, save_path: str | None = None):
    """
    Create a visualization of the topographic map and hiking trails.

    Args:
        data: Input data string
        save_path: Optional path to save the visualization
    """
    # Parse the grid
    grid = parse_grid(data)
    grid_array = np.array(grid)

    # Set up the plot
    plt.figure(figsize=(12, 12))

    # Create topographic map
    plt.imshow(grid_array, cmap="terrain")
    plt.colorbar(label="Height")

    # Find and visualize trails from each trailhead
    trailheads = find_trailheads(grid)
    colors = plt.cm.rainbow(np.linspace(0, 1, len(trailheads)))

    for (start_x, start_y), color in zip(trailheads, colors):
        path = {(start_x, start_y)}

        def visualize_paths(
            x: int, y: int, height: int, trail_points: List[Tuple[int, int]]
        ):
            """Recursively find and visualize all possible paths."""
            if grid[x][y] == 9:
                # Draw the trail
                trail_points.append((x, y))
                points = np.array(trail_points)
                plt.plot(
                    points[:, 1], points[:, 0], "-", color=color, alpha=0.3, linewidth=1
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

        # Start visualization from this trailhead
        visualize_paths(start_x, start_y, 0, [(start_x, start_y)])

    # Mark trailheads
    trailhead_x, trailhead_y = zip(*trailheads)
    plt.plot(trailhead_y, trailhead_x, "wo", markersize=8, label="Trailheads")

    # Customize plot
    plt.title("Hiking Trails Topographic Map")
    plt.xlabel("X coordinate")
    plt.ylabel("Y coordinate")
    plt.legend()
    plt.grid(True, alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    else:
        plt.show()

    plt.close()


def visualize_trails_3d(data: str, save_path: str | None = None):
    """
    Create a 3D visualization of the topographic map and hiking trails.

    Args:
        data: Input data string
        save_path: Optional path to save the visualization
    """
    # Parse the grid
    grid = parse_grid(data)
    grid_array = np.array(grid)

    # Scale down the height values to make elevation changes much less steep
    height_scale = 0.001  # Reduced by 10x for much flatter terrain
    scaled_grid = grid_array * height_scale

    # Create coordinate matrices with proper scaling
    x_scale = 1.0  # Keep original x scale
    y_scale = 1.0  # Keep original y scale
    x = np.arange(grid_array.shape[1]) * x_scale
    y = np.arange(grid_array.shape[0]) * y_scale
    x, y = np.meshgrid(x, y)

    # Set up the 3D plot
    fig = plt.figure(figsize=(15, 12))
    ax = fig.add_subplot(111, projection="3d")

    # Create surface plot with scaled heights but original x,y scales
    surface = ax.plot_surface(
        x, y, scaled_grid, cmap="terrain", alpha=0.8, linewidth=0, antialiased=True
    )

    # Add colorbar showing original height values
    fig.colorbar(surface, label="Original Height")

    # Find and visualize trails from each trailheads
    trailheads = find_trailheads(grid)
    colors = plt.cm.hsv(np.linspace(0, 1, len(trailheads)))

    for (start_x, start_y), color in zip(trailheads, colors):
        path = {(start_x, start_y)}

        def visualize_paths_3d(
            x: int, y: int, height: int, trail_points: List[Tuple[int, int]]
        ):
            """Recursively find and visualize all possible paths in 3D."""
            if grid[x][y] == 9:
                # Draw the trail
                trail_points.append((x, y))
                points = np.array(trail_points)
                # Scale heights for trails and add tiny offset to make them visible
                heights = np.array(
                    [
                        grid[px][py] * height_scale + 0.005 for px, py in trail_points
                    ]  # Reduced offset
                )
                ax.plot3D(
                    points[:, 1] * x_scale,  # x coordinates with scale
                    points[:, 0] * y_scale,  # y coordinates with scale
                    heights,  # z coordinates already scaled
                    "-",
                    color=color,
                    alpha=0.6,
                    linewidth=2,
                )
                trail_points.pop()
                return

            for next_x, next_y in get_neighbors(x, y, grid):
                if (next_x, next_y) not in path and grid[next_x][next_y] == height + 1:
                    path.add((next_x, next_y))
                    trail_points.append((next_x, next_y))
                    visualize_paths_3d(next_x, next_y, height + 1, trail_points)
                    trail_points.pop()
                    path.remove((next_x, next_y))

        # Start visualization from this trailhead
        visualize_paths_3d(start_x, start_y, 0, [(start_x, start_y)])

        # Mark trailhead with a sphere (using scaled height but original x,y)
        ax.scatter(
            [start_y * x_scale],
            [start_x * y_scale],
            [grid[start_x][start_y] * height_scale],
            color="white",
            s=100,
            label="Trailhead" if (start_x, start_y) == trailheads[0] else "",
        )

    # Customize plot
    ax.set_title("3D Hiking Trails Topographic Map")
    ax.set_xlabel("X coordinate")
    ax.set_ylabel("Y coordinate")
    ax.set_zlabel("Height")

    # Set the viewing angle for better visualization
    ax.view_init(elev=20, azim=45)  # Reduced elevation angle for better perspective

    # Add legend
    ax.legend()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    else:
        plt.show()

    plt.close()


if __name__ == "__main__":
    data = read_input()
    # Create both 2D and 3D visualizations
    visualize_trails(data, "hiking_trails_map_2d.png")
    visualize_trails_3d(data, "hiking_trails_map_3d.png")
