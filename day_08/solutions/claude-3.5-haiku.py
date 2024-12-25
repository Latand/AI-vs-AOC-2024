from typing import List, Tuple, Set
import itertools


def read_input() -> List[str]:
    """
    Read input from the file
    """
    with open("../input.txt", "r") as f:
        return f.read().splitlines()


def parse_map(grid: List[str]) -> Tuple[dict, dict]:
    """
    Parse the grid and return dictionaries of antenna locations by frequency
    """
    antennas_by_freq = {}
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char != ".":
                if char not in antennas_by_freq:
                    antennas_by_freq[char] = []
                antennas_by_freq[char].append((x, y))

    return antennas_by_freq


def find_antinodes_v1(antennas_by_freq: dict) -> Set[Tuple[int, int]]:
    """
    Find antinodes based on Part 1 rules (one antenna is twice as far as the other)
    """
    antinodes = set()

    for freq, freq_antennas in antennas_by_freq.items():
        # Check all pairs of antennas with the same frequency
        for (x1, y1), (x2, y2) in itertools.combinations(freq_antennas, 2):
            # Calculate vector between antennas
            dx = x2 - x1
            dy = y2 - y1

            # Check both sides of the line
            for side in [-1, 1]:
                # Extrapolate to find antinode
                antinode_x = x2 + side * dx
                antinode_y = y2 + side * dy

                antinodes.add((antinode_x, antinode_y))

    return antinodes


def find_antinodes_v2(antennas_by_freq: dict) -> Set[Tuple[int, int]]:
    """
    Find antinodes based on Part 2 rules (in line with at least two antennas)
    """
    antinodes = set()

    for freq, freq_antennas in antennas_by_freq.items():
        # Check all triples of antennas with the same frequency
        for (x1, y1), (x2, y2), *rest in itertools.combinations(freq_antennas, 3):
            # Check if antennas are collinear
            if (
                (x1 == x2 and x1 == rest[0][0])
                or (y1 == y2 and y1 == rest[0][1])
                or ((x2 - x1) * (rest[0][1] - y1) == (rest[0][0] - x1) * (y2 - y1))
            ):
                # Mark all the original antennas as antinodes
                antinodes.add((x1, y1))
                antinodes.add((x2, y2))
                antinodes.add(rest[0])

    return antinodes


def part1(grid: List[str]) -> int:
    """
    Solution for part 1
    """
    antennas_by_freq = parse_map(grid)
    antinodes = find_antinodes_v1(antennas_by_freq)
    return len(antinodes)


def part2(grid: List[str]) -> int:
    """
    Solution for part 2
    """
    antennas_by_freq = parse_map(grid)
    antinodes = find_antinodes_v2(antennas_by_freq)
    return len(antinodes)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
