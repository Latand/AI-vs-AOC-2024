from typing import List, Tuple, Set
from collections import deque, defaultdict


def parse_grid(data: str) -> List[List[str]]:
    """Parse the input grid into a 2D list."""
    return [list(row) for row in data.strip().split("\n")]


def find_start_end(grid: List[List[str]]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """Find start and end positions in the grid."""
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == "S":
                start = (x, y)
            elif cell == "E":
                end = (x, y)
    return start, end


def is_valid_move(grid: List[List[str]], x: int, y: int) -> bool:
    """Check if a move is within grid and not a wall."""
    return 0 <= y < len(grid) and 0 <= x < len(grid[0]) and grid[y][x] != "#"


def get_neighbors(grid: List[List[str]], x: int, y: int) -> List[Tuple[int, int]]:
    """Get valid neighboring positions."""
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    return [
        (x + dx, y + dy) for dx, dy in directions if is_valid_move(grid, x + dx, y + dy)
    ]


def explore_cheats(
    grid: List[List[str]],
    start: Tuple[int, int],
    end: Tuple[int, int],
    max_cheat_time: int,
) -> List[int]:
    """
    Explore all possible cheats and their time savings.

    Returns a list of time savings for each unique cheat.
    """
    cheat_savings = []
    h, w = len(grid), len(grid[0])

    # Try every possible start of a cheat
    for start_y in range(h):
        for start_x in range(w):
            # Only consider non-wall starting points
            if grid[start_y][start_x] == "#":
                continue

            # Try every possible end of the cheat
            for end_y in range(h):
                for end_x in range(w):
                    # Only consider non-wall ending points
                    if grid[end_y][end_x] == "#":
                        continue

                    # Skip if start and end are the same
                    if (start_x, start_y) == (end_x, end_y):
                        continue

                    # Attempt to find a wall-passing path from start to end
                    visited = set()
                    queue = deque([(start_x, start_y, 0, False)])

                    while queue:
                        x, y, cheat_time, used_cheat = queue.popleft()

                        # Check if we've reached the end
                        if (x, y) == (end_x, end_y):
                            # Calculate time saved by cheating through walls
                            time_saved = cheat_time
                            if time_saved > 0:
                                cheat_savings.append(time_saved)
                            break

                        # Avoid revisiting states
                        state = (x, y, used_cheat)
                        if state in visited:
                            continue
                        visited.add(state)

                        # Normal moves
                        for nx, ny in get_neighbors(grid, x, y):
                            queue.append((nx, ny, cheat_time, used_cheat))

                        # Cheat moves (if not already used a cheat)
                        if not used_cheat and cheat_time < max_cheat_time:
                            # Try moving through walls
                            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                                nx, ny = x + dx, y + dy
                                # Ignore if wall and would exceed cheat time
                                queue.append((nx, ny, cheat_time + 1, True))

    return cheat_savings


def part1(data: str) -> int:
    """
    Count cheats saving at least 100 picoseconds using 2-picosecond cheat rule.
    """
    grid = parse_grid(data)
    start, end = find_start_end(grid)

    # Find cheats that save at least 100 picoseconds
    cheats = explore_cheats(grid, start, end, max_cheat_time=2)
    return sum(1 for cheat in cheats if cheat >= 100)


def part2(data: str) -> int:
    """
    Count cheats saving at least 100 picoseconds using 20-picosecond cheat rule.
    """
    grid = parse_grid(data)
    start, end = find_start_end(grid)

    # Find cheats that save at least 100 picoseconds
    cheats = explore_cheats(grid, start, end, max_cheat_time=20)
    return sum(1 for cheat in cheats if cheat >= 100)


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
