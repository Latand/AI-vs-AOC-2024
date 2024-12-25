from typing import List, Tuple, Set, Dict
from enum import Enum, auto


class Direction(Enum):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()


def read_input() -> List[str]:
    with open("../input.txt") as f:
        return f.read().splitlines()


def parse_map(
    grid: List[str],
) -> Tuple[Tuple[int, int], Direction, Set[Tuple[int, int]]]:
    """
    Parse the input grid to find guard's starting position, initial direction,
    and obstacles (walls).
    """
    obstacles = set()
    guard_pos = None
    initial_dir = Direction.UP

    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == "#":
                obstacles.add((x, y))
            elif char == "^":
                guard_pos = (x, y)
                initial_dir = Direction.UP
            elif char == "v":
                guard_pos = (x, y)
                initial_dir = Direction.DOWN
            elif char == ">":
                guard_pos = (x, y)
                initial_dir = Direction.RIGHT
            elif char == "<":
                guard_pos = (x, y)
                initial_dir = Direction.LEFT

    return guard_pos, initial_dir, obstacles


def get_next_direction(current_dir: Direction) -> Direction:
    """
    Rotate 90 degrees right from the current direction.
    """
    rotations = {
        Direction.UP: Direction.RIGHT,
        Direction.RIGHT: Direction.DOWN,
        Direction.DOWN: Direction.LEFT,
        Direction.LEFT: Direction.UP,
    }
    return rotations[current_dir]


def get_next_position(pos: Tuple[int, int], direction: Direction) -> Tuple[int, int]:
    """
    Get the next position based on current position and direction.
    """
    x, y = pos
    if direction == Direction.UP:
        return (x, y - 1)
    elif direction == Direction.RIGHT:
        return (x + 1, y)
    elif direction == Direction.DOWN:
        return (x, y + 1)
    elif direction == Direction.LEFT:
        return (x - 1, y)


def simulate_guard_path(grid: List[str]) -> Set[Tuple[int, int]]:
    """
    Simulate the guard's path and return all visited positions.
    """
    guard_pos, current_dir, obstacles = parse_map(grid)
    visited = {guard_pos}
    max_x = len(grid[0]) - 1
    max_y = len(grid) - 1

    while True:
        # Check the next position
        next_pos = get_next_position(guard_pos, current_dir)

        # Check if next position is out of bounds
        x, y = next_pos
        if x < 0 or x > max_x or y < 0 or y > max_y:
            break

        # If obstacle is in front, rotate right
        if next_pos in obstacles:
            current_dir = get_next_direction(current_dir)
        else:
            # Move forward
            guard_pos = next_pos
            visited.add(guard_pos)

    return visited


def find_potential_loop_blockers(grid: List[str]) -> Set[Tuple[int, int]]:
    """
    Find all positions where adding an obstacle would cause the guard to enter a loop.
    Exclude the starting position.
    """
    guard_pos, initial_dir, initial_obstacles = parse_map(grid)
    max_x = len(grid[0]) - 1
    max_y = len(grid) - 1

    potential_blockers = set()

    # Try adding an obstacle at each empty position
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            # Skip if already an obstacle or the starting position
            if (x, y) in initial_obstacles or (x, y) == guard_pos:
                continue

            # Create a copy of the grid and mark the test obstacle
            test_grid = grid.copy()
            test_grid[y] = test_grid[y][:x] + "#" + test_grid[y][x + 1 :]

            # Reset initial conditions
            current_pos = guard_pos
            current_dir = initial_dir
            visited = {current_pos}
            path_log = [current_pos]
            iterations = 0

            while iterations < 10000:  # Prevent infinite loop
                next_pos = get_next_position(current_pos, current_dir)

                # Check out of bounds
                if (
                    next_pos[0] < 0
                    or next_pos[0] > max_x
                    or next_pos[1] < 0
                    or next_pos[1] > max_y
                ):
                    break

                # Check obstacle
                if next_pos in initial_obstacles.union({(x, y)}):
                    current_dir = get_next_direction(current_dir)
                else:
                    current_pos = next_pos

                    # Check for loop
                    if current_pos in path_log:
                        potential_blockers.add((x, y))
                        break

                    visited.add(current_pos)
                    path_log.append(current_pos)

                iterations += 1

    return potential_blockers


def part1(grid: List[str]) -> int:
    """
    Count the number of distinct positions the guard visits.
    """
    return len(simulate_guard_path(grid))


def part2(grid: List[str]) -> int:
    """
    Count the number of possible positions to place a blocker to force a loop.
    """
    return len(find_potential_loop_blockers(grid))


def main():
    grid = read_input()

    result1 = part1(grid)
    print(f"Part 1: {result1}")

    result2 = part2(grid)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
