import re


def read_input():
    with open("../input.txt") as f:
        return [line.strip() for line in f]


def count_word_occurrences(grid, word):
    """Counts occurrences of a word in all 8 possible directions."""
    rows, cols = len(grid), len(grid[0])
    word_len = len(word)
    directions = [
        (0, 1),  # Right
        (0, -1),  # Left
        (1, 0),  # Down
        (-1, 0),  # Up
        (1, 1),  # Down-Right
        (1, -1),  # Down-Left
        (-1, 1),  # Up-Right
        (-1, -1),  # Up-Left
    ]

    count = 0

    for r in range(rows):
        for c in range(cols):
            for dr, dc in directions:
                match = True
                for k in range(word_len):
                    nr, nc = r + k * dr, c + k * dc
                    if (
                        not (0 <= nr < rows and 0 <= nc < cols)
                        or grid[nr][nc] != word[k]
                    ):
                        match = False
                        break
                if match:
                    count += 1

    return count


def part1(data):
    """Counts the total number of times 'XMAS' appears in the grid."""
    return count_word_occurrences(data, "XMAS")


def count_x_mas_occurrences(grid):
    """Counts occurrences of X-MAS patterns in the grid."""
    rows, cols = len(grid), len(grid[0])
    count = 0

    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            # Check for X-MAS pattern:
            # M.S
            # .A.
            # M.S
            if (
                grid[r - 1][c - 1] == "M"
                and grid[r - 1][c + 1] == "S"
                and grid[r][c] == "A"
                and grid[r + 1][c - 1] == "M"
                and grid[r + 1][c + 1] == "S"
            ):
                count += 1

    return count


def part2(data):
    """Counts the total number of X-MAS patterns in the grid."""
    return count_x_mas_occurrences(data)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
