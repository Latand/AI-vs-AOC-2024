from collections import deque

moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def is_valid(x, y, grid_size):
    return 0 <= x < grid_size and 0 <= y < grid_size


def bfs(start, end, corrupted, grid_size):
    queue = deque([start])
    visited = set([start])
    steps = 0
    while queue:
        for _ in range(len(queue)):
            x, y = queue.popleft()
            if (x, y) == end:
                return steps
            for dx, dy in moves:
                nx, ny = x + dx, y + dy
                if (
                    is_valid(nx, ny, grid_size)
                    and (nx, ny) not in corrupted
                    and (nx, ny) not in visited
                ):
                    visited.add((nx, ny))
                    queue.append((nx, ny))
        steps += 1
    return -1  # no path found


def read_input():
    with open("../input.txt") as f:
        lines = f.read().strip().splitlines()
    byte_positions = []
    for line in lines:
        x, y = map(int, line.strip().split(","))
        byte_positions.append((x, y))
    return byte_positions


def part1(byte_positions, grid_size=71):
    corrupted = set(byte_positions[:1024])
    steps = bfs((0, 0), (grid_size - 1, grid_size - 1), corrupted, grid_size)
    return steps


def part2(byte_positions, grid_size=71):
    corrupted = set()
    for pos in byte_positions:
        corrupted.add(pos)
        if bfs((0, 0), (grid_size - 1, grid_size - 1), corrupted, grid_size) == -1:
            return pos
    return None


def main():
    byte_positions = read_input()
    # Part one
    steps = part1(byte_positions)
    print(f"Part 1: {steps}")
    # Part two
    blocking_byte = part2(byte_positions)
    if blocking_byte:
        print(f"Part 2: {blocking_byte[0]},{blocking_byte[1]}")
    else:
        print("Part 2: No byte blocks the path")


if __name__ == "__main__":
    main()
