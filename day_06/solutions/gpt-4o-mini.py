def read_input():
    with open("../input.txt") as f:
        return f.read().strip().splitlines()


# Directions: up, right, down, left
DIRECTIONS = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
]  # delta row, delta col for up, right, down, left


def turn_right(direction):
    return (direction + 1) % 4


def move_guard(grid, start_pos, start_dir):
    visited = set()
    x, y = start_pos
    dir = start_dir
    visited.add((x, y))

    while True:
        # Check if the guard moves outside the grid
        if not (0 <= x < len(grid) and 0 <= y < len(grid[0])):
            break

        if grid[x][y] == "#":  # If there's an obstacle, turn right
            dir = turn_right(dir)
        else:  # Otherwise, move forward in the current direction
            x += DIRECTIONS[dir][0]
            y += DIRECTIONS[dir][1]
            visited.add((x, y))

    return visited


def part1(grid):
    # Find initial position and direction of the guard
    start_pos = None
    start_dir = None
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "^":
                start_pos = (i, j)
                start_dir = 0  # up
            elif grid[i][j] == ">":
                start_pos = (i, j)
                start_dir = 1  # right
            elif grid[i][j] == "v":
                start_pos = (i, j)
                start_dir = 2  # down
            elif grid[i][j] == "<":
                start_pos = (i, j)
                start_dir = 3  # left
            if start_pos:
                break

    # Run the guard movement simulation
    visited = move_guard(grid, start_pos, start_dir)
    return len(visited)


def part2(grid):
    # For part 2, we need to check all positions where a new obstruction can be placed
    possible_positions = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == ".":
                # Try placing an obstruction at (i, j)
                new_grid = [list(row) for row in grid]
                new_grid[i][j] = "#"
                # Now simulate the guard's movement and check if it gets stuck in a loop
                start_pos = None
                start_dir = None
                for x in range(len(grid)):
                    for y in range(len(grid[x])):
                        if grid[x][y] == "^":
                            start_pos = (x, y)
                            start_dir = 0
                        elif grid[x][y] == ">":
                            start_pos = (x, y)
                            start_dir = 1
                        elif grid[x][y] == "v":
                            start_pos = (x, y)
                            start_dir = 2
                        elif grid[x][y] == "<":
                            start_pos = (x, y)
                            start_dir = 3
                        if start_pos:
                            break

                visited = move_guard(new_grid, start_pos, start_dir)
                if (i, j) in visited:
                    possible_positions += 1

    return possible_positions


def main():
    grid = read_input()

    result1 = part1(grid)
    print(f"Part 1: {result1}")

    result2 = part2(grid)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
