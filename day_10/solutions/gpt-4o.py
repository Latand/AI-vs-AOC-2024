def read_input():
    with open("input.txt") as f:
        return f.read().strip()


def parse_map(data):
    """Convert input data into a 2D list of integers."""
    return [[int(char) for char in line] for line in data.splitlines()]


def find_trailheads(height_map):
    """Identify all trailhead positions (positions with height 0)."""
    trailheads = []
    for row in range(len(height_map)):
        for col in range(len(height_map[0])):
            if height_map[row][col] == 0:
                trailheads.append((row, col))
    return trailheads


def is_valid_position(row, col, height_map):
    """Check if a position is within bounds of the height map."""
    return 0 <= row < len(height_map) and 0 <= col < len(height_map[0])


def find_trails_from_trailhead(trailhead, height_map):
    """Find all valid hiking trails starting from a given trailhead."""
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    trails = set()

    def dfs(path):
        current_row, current_col = path[-1]
        current_height = height_map[current_row][current_col]

        # If we reached height 9, add the trail to the set
        if current_height == 9:
            trails.add(tuple(path))
            return

        for dr, dc in directions:
            next_row, next_col = current_row + dr, current_col + dc
            if is_valid_position(next_row, next_col, height_map):
                next_height = height_map[next_row][next_col]
                if next_height == current_height + 1:
                    dfs(path + [(next_row, next_col)])

    dfs([trailhead])
    return trails


def calculate_score(trailhead, height_map):
    """Calculate the score of a trailhead (number of reachable 9s)."""
    trails = find_trails_from_trailhead(trailhead, height_map)
    reachable_nines = set(
        (path[-1][0], path[-1][1])
        for path in trails
        if height_map[path[-1][0]][path[-1][1]] == 9
    )
    return len(reachable_nines)


def calculate_rating(trailhead, height_map):
    """Calculate the rating of a trailhead (number of distinct trails)."""
    trails = find_trails_from_trailhead(trailhead, height_map)
    return len(trails)


def part1(data):
    """Solve part 1 of the puzzle."""
    height_map = parse_map(data)
    trailheads = find_trailheads(height_map)
    return sum(calculate_score(trailhead, height_map) for trailhead in trailheads)


def part2(data):
    """Solve part 2 of the puzzle."""
    height_map = parse_map(data)
    trailheads = find_trailheads(height_map)
    return sum(calculate_rating(trailhead, height_map) for trailhead in trailheads)


if __name__ == "__main__":
    data = read_input()

    print("Part 1:", part1(data))
    print("Part 2:", part2(data))
