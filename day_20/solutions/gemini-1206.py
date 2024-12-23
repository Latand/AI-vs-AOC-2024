from collections import deque


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_map(data: str):
    grid = data.splitlines()
    start = None
    end = None
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == "S":
                start = (r, c)
            elif cell == "E":
                end = (r, c)
    return grid, start, end


def bfs(grid, start, end):
    queue = deque([(start, 0)])
    visited = {start}
    while queue:
        (r, c), dist = queue.popleft()
        if (r, c) == end:
            return dist
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if (
                0 <= nr < len(grid)
                and 0 <= nc < len(grid[0])
                and grid[nr][nc] != "#"
                and (nr, nc) not in visited
            ):
                visited.add((nr, nc))
                queue.append(((nr, nc), dist + 1))
    return -1


def solve(data: str, max_cheat_time: int, min_save_time: int) -> int:
    grid, start, end = parse_map(data)
    shortest_path = bfs(grid, start, end)

    cheats = {}
    for sr in range(len(grid)):
        for sc in range(len(grid[0])):
            if grid[sr][sc] != "#":
                for er in range(len(grid)):
                    for ec in range(len(grid[0])):
                        if grid[er][ec] != "#":
                            original_dist = bfs(grid, (sr, sc), (er, ec))

                            if original_dist == -1:
                                continue

                            queue = deque([((sr, sc), 0, [])])
                            visited = {((sr, sc), 0)}

                            while queue:
                                (cr, cc), cheat_time, path = queue.popleft()

                                if (cr, cc) == (
                                    er,
                                    ec,
                                ) and cheat_time <= max_cheat_time:
                                    path_len = len(path) if len(path) > 0 else 0

                                    saved_time = original_dist - path_len

                                    if saved_time > 0:
                                        if (
                                            sr,
                                            sc,
                                            er,
                                            ec,
                                        ) not in cheats or saved_time > cheats[
                                            (sr, sc, er, ec)
                                        ]:
                                            cheats[(sr, sc, er, ec)] = saved_time
                                    break

                                if cheat_time >= max_cheat_time:
                                    continue

                                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                                    nr, nc = cr + dr, cc + dc

                                    if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                                        new_cheat_time = cheat_time

                                        if grid[nr][nc] == "#":
                                            new_cheat_time += 1
                                        else:
                                            new_cheat_time = (
                                                cheat_time + 1
                                                if grid[nr][nc] == "#"
                                                else cheat_time
                                            )

                                        if (
                                            new_cheat_time <= max_cheat_time
                                            and ((nr, nc), new_cheat_time)
                                            not in visited
                                        ):
                                            visited.add(((nr, nc), new_cheat_time))
                                            new_path = (
                                                path + [(nr, nc)]
                                                if grid[nr][nc] == "#"
                                                else path
                                            )

                                            queue.append(
                                                ((nr, nc), new_cheat_time, new_path)
                                            )

    count = 0
    for saved_time in cheats.values():
        path_before = bfs(
            grid,
            start,
            (
                list(cheats.keys())[list(cheats.values()).index(saved_time)][0],
                list(cheats.keys())[list(cheats.values()).index(saved_time)][1],
            ),
        )
        path_after = bfs(
            grid,
            (
                list(cheats.keys())[list(cheats.values()).index(saved_time)][2],
                list(cheats.keys())[list(cheats.values()).index(saved_time)][3],
            ),
            end,
        )
        if (
            shortest_path - path_before - path_after - (original_dist - saved_time) > 0
            and saved_time >= min_save_time
        ):
            count += 1
    return count


def part1(data: str) -> int:
    return solve(data, 2, 0)


def part2(data: str) -> int:
    return solve(data, 20, 100)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
