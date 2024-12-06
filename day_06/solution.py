from enum import Enum
from typing import List, Set, Tuple


class Direction(Enum):
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)

    def turn_right(self) -> "Direction":
        return {
            Direction.UP: Direction.RIGHT,
            Direction.RIGHT: Direction.DOWN,
            Direction.DOWN: Direction.LEFT,
            Direction.LEFT: Direction.UP,
        }[self]


def read_input() -> str:
    with open("input.txt") as f:
        return f.read().rstrip("\n")


def parse_grid(data: str) -> Tuple[List[List[str]], Tuple[int, int], Direction]:
    grid = [list(line) for line in data.splitlines()]

    # Find starting position and direction
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == "^":
                return grid, (i, j), Direction.UP

    raise ValueError("No starting position found")


def is_valid_position(pos: Tuple[int, int], grid: List[List[str]]) -> bool:
    rows, cols = len(grid), len(grid[0])
    row, col = pos
    return 0 <= row < rows and 0 <= col < cols


def next_position(pos: Tuple[int, int], direction: Direction) -> Tuple[int, int]:
    return (pos[0] + direction.value[0], pos[1] + direction.value[1])


def detect_loop(
    grid: List[List[str]], start_pos: Tuple[int, int], start_dir: Direction
) -> bool:
    pos = start_pos
    direction = start_dir
    visited: Set[Tuple[Tuple[int, int], Direction]] = set()

    while True:
        # Store state (position + direction) to detect loops
        state = (pos, direction)
        if state in visited:
            return True
        visited.add(state)

        # Check position ahead
        next_pos = next_position(pos, direction)

        # If we're out of bounds, no loop
        if not is_valid_position(next_pos, grid):
            return False

        # If there's an obstacle ahead, turn right
        if grid[next_pos[0]][next_pos[1]] == "#":
            direction = direction.turn_right()
            continue

        # Move forward
        pos = next_pos


def part1(data: str) -> int:
    # Parse the grid and get starting position and direction
    grid, pos, direction = parse_grid(data)
    visited: Set[Tuple[int, int]] = {pos}

    while True:
        # Check position ahead
        next_pos = next_position(pos, direction)

        # If we're out of bounds, we're done
        if not is_valid_position(next_pos, grid):
            break

        # If there's an obstacle ahead, turn right
        if grid[next_pos[0]][next_pos[1]] == "#":
            direction = direction.turn_right()
            continue

        # Move forward
        pos = next_pos
        visited.add(pos)

    return len(visited)


def part2(data: str) -> int:
    # Parse the grid and get starting position
    grid, start_pos, start_dir = parse_grid(data)
    loop_positions = 0

    # Try each position
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            # Skip if position is already occupied or is start position
            if grid[i][j] != "." or (i, j) == start_pos:
                continue

            # Try placing obstacle here
            grid[i][j] = "#"

            # Check if this creates a loop
            if detect_loop(grid, start_pos, start_dir):
                loop_positions += 1

            # Reset the position
            grid[i][j] = "."

    return loop_positions


if __name__ == "__main__":
    data = read_input()
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))
