from typing import List, Set, Tuple
from enum import Enum
import copy


class Direction(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)

    def turn_right(self):
        directions = list(Direction)
        return directions[(directions.index(self) + 1) % 4]


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_map(data: str) -> Tuple[List[List[str]], Tuple[int, int], Direction]:
    grid = [list(line) for line in data.splitlines()]

    # Find guard's starting position and direction
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "^":
                grid[y][x] = "."
                return grid, (x, y), Direction.UP
            elif grid[y][x] == ">":
                grid[y][x] = "."
                return grid, (x, y), Direction.RIGHT
            elif grid[y][x] == "v":
                grid[y][x] = "."
                return grid, (x, y), Direction.DOWN
            elif grid[y][x] == "<":
                grid[y][x] = "."
                return grid, (x, y), Direction.LEFT

    raise ValueError("No guard found in input map")


def is_valid_position(grid: List[List[str]], pos: Tuple[int, int]) -> bool:
    return 0 <= pos[1] < len(grid) and 0 <= pos[0] < len(grid[0])


def part1(data: str) -> int:
    grid, start_pos, start_dir = parse_map(data)
    visited = {start_pos}

    pos = start_pos
    direction = start_dir

    while True:
        # Calculate next position
        next_pos = (pos[0] + direction.value[0], pos[1] + direction.value[1])

        # Check if guard would move out of bounds
        if not is_valid_position(grid, next_pos):
            break

        # Check if there's an obstacle ahead
        if grid[next_pos[1]][next_pos[0]] == "#":
            direction = direction.turn_right()
            continue

        # Move to next position
        pos = next_pos
        visited.add(pos)

    return len(visited)


def simulate_path(
    grid: List[List[str]], start_pos: Tuple[int, int], start_dir: Direction
) -> Set[Tuple[int, int]]:
    visited = {start_pos}
    pos = start_pos
    direction = start_dir
    path = [(pos, direction)]

    while True:
        next_pos = (pos[0] + direction.value[0], pos[1] + direction.value[1])

        if not is_valid_position(grid, next_pos):
            return visited

        if grid[next_pos[1]][next_pos[0]] == "#":
            direction = direction.turn_right()
            current_state = (pos, direction)
            if current_state in path:
                return visited
            path.append(current_state)
            continue

        pos = next_pos
        visited.add(pos)
        current_state = (pos, direction)
        if current_state in path:
            return visited
        path.append(current_state)

    return visited


def part2(data: str) -> int:
    grid, start_pos, start_dir = parse_map(data)
    valid_positions = 0

    # Try placing an obstacle at each position
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            # Skip if position is already occupied or is start position
            if grid[y][x] == "#" or (x, y) == start_pos:
                continue

            # Create a copy of the grid with new obstacle
            test_grid = copy.deepcopy(grid)
            test_grid[y][x] = "#"

            # Simulate guard movement
            visited = simulate_path(test_grid, start_pos, start_dir)

            # If visited positions are finite (guard got stuck in a loop)
            if visited and len(visited) < len(grid) * len(grid[0]):
                valid_positions += 1

    return valid_positions


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
