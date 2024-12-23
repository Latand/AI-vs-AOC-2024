from collections import deque
from typing import List, Tuple, Set, Dict
import heapq


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_grid(data: str) -> Tuple[List[List[str]], Tuple[int, int], Tuple[int, int]]:
    grid = [list(line) for line in data.splitlines()]
    start = None
    end = None

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "S":
                start = (i, j)
                grid[i][j] = "."
            elif grid[i][j] == "E":
                end = (i, j)
                grid[i][j] = "."

    return grid, start, end


def get_neighbors(
    pos: Tuple[int, int], grid: List[List[str]], allow_walls: bool = False
) -> List[Tuple[int, int]]:
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    neighbors = []
    for dy, dx in directions:
        ny, nx = pos[0] + dy, pos[1] + dx
        if (
            0 <= ny < len(grid)
            and 0 <= nx < len(grid[0])
            and (grid[ny][nx] == "." or (allow_walls and grid[ny][nx] == "#"))
        ):
            neighbors.append((ny, nx))
    return neighbors


def find_shortest_path(
    grid: List[List[str]], start: Tuple[int, int], end: Tuple[int, int]
) -> int:
    queue = [(0, start)]
    visited = {start}

    while queue:
        dist, pos = heapq.heappop(queue)
        if pos == end:
            return dist

        for next_pos in get_neighbors(pos, grid):
            if next_pos not in visited:
                visited.add(next_pos)
                heapq.heappush(queue, (dist + 1, next_pos))

    return float("inf")


def find_cheating_paths(
    grid: List[List[str]],
    start: Tuple[int, int],
    end: Tuple[int, int],
    max_cheat_duration: int,
) -> Dict[int, int]:
    base_time = find_shortest_path(grid, start, end)
    savings = {}
    height, width = len(grid), len(grid[0])

    # BFS to find all possible positions
    queue = deque([(start, 0, set())])
    visited = {(start, 0)}

    while queue:
        pos, time, path = queue.popleft()
        path = path | {pos}

        # Try starting a cheat from this position
        for cheat_start in get_neighbors(pos, grid, True):
            if grid[cheat_start[0]][cheat_start[1]] == "#":
                # BFS for cheat paths
                cheat_queue = deque([(cheat_start, 1, {cheat_start})])
                cheat_visited = {cheat_start}

                while cheat_queue:
                    cheat_pos, cheat_time, cheat_path = cheat_queue.popleft()

                    # Try ending cheat here if we're on a valid spot
                    if (
                        cheat_time <= max_cheat_duration
                        and grid[cheat_pos[0]][cheat_pos[1]] == "."
                    ):
                        # Calculate remaining distance to end
                        remaining_dist = find_shortest_path(grid, cheat_pos, end)
                        if remaining_dist != float("inf"):
                            total_time = time + cheat_time + remaining_dist
                            if total_time < base_time:
                                saved_time = base_time - total_time
                                savings[saved_time] = savings.get(saved_time, 0) + 1

                    if cheat_time < max_cheat_duration:
                        for next_pos in get_neighbors(cheat_pos, grid, True):
                            if next_pos not in cheat_path:
                                cheat_queue.append(
                                    (next_pos, cheat_time + 1, cheat_path | {next_pos})
                                )

        # Continue normal path
        for next_pos in get_neighbors(pos, grid):
            if (next_pos, time + 1) not in visited:
                visited.add((next_pos, time + 1))
                queue.append((next_pos, time + 1, path))

    return savings


def part1(data: str) -> int:
    """
    Solution for part 1
    """
    grid, start, end = parse_grid(data)
    savings = find_cheating_paths(grid, start, end, 2)
    return sum(count for time_saved, count in savings.items() if time_saved >= 100)


def part2(data: str) -> int:
    """
    Solution for part 2
    """
    grid, start, end = parse_grid(data)
    savings = find_cheating_paths(grid, start, end, 20)
    return sum(count for time_saved, count in savings.items() if time_saved >= 100)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
