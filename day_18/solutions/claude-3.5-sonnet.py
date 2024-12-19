from collections import deque
from typing import List, Tuple, Set


def read_input():
    with open("../input.txt") as f:
        return [tuple(map(int, line.strip().split(","))) for line in f]


def get_neighbors(x: int, y: int, max_x: int, max_y: int) -> List[Tuple[int, int]]:
    """Return valid neighboring coordinates."""
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    neighbors = []
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x <= max_x and 0 <= new_y <= max_y:
            neighbors.append((new_x, new_y))
    return neighbors


def find_shortest_path(rocks: Set[Tuple[int, int]], max_x: int, max_y: int) -> int:
    """Find shortest path from (0,0) to (max_x,max_y) avoiding rocks using BFS."""
    if (0, 0) in rocks or (max_x, max_y) in rocks:
        return -1

    queue = deque([(0, 0, 0)])  # (x, y, steps)
    visited = {(0, 0)}

    while queue:
        x, y, steps = queue.popleft()

        if x == max_x and y == max_y:
            return steps

        for next_x, next_y in get_neighbors(x, y, max_x, max_y):
            if (next_x, next_y) not in visited and (next_x, next_y) not in rocks:
                visited.add((next_x, next_y))
                queue.append((next_x, next_y, steps + 1))

    return -1


def can_reach_exit(
    start: Tuple[int, int], rocks: Set[Tuple[int, int]], max_x: int, max_y: int
) -> bool:
    """Check if there exists any path from start to (max_x,max_y)."""
    queue = deque([start])
    visited = {start}

    while queue:
        x, y = queue.popleft()

        if x == max_x and y == max_y:
            return True

        for next_x, next_y in get_neighbors(x, y, max_x, max_y):
            if (next_x, next_y) not in visited and (next_x, next_y) not in rocks:
                visited.add((next_x, next_y))
                queue.append((next_x, next_y))

    return False


def part1(data: List[Tuple[int, int]]) -> int:
    """
    Find shortest path length after first 1024 bytes have fallen.
    """
    rocks = set(data[:1024])  # Take first 1024 bytes
    max_coord = 70  # As specified in the problem
    return find_shortest_path(rocks, max_coord, max_coord)


def part2(data: List[Tuple[int, int]]) -> str:
    """
    Find coordinates of first byte that blocks path to exit.
    """
    max_coord = 70
    rocks = set()

    for i, (x, y) in enumerate(data):
        rocks.add((x, y))
        # Only check if we can reach exit if this rock could potentially block the path
        if not can_reach_exit((0, 0), rocks, max_coord, max_coord):
            return f"{x},{y}"

    return "No solution found"


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
