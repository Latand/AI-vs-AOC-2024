def read_input():
    with open("input.txt") as f:
        return f.read().strip()


def part1(data: str) -> int:
    """Solve part 1 of the puzzle."""
    grid = [[int(c) for c in line] for line in data.splitlines()]
    rows, cols = len(grid), len(grid[0])
    trailheads = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                trailheads.append((r, c))

    total_score = 0
    for start_r, start_c in trailheads:
        score = 0
        q = [(start_r, start_c, 0)]
        visited = set()
        while q:
            r, c, h = q.pop(0)
            if (r, c) in visited:
                continue
            visited.add((r, c))

            if h == 9:
                score += 1
                continue

            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == h + 1:
                    q.append((nr, nc, h + 1))
        total_score += score

    return total_score


def part2(data: str) -> int:
    """Solve part 2 of the puzzle."""
    grid = [[int(c) for c in line] for line in data.splitlines()]
    rows, cols = len(grid), len(grid[0])
    trailheads = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                trailheads.append((r, c))

    total_rating = 0
    for start_r, start_c in trailheads:
        rating = 0
        q = [([(start_r, start_c)], 0)]

        while q:
            path, h = q.pop(0)
            r, c = path[-1]

            if h == 9:
                rating += 1
                continue

            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == h + 1:
                    q.append((path + [(nr, nc)], h + 1))
        total_rating += rating

    return total_rating


if __name__ == "__main__":
    data = read_input()

    print("Part 1:", part1(data))
    print("Part 2:", part2(data))
