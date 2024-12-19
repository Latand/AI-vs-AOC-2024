from collections import defaultdict, deque
from heapq import heappush, heappop
import sys
from typing import List, Set, Tuple, Dict


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


# Directions: 0=right, 1=down, 2=left, 3=up
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def parse_maze(data: str) -> Tuple[List[str], Tuple[int, int], Tuple[int, int]]:
    """Parse the maze and return the grid and start/end positions."""
    grid = data.split("\n")
    start = end = None

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "S":
                start = (i, j)
            elif grid[i][j] == "E":
                end = (i, j)

    return grid, start, end


def dijkstra(
    grid: List[str], start: Tuple[int, int], end: Tuple[int, int]
) -> Tuple[int, Dict]:
    """Run Dijkstra's algorithm with turning costs."""
    rows, cols = len(grid), len(grid[0])

    # State: (row, col, direction)
    # Initially facing east (0)
    initial_state = (start[0], start[1], 0)

    # Distance from start to each state
    distances = defaultdict(lambda: sys.maxsize)
    distances[initial_state] = 0

    # Previous state for reconstructing path
    previous = {}

    # Priority queue: (distance, row, col, direction)
    pq = [(0, start[0], start[1], 0)]

    while pq:
        dist, row, col, direction = heappop(pq)

        if (row, col) == end:
            return dist, previous

        # Skip if we've found a better path to this state
        if dist > distances[(row, col, direction)]:
            continue

        # Try all possible moves from current position
        for new_dir in range(4):
            # Calculate turning cost
            turn_cost = 0
            if new_dir != direction:
                # Cost for turning 90 degrees
                turn_cost = 1000

            # Get new position
            dr, dc = DIRS[new_dir]
            new_row, new_col = row + dr, col + dc

            # Check if move is valid
            if (
                0 <= new_row < rows
                and 0 <= new_col < cols
                and grid[new_row][new_col] != "#"
            ):
                new_cost = dist + turn_cost + 1  # 1 is the cost to move forward

                if new_cost < distances[(new_row, new_col, new_dir)]:
                    distances[(new_row, new_col, new_dir)] = new_cost
                    previous[(new_row, new_col, new_dir)] = (row, col, direction)
                    heappush(pq, (new_cost, new_row, new_col, new_dir))

    return float("inf"), previous


def get_optimal_paths(
    grid: List[str],
    start: Tuple[int, int],
    end: Tuple[int, int],
    min_cost: int,
    previous: Dict,
) -> Set[Tuple[int, int]]:
    """Find all tiles that are part of any optimal path."""
    rows, cols = len(grid), len(grid[0])
    optimal_tiles = set()

    # Try all possible final directions
    for final_dir in range(4):
        if (end[0], end[1], final_dir) not in previous:
            continue

        current_cost = 0
        current = (end[0], end[1], final_dir)
        path_tiles = set()

        # Reconstruct path
        while current in previous:
            row, col, dir = current
            path_tiles.add((row, col))
            prev_row, prev_col, prev_dir = previous[current]

            # Calculate cost between states
            if dir != prev_dir:
                current_cost += 1000
            current_cost += 1

            current = (prev_row, prev_col, prev_dir)

        # Add start tile
        path_tiles.add(start)

        # If this is an optimal path, add its tiles to the set
        if current_cost == min_cost:
            optimal_tiles.update(path_tiles)

    return optimal_tiles


def part1(data: str) -> int:
    """Find the minimum cost path through the maze."""
    grid, start, end = parse_maze(data)
    min_cost, previous = dijkstra(grid, start, end)
    return min_cost


def part2(data: str) -> int:
    """Count tiles that are part of any optimal path."""
    grid, start, end = parse_maze(data)
    min_cost, previous = dijkstra(grid, start, end)
    optimal_tiles = get_optimal_paths(grid, start, end, min_cost, previous)
    return len(optimal_tiles)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
