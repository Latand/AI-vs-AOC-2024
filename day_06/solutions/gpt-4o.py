def read_input():
    with open("../input.txt") as f:
        return [list(line.strip()) for line in f.readlines()]


def find_starting_position_and_direction(grid):
    directions = {"^": (0, -1), ">": (1, 0), "v": (0, 1), "<": (-1, 0)}
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell in directions:
                return (x, y), directions[cell]


def turn_right(direction):
    dx, dy = direction
    return -dy, dx


def simulate_patrol(grid):
    start_pos, direction = find_starting_position_and_direction(grid)
    visited = set()
    x, y = start_pos

    visited.add((x, y))

    while 0 <= y < len(grid) and 0 <= x < len(grid[0]):
        nx, ny = x + direction[0], y + direction[1]

        if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and grid[ny][nx] != "#":
            x, y = nx, ny
        else:
            direction = turn_right(direction)

        visited.add((x, y))

    return visited


def find_loop_obstruction_positions(grid, visited_positions):
    start_pos, direction = find_starting_position_and_direction(grid)
    obstruction_positions = set()

    x, y = start_pos
    patrol_positions = {}
    step_count = 0

    while 0 <= y < len(grid) and 0 <= x < len(grid[0]):
        if (x, y) in patrol_positions:
            loop_start = patrol_positions[(x, y)]
            loop_positions = set(
                pos for pos, step in patrol_positions.items() if step >= loop_start
            )

            for lx, ly in loop_positions:
                if (lx, ly) not in visited_positions:
                    obstruction_positions.add((lx, ly))

            break

        patrol_positions[(x, y)] = step_count
        step_count += 1

        nx, ny = x + direction[0], y + direction[1]

        if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and grid[ny][nx] != "#":
            x, y = nx, ny
        else:
            direction = turn_right(direction)

    return obstruction_positions


def part1(grid):
    visited_positions = simulate_patrol(grid)
    return len(visited_positions)


def part2(grid):
    visited_positions = simulate_patrol(grid)
    obstruction_positions = find_loop_obstruction_positions(grid, visited_positions)
    return len(obstruction_positions)


def main():
    grid = read_input()

    result1 = part1(grid)
    print(f"Part 1: {result1}")

    result2 = part2(grid)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
