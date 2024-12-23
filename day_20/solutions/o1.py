def read_input():
    """
    Reads the puzzle input from ../input.txt
    """
    with open("../input.txt") as f:
        return f.read().strip()


def parse_grid(data: str):
    """
    Parse the puzzle input into:
     - grid: 2D list of characters
     - start: (row, col) for 'S'
     - end: (row, col) for 'E'
    """
    lines = data.splitlines()
    grid = [list(line) for line in lines]

    start = None
    end = None

    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == "S":
                start = (r, c)
            elif val == "E":
                end = (r, c)

    return grid, start, end


def neighbors(r, c, rows, cols):
    """
    Return the 4-directionally adjacent cells (up, down, left, right).
    """
    for nr, nc in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
        if 0 <= nr < rows and 0 <= nc < cols:
            yield nr, nc


def bfs_normal(grid, start):
    """
    Standard BFS on the grid treating '.' and 'S'/'E' as walkable,
    '#' as walls. Returns a dictionary dist[(r, c)] = shortest steps from start
    for all reachable track cells.
    """
    from collections import deque

    rows = len(grid)
    cols = len(grid[0])
    dist = {}
    queue = deque()

    # Start BFS from 'start'
    dist[start] = 0
    queue.append(start)

    while queue:
        r, c = queue.popleft()
        for nr, nc in neighbors(r, c, rows, cols):
            # We only walk on non-wall cells (S, E, .)
            if grid[nr][nc] != "#" and (nr, nc) not in dist:
                dist[(nr, nc)] = dist[(r, c)] + 1
                queue.append((nr, nc))

    return dist


def bfs_ignoring_walls(grid, start, max_steps):
    """
    BFS that can pass through walls, up to 'max_steps' steps away.
    Returns a dict min_dist[(r, c)] = steps needed to reach (r, c),
    ignoring walls, from 'start'. Limited to a maximum of 'max_steps'
    to avoid huge expansions for large grids.

    We do NOT require (r, c) to be open track at intermediate steps,
    but do require that the BFS stops after max_steps expansions.
    """
    from collections import deque

    rows = len(grid)
    cols = len(grid[0])
    dist = {}
    queue = deque()

    dist[start] = 0
    queue.append(start)

    while queue:
        r, c = queue.popleft()
        current_steps = dist[(r, c)]
        if current_steps == max_steps:
            # We've reached the maximum distance we allow ignoring walls
            continue

        for nr, nc in neighbors(r, c, rows, cols):
            # We can pass through walls ignoring collisions:
            # but we only keep track up to max_steps
            if (nr, nc) not in dist:
                dist[(nr, nc)] = current_steps + 1
                queue.append((nr, nc))

    return dist


def solve_part(grid, start, end, cheat_max_length):
    """
    Returns how many cheats would save at least 100 picoseconds
    when the cheat can last up to 'cheat_max_length' steps.

    Steps to solve:
    1) BFS normally for dist_S[x], the cost from S->x (for x in track).
    2) BFS normally for dist_E[x], the cost from x->E (this we do by BFS from E).
    3) Let T = dist_S[end]. (normal cost S->E)
    4) For each track cell x, we find dist_S[x]. If x is unreachable, skip.
       For each track cell y, we see if y is reachable from x in <= cheat_max_length ignoring walls.
         - Also require that y is track so the cheat can end on normal track.
         - Then total time using this cheat is dist_S[x] + (the ignoring-wall distance x->y) + dist_E[y].
         - The saving is T - that total time.
         - If saving >= 100, we count it.
    5) Return the total count of such cheats.
    """
    from collections import defaultdict

    rows = len(grid)
    cols = len(grid[0])

    # 1) BFS normal from S
    dist_S = bfs_normal(grid, start)
    # 2) BFS normal from E (we’ll get cost from any cell x -> E)
    #    by just BFS from E and reading dist_E[x].
    dist_E = bfs_normal(grid, end)

    # Normal cost from S->E:
    T = dist_S.get(end, None)
    if T is None:
        # If E is not reachable at all, no cheat can help
        return 0

    # Collect all track cells (including S and E) for iteration
    track_cells = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "#":  # i.e. it's track, S, or E
                track_cells.append((r, c))

    # Precompute ignoring-wall BFS for each track cell to limit repeated BFS
    # However, if the grid is large, this can be big. For a small puzzle it’s okay.
    ignore_walls_map = {}
    for cell in track_cells:
        ignore_walls_map[cell] = bfs_ignoring_walls(grid, cell, cheat_max_length)

    count_100_plus = 0
    seen_cheats = set()  # To ensure we only count distinct (startPos, endPos) cheats

    for x in track_cells:
        # dist_S[x] must exist to be a valid x
        if x not in dist_S:
            continue
        cost_S_x = dist_S[x]

        # BFS ignoring walls from x
        dist_ignore = ignore_walls_map[x]

        for y in track_cells:
            # We'll only consider y if y is reachable from x in <= cheat_max_length ignoring walls
            # and y is track (which it is by construction).
            if y in dist_ignore:
                cheat_length = dist_ignore[y]
                if cheat_length <= cheat_max_length:
                    # dist_E[y] must exist for y to be valid end
                    if y in dist_E:
                        cost_y_E = dist_E[y]
                        total_time = cost_S_x + cheat_length + cost_y_E
                        saving = T - total_time
                        if saving >= 100:
                            # We identify a cheat by (x, y) as the puzzle states:
                            # "Cheats are uniquely identified by their start and end position."
                            if (x, y) not in seen_cheats:
                                seen_cheats.add((x, y))
                                count_100_plus += 1

    return count_100_plus


def part1(data: str) -> int:
    """
    Part 1: Single cheat up to 2 picoseconds.
    Count how many cheats would save >= 100 picoseconds.
    """
    grid, start, end = parse_grid(data)
    # Maximum cheat length = 2
    return solve_part(grid, start, end, cheat_max_length=2)


def part2(data: str) -> int:
    """
    Part 2: Single cheat up to 20 picoseconds.
    Count how many cheats would save >= 100 picoseconds.
    """
    grid, start, end = parse_grid(data)
    # Maximum cheat length = 20
    return solve_part(grid, start, end, cheat_max_length=20)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
