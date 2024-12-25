import sys
from collections import defaultdict


def read_input():
    """
    Reads the puzzle input from ../input.txt
    """
    with open("../input.txt") as f:
        return f.read().splitlines()


# Directions in order: Up, Right, Down, Left
# We'll represent these as (drow, dcol)
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def turn_right(direction_index: int) -> int:
    """
    Turns the direction index 90 degrees to the right.
    direction_index cycles 0->1->2->3->0
    """
    return (direction_index + 1) % 4


def simulate(grid, start_row, start_col, start_dir):
    """
    Simulate the guard's movement through the grid.
    Returns:
      visited_positions: set of (row, col) visited
      left_map: bool, True if guard eventually leaves the map, False if guard loops

    The guard follows these rules:
      1) If there is an obstacle (#) directly in front, turn right 90 deg
      2) Otherwise, move forward one cell
    Continue until leaving the map or repeating a state (loop).

    We'll detect a loop if we re-visit the same (row, col, direction_index).
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    visited_positions = set()
    visited_states = set()  # (row, col, direction_index)

    row, col = start_row, start_col
    direction_index = start_dir

    while True:
        # If we have left the map, end
        if row < 0 or row >= rows or col < 0 or col >= cols:
            return visited_positions, True  # True => left map

        # If we are in a repeated state, this is a loop
        state = (row, col, direction_index)
        if state in visited_states:
            return visited_positions, False  # False => did not leave, but looped
        visited_states.add(state)

        # Mark the current position visited
        visited_positions.add((row, col))

        # Check what's in front of the guard
        drow, dcol = DIRECTIONS[direction_index]
        forward_r = row + drow
        forward_c = col + dcol

        # If forward is out-of-bounds or an obstacle, turn right
        if not (0 <= forward_r < rows and 0 <= forward_c < cols):
            direction_index = turn_right(direction_index)
        elif grid[forward_r][forward_c] == "#":
            direction_index = turn_right(direction_index)
        else:
            # Move forward
            row, col = forward_r, forward_c


def part1(data: list) -> int:
    """
    Part 1:
    Predict the path of the guard using the given patrol rules.
    Return the number of distinct positions visited (including the starting position)
    before leaving the mapped area.
    """
    # Parse the input into a grid
    grid = [list(line) for line in data]

    # Find the guard's starting position and direction
    start_row, start_col, start_dir = None, None, None
    # We'll map '^','>','v','<' to direction indices 0,1,2,3
    char_to_dir = {"^": 0, ">": 1, "v": 2, "<": 3}

    for r, row_data in enumerate(grid):
        for c, val in enumerate(row_data):
            if val in char_to_dir:
                start_row, start_col = r, c
                start_dir = char_to_dir[val]
                # Replace the guard's symbol with '.' so we treat it as open space
                grid[r][c] = "."
                break
        if start_row is not None:
            break

    visited_positions, left_map = simulate(grid, start_row, start_col, start_dir)
    # Part 1 wants the count of distinct positions before leaving
    return len(visited_positions)


def part2(data: list) -> int:
    """
    Part 2:
    We want to place one new obstruction (#) in a position (which is not the guard's
    start position) such that the guard gets stuck in a loop and never leaves the map.

    Return the number of such positions.
    """
    # Parse the input into a grid
    grid = [list(line) for line in data]

    # Find the guard's starting position and direction
    start_row, start_col, start_dir = None, None, None
    char_to_dir = {"^": 0, ">": 1, "v": 2, "<": 3}

    for r, row_data in enumerate(grid):
        for c, val in enumerate(row_data):
            if val in char_to_dir:
                start_row, start_col = r, c
                start_dir = char_to_dir[val]
                # Replace the guard's symbol with '.' so we treat it as open space
                grid[r][c] = "."
                break
        if start_row is not None:
            break

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    possible_obstructions = 0

    # We'll test placing an obstacle in each valid '.' cell (except guard's start)
    for r in range(rows):
        for c in range(cols):
            if (r, c) == (start_row, start_col):
                # Can't place the new obstruction at guard's initial position
                continue
            if grid[r][c] == ".":
                # Place a temporary obstacle
                grid[r][c] = "#"

                visited_positions, left_map = simulate(
                    grid, start_row, start_col, start_dir
                )
                # If left_map == False => that means we looped
                if not left_map:
                    possible_obstructions += 1

                # Remove the obstacle
                grid[r][c] = "."

    return possible_obstructions


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    # Increase recursion limit just in case of large grids and deeper calls
    sys.setrecursionlimit(10**7)
    main()
