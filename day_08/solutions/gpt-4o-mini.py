def read_input():
    with open("../input.txt") as f:
        return f.read().strip().splitlines()


def find_antenna_positions(grid):
    """
    Returns a dictionary where keys are antenna frequencies and values are lists of coordinates (r, c)
    for each antenna in the grid.
    """
    antenna_positions = {}
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val.isalnum():  # only consider antennas (letters and digits)
                if val not in antenna_positions:
                    antenna_positions[val] = []
                antenna_positions[val].append((r, c))
    return antenna_positions


def calculate_antinnodes_part1(grid):
    antenna_positions = find_antenna_positions(grid)
    antinodes = set()

    for freq, positions in antenna_positions.items():
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                r1, c1 = positions[i]
                r2, c2 = positions[j]
                # Check if they are exactly twice as far apart
                if r1 == r2 and abs(c1 - c2) % 2 == 0:
                    midpoint = (r1, (c1 + c2) // 2)
                    antinodes.add(midpoint)
                elif c1 == c2 and abs(r1 - r2) % 2 == 0:
                    midpoint = ((r1 + r2) // 2, c1)
                    antinodes.add(midpoint)

    return len(antinodes)


def calculate_antinnodes_part2(grid):
    antenna_positions = find_antenna_positions(grid)
    antinodes = set()

    for freq, positions in antenna_positions.items():
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                r1, c1 = positions[i]
                r2, c2 = positions[j]

                # Antinodes are at all in-line points, including antennas themselves
                if r1 == r2:  # Horizontal line
                    for col in range(min(c1, c2), max(c1, c2) + 1):
                        antinodes.add((r1, col))
                elif c1 == c2:  # Vertical line
                    for row in range(min(r1, r2), max(r1, r2) + 1):
                        antinodes.add((row, c1))

        # Add all positions of antennas as they are antinodes in part 2
        for r, c in positions:
            antinodes.add((r, c))

    return len(antinodes)


def part1(data: str) -> int:
    return calculate_antinnodes_part1(data)


def part2(data: str) -> int:
    return calculate_antinnodes_part2(data)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
