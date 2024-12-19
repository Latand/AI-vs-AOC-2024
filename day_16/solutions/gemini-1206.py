import heapq


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def solve_maze(grid):
    start = None
    end = None
    rows = len(grid)
    cols = len(grid[0])
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "S":
                start = (r, c)
            elif grid[r][c] == "E":
                end = (r, c)

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # East, South, West, North
    queue = [
        (0, 0, start[0], start[1], 0, [])
    ]  # (score, turns, row, col, direction_index, path)
    visited = set()
    best_score = float("inf")
    best_paths = []

    while queue:
        score, turns, r, c, dir_index, path = heapq.heappop(queue)

        if (r, c) == end:
            if score < best_score:
                best_score = score
                best_paths = [path + [(r, c)]]
            elif score == best_score:
                best_paths.append(path + [(r, c)])
            continue

        if (r, c, dir_index) in visited and score >= visited.get(
            (r, c, dir_index), float("inf")
        ):
            continue

        visited[(r, c, dir_index)] = score

        # Move forward
        dr, dc = directions[dir_index]
        new_r, new_c = r + dr, c + dc
        if 0 <= new_r < rows and 0 <= new_c < cols and grid[new_r][new_c] != "#":
            heapq.heappush(
                queue, (score + 1, turns, new_r, new_c, dir_index, path + [(r, c)])
            )

        # Turn clockwise
        new_dir_index = (dir_index + 1) % 4
        heapq.heappush(
            queue, (score + 1000, turns + 1, r, c, new_dir_index, path + [(r, c)])
        )

        # Turn counterclockwise
        new_dir_index = (dir_index - 1) % 4
        heapq.heappush(
            queue, (score + 1000, turns + 1, r, c, new_dir_index, path + [(r, c)])
        )

    return best_score, best_paths


def part1(data: str) -> int:
    grid = data.split("\n")
    best_score, _ = solve_maze(grid)
    return best_score


def part2(data: str) -> int:
    grid = data.split("\n")
    _, best_paths = solve_maze(grid)

    tiles_in_best_paths = set()
    for path in best_paths:
        for r, c in path:
            tiles_in_best_paths.add((r, c))

    return len(tiles_in_best_paths)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
