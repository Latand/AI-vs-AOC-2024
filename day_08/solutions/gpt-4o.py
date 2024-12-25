import re
from collections import defaultdict
from itertools import combinations


def read_input():
    with open("../input.txt") as f:
        return f.read().strip().splitlines()


def parse_map(grid):
    """Parse the input map and extract antenna positions and frequencies."""
    antennas = []
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char != ".":
                antennas.append((x, y, char))
    return antennas


def calculate_antinodes_part1(antennas, width, height):
    """Calculate antinodes for part 1 based on distance criteria."""
    antinodes = set()
    frequency_groups = defaultdict(list)

    # Group antennas by frequency
    for x, y, freq in antennas:
        frequency_groups[freq].append((x, y))

    # Check pairs of antennas for each frequency
    for freq, points in frequency_groups.items():
        for (x1, y1), (x2, y2) in combinations(points, 2):
            dx, dy = x2 - x1, y2 - y1

            # Check the distance condition for antinodes
            if abs(dx) % 2 == 0 and abs(dy) % 2 == 0:
                mx, my = dx // 2, dy // 2
                antinode1 = (x1 - mx, y1 - my)
                antinode2 = (x2 + mx, y2 + my)

                # Ensure antinodes are within bounds
                if 0 <= antinode1[0] < width and 0 <= antinode1[1] < height:
                    antinodes.add(antinode1)
                if 0 <= antinode2[0] < width and 0 <= antinode2[1] < height:
                    antinodes.add(antinode2)

    return antinodes


def calculate_antinodes_part2(antennas, width, height):
    """Calculate antinodes for part 2 including all alignments."""
    antinodes = set()
    frequency_groups = defaultdict(list)

    # Group antennas by frequency
    for x, y, freq in antennas:
        frequency_groups[freq].append((x, y))

    # Check all pairs of antennas for each frequency
    for freq, points in frequency_groups.items():
        for (x1, y1), (x2, y2) in combinations(points, 2):
            dx, dy = x2 - x1, y2 - y1
            gcd = abs(dx) if dy == 0 else abs(dy)

            # Normalize the direction vector
            step_x, step_y = dx // gcd, dy // gcd

            # Add all points in line between the two antennas
            x, y = x1, y1
            while 0 <= x < width and 0 <= y < height:
                antinodes.add((x, y))
                x += step_x
                y += step_y

        # Include antennas themselves if they align with at least two others
        if len(points) > 1:
            antinodes.update(points)

    return antinodes


def main():
    grid = read_input()
    width, height = len(grid[0]), len(grid)
    antennas = parse_map(grid)

    # Part 1
    part1_antinodes = calculate_antinodes_part1(antennas, width, height)
    print(f"Part 1: {len(part1_antinodes)}")

    # Part 2
    part2_antinodes = calculate_antinodes_part2(antennas, width, height)
    print(f"Part 2: {len(part2_antinodes)}")


if __name__ == "__main__":
    main()
