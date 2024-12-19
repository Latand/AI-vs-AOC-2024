from typing import List, Tuple
from heapq import heappush, heappop
from collections import defaultdict

# Directions: East (0), North (1), West (2), South (3)
DIRECTIONS = [(0, 1), (-1, 0), (0, -1), (1, 0)]


def parse_maze(data: str) -> Tuple[List[List[str]], Tuple[int, int], Tuple[int, int]]:
    """Parse the maze input into a 2D grid with start and end positions."""
    maze = [list(row) for row in data.split("\n")]
    start, end = None, None
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == "S":
                start = (y, x)
            elif cell == "E":
                end = (y, x)
    return maze, start, end


def is_valid_move(maze: List[List[str]], pos: Tuple[int, int]) -> bool:
    """Check if a position is a valid move in the maze."""
    y, x = pos
    return 0 <= y < len(maze) and 0 <= x < len(maze[0]) and maze[y][x] != "#"


def find_best_paths(
    maze: List[List[str]], start: Tuple[int, int], end: Tuple[int, int]
) -> List[Tuple[Tuple[int, int], int]]:
    """Find all best paths through the maze with the lowest total score."""
    # State: (y, x, direction)
    queue = [(0, start[0], start[1], 0)]  # (score, y, x, direction)
    visited = defaultdict(lambda: float("inf"))
    best_paths = {}
    best_score = float("inf")

    while queue:
        score, y, x, direction = heappop(queue)

        # Skip if we've found a better path to this state
        if score > visited[(y, x, direction)]:
            continue

        # Reached end
        if (y, x) == end:
            if score < best_score:
                best_score = score
                best_paths = {(y, x): score}
            elif score == best_score:
                best_paths[(y, x)] = score
            continue

        # Try moving forward
        dy, dx = DIRECTIONS[direction]
        new_y, new_x = y + dy, x + dx
        if is_valid_move(maze, (new_y, new_x)):
            forward_score = score + 1
            if forward_score <= visited.get((new_y, new_x, direction), float("inf")):
                visited[(new_y, new_x, direction)] = forward_score
                heappush(queue, (forward_score, new_y, new_x, direction))

        # Try turning left and right
        for turn_direction in [(direction - 1) % 4, (direction + 1) % 4]:
            turn_score = score + 1000
            if turn_score <= visited.get((y, x, turn_direction), float("inf")):
                visited[(y, x, turn_direction)] = turn_score
                heappush(queue, (turn_score, y, x, turn_direction))

    return list(best_paths.keys())


def solve_maze(data: str, part2: bool = False) -> int:
    """Solve the maze challenge."""
    maze, start, end = parse_maze(data)

    if not part2:
        # Part 1: Find lowest score path
        queue = [(0, start[0], start[1], 0)]  # (score, y, x, direction)
        visited = defaultdict(lambda: float("inf"))

        while queue:
            score, y, x, direction = heappop(queue)

            # Reached end
            if (y, x) == end:
                return score

            # Skip if we've found a better path to this state
            if score > visited[(y, x, direction)]:
                continue

            # Try moving forward
            dy, dx = DIRECTIONS[direction]
            new_y, new_x = y + dy, x + dx
            if is_valid_move(maze, (new_y, new_x)):
                forward_score = score + 1
                if forward_score <= visited.get(
                    (new_y, new_x, direction), float("inf")
                ):
                    visited[(new_y, new_x, direction)] = forward_score
                    heappush(queue, (forward_score, new_y, new_x, direction))

            # Try turning left and right
            for turn_direction in [(direction - 1) % 4, (direction + 1) % 4]:
                turn_score = score + 1000
                if turn_score <= visited.get((y, x, turn_direction), float("inf")):
                    visited[(y, x, turn_direction)] = turn_score
                    heappush(queue, (turn_score, y, x, turn_direction))
    else:
        # Part 2: Count tiles on best paths
        best_path_tiles = find_best_paths(maze, start, end)
        return len(set(best_path_tiles))


def part1(data: str) -> int:
    return solve_maze(data)


def part2(data: str) -> int:
    return solve_maze(data, part2=True)


def main():
    with open("../input.txt") as f:
        data = f.read().strip()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
