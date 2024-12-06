from enum import Enum
from typing import List, Set, Tuple
import time


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
    # Start timing
    start_time = time.perf_counter()

    grid, start_pos, start_dir = parse_grid(data)

    # First, let's find all positions that the guard visits before leaving the map.
    # We'll store the full path (pos, direction) steps.
    visited_positions: Set[Tuple[int, int]] = set()
    path = []

    # Simulate the guard's path normally (without any new obstruction)
    pos, direction = start_pos, start_dir
    visited_positions.add(pos)
    path.append((pos, direction))
    while True:
        next_pos = next_position(pos, direction)
        if not is_valid_position(next_pos, grid):
            break
        if grid[next_pos[0]][next_pos[1]] == "#":
            # Turn right
            direction = direction.turn_right()
        else:
            # Move forward
            pos = next_pos
            visited_positions.add(pos)
        path.append((pos, direction))

    # We now know which positions were visited before leaving.
    # We need to check which positions, if turned into an obstacle, would create a loop.

    # The guard cannot see us place an obstruction at their starting position.
    # Also, we must consider only positions that are not originally obstacles.
    possible_positions = [
        p for p in visited_positions if p != start_pos and grid[p[0]][p[1]] != "#"
    ]

    loop_count = 0

    # To detect a loop, we re-simulate the guard's movement with the new obstruction.
    # If we ever revisit the same (pos, direction) state, we have a loop.
    # We'll give a reasonable upper bound iteration limit to detect loops (e.g. number of grid cells * 4 directions).

    rows, cols = len(grid), len(grid[0])
    max_steps = rows * cols * 4 * 5  # heuristic upper bound

    for obstruct in possible_positions:
        # Modify grid temporarily
        original = grid[obstruct[0]][obstruct[1]]
        grid[obstruct[0]][obstruct[1]] = "#"

        pos, direction = start_pos, start_dir
        seen_states = set()
        seen_states.add((pos, direction))

        loop_found = False
        for _ in range(max_steps):
            next_pos = next_position(pos, direction)
            if not is_valid_position(next_pos, grid):
                # Guard leaves
                break
            if grid[next_pos[0]][next_pos[1]] == "#":
                direction = direction.turn_right()
            else:
                pos = next_pos

            state = (pos, direction)
            if state in seen_states:
                # Loop detected
                loop_found = True
                break
            seen_states.add(state)

        if loop_found:
            loop_count += 1

        # Revert the grid
        grid[obstruct[0]][obstruct[1]] = original

    # End timing and calculate duration
    end_time = time.perf_counter()
    duration = end_time - start_time

    print(f"Part 2 execution time: {duration:.4f} seconds")
    return loop_count


if __name__ == "__main__":
    data = read_input()
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))
