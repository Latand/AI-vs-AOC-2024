from typing import List, Set, Tuple
import re


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def get_all_directions() -> List[Tuple[int, int]]:
    """Returns all possible directions for word search (horizontal, vertical, diagonal)"""
    return [
        (0, 1),  # right
        (1, 0),  # down
        (1, 1),  # diagonal down-right
        (-1, 1),  # diagonal up-right
        (0, -1),  # left
        (-1, 0),  # up
        (-1, -1),  # diagonal up-left
        (1, -1),  # diagonal down-left
    ]


def find_xmas_occurrences(grid: List[str]) -> int:
    """
    Find all occurrences of 'XMAS' in the grid (part 1)
    """
    height, width = len(grid), len(grid[0])
    count = 0
    directions = get_all_directions()

    for i in range(height):
        for j in range(width):
            if grid[i][j] == "X":  # Start point found
                for dx, dy in directions:
                    # Check if word fits in this direction
                    if 0 <= i + 3 * dx < height and 0 <= j + 3 * dy < width:
                        # Check for 'MAS' after 'X'
                        if (
                            grid[i + dx][j + dy] == "M"
                            and grid[i + 2 * dx][j + 2 * dy] == "A"
                            and grid[i + 3 * dx][j + 3 * dy] == "S"
                        ):
                            count += 1

    return count


def find_xmas_pattern(grid: List[str]) -> int:
    """
    Find all X-shaped patterns of 'MAS' (part 2)
    """
    height, width = len(grid), len(grid[0])
    count = 0

    # For each cell that could be the center of an X
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            # Define the four endpoints of the X relative to center
            endpoints = [
                ((i - 1, j - 1), (i - 1, j + 1)),  # Top endpoints
                ((i + 1, j - 1), (i + 1, j + 1)),  # Bottom endpoints
            ]

            valid_patterns = 0
            # Check each possible combination of MAS patterns
            for top_left, top_right in [endpoints[0]]:
                for bottom_left, bottom_right in [endpoints[1]]:
                    # Check both directions (left-to-right and right-to-left)
                    directions = [
                        # Top-left to center to bottom-right
                        [(top_left, (i, j), bottom_right), "MAS"],
                        # Top-right to center to bottom-left
                        [(top_right, (i, j), bottom_left), "MAS"],
                    ]

                    for path, pattern in directions:
                        # Get characters along the path
                        chars = []
                        for x, y in path:
                            if 0 <= x < height and 0 <= y < width:
                                chars.append(grid[x][y])
                            else:
                                break

                        # Check if chars match pattern or its reverse
                        if len(chars) == 3:
                            word = "".join(chars)
                            if word == pattern or word == pattern[::-1]:
                                valid_patterns += 1

                    # If we found both MAS patterns forming an X
                    if valid_patterns == 2:
                        count += 1
                        break

    return count


def part1(data: str) -> int:
    """
    Solution for part 1: Find all occurrences of 'XMAS'
    """
    grid = data.strip().split("\n")
    return find_xmas_occurrences(grid)


def part2(data: str) -> int:
    """
    Solution for part 2: Find all X-shaped patterns of 'MAS'
    """
    grid = data.strip().split("\n")
    return find_xmas_pattern(grid)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
