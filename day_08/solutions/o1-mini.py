import re
from typing import List, Tuple, Dict, Set


def read_input() -> List[str]:
    with open("../input.txt") as f:
        return [line.rstrip("\n") for line in f]


def parse_grid(grid: List[str]) -> Tuple[int, int, Dict[str, List[Tuple[int, int]]]]:
    """
    Parses the grid and returns the number of rows, number of columns,
    and a dictionary mapping frequencies to their antenna positions.
    """
    rows = len(grid)
    cols = max(len(line) for line in grid) if grid else 0
    freq_map: Dict[str, List[Tuple[int, int]]] = {}

    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            if char != ".":
                freq_map.setdefault(char, []).append((x, y))

    return rows, cols, freq_map


def get_map_bounds(grid: List[str]) -> Tuple[int, int]:
    """
    Returns the number of rows and columns in the grid.
    """
    rows = len(grid)
    cols = max(len(line) for line in grid) if grid else 0
    return rows, cols


def part1(data: str) -> int:
    grid = data.splitlines()
    rows, cols, freq_map = parse_grid(grid)
    antinodes: Set[Tuple[int, int]] = set()

    for freq, antennas in freq_map.items():
        if len(antennas) < 2:
            continue
        n = len(antennas)
        for i in range(n):
            for j in range(i + 1, n):
                ax, ay = antennas[i]
                bx, by = antennas[j]

                # Calculate antinode positions
                # C = 2*B - A
                cx = 2 * bx - ax
                cy = 2 * by - ay
                # D = 2*A - B
                dx = 2 * ax - bx
                dy = 2 * ay - by

                # Check if within bounds
                if 0 <= cx < cols and 0 <= cy < rows:
                    antinodes.add((cx, cy))
                if 0 <= dx < cols and 0 <= dy < rows:
                    antinodes.add((dx, dy))

    return len(antinodes)


def get_all_lines(
    freq_antennas: List[Tuple[int, int]], rows: int, cols: int
) -> Set[Tuple[int, int]]:
    """
    Given a list of antenna positions, returns all grid positions that lie on any line
    defined by at least two antennas.
    """
    lines_positions: Set[Tuple[int, int]] = set()
    n = len(freq_antennas)

    for i in range(n):
        for j in range(i + 1, n):
            (x1, y1) = freq_antennas[i]
            (x2, y2) = freq_antennas[j]

            dx = x2 - x1
            dy = y2 - y1

            if dx == 0 and dy == 0:
                continue  # Same point, skip

            # Find all points on the line defined by (x1, y1) and (x2, y2)
            # We use the equation (y - y1)*dx = (x - x1)*dy
            # Iterate through all grid positions and check if they satisfy the equation
            for y in range(rows):
                for x in range(cols):
                    if (y - y1) * dx == (x - x1) * dy:
                        lines_positions.add((x, y))

    return lines_positions


def part2(data: str) -> int:
    grid = data.splitlines()
    rows, cols, freq_map = parse_grid(grid)
    antinodes: Set[Tuple[int, int]] = set()

    for freq, antennas in freq_map.items():
        if len(antennas) < 2:
            continue
        # Get all positions that lie on any line defined by two antennas of this frequency
        lines_positions = get_all_lines(antennas, rows, cols)
        antinodes.update(lines_positions)

    return len(antinodes)


def main():
    data = read_input()
    result1 = part1("\n".join(data))
    print(f"Part 1: {result1}")

    result2 = part2("\n".join(data))
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
