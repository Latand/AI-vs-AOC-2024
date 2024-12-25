import re


def read_input():
    with open("../input.txt") as f:
        return [line.strip() for line in f.readlines()]


def part1(data: list) -> int:
    """
    Counts the number of times the word "XMAS" appears in the grid.
    The word can be horizontal, vertical, diagonal, forwards, or backwards.
    """
    word = "XMAS"
    word_length = len(word)
    count = 0
    rows = len(data)
    cols = len(data[0]) if rows > 0 else 0

    # Define all 8 possible directions: (dx, dy)
    directions = [
        (-1, -1),  # Up-Left
        (-1, 0),  # Up
        (-1, 1),  # Up-Right
        (0, -1),  # Left
        (0, 1),  # Right
        (1, -1),  # Down-Left
        (1, 0),  # Down
        (1, 1),  # Down-Right
    ]

    for i in range(rows):
        for j in range(cols):
            for dx, dy in directions:
                # Extract the word in the current direction
                temp = []
                x, y = i, j
                for k in range(word_length):
                    if 0 <= x < rows and 0 <= y < cols:
                        temp.append(data[x][y])
                        x += dx
                        y += dy
                    else:
                        break
                if "".join(temp) == word:
                    count += 1

    return count


def part2(data: list) -> int:
    """
    Counts the number of times an X-MAS appears in the grid.
    An X-MAS is defined as two "MAS" sequences in the shape of an X.
    Each "MAS" can be forwards or backwards.
    """
    count = 0
    rows = len(data)
    cols = len(data[0]) if rows > 0 else 0

    # Define the relative positions for a 3x3 X pattern
    for i in range(rows - 2):
        for j in range(cols - 2):
            # Extract the two diagonals
            diag1 = data[i][j] + data[i + 1][j + 1] + data[i + 2][j + 2]
            diag2 = data[i][j + 2] + data[i + 1][j + 1] + data[i + 2][j]

            # Check if both diagonals are "MAS" or "SAM"
            if (diag1 == "MAS" or diag1 == "SAM") and (
                diag2 == "MAS" or diag2 == "SAM"
            ):
                count += 1

    return count


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
