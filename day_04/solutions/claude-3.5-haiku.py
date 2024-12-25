def read_input():
    with open("../input.txt") as f:
        return f.read().strip().split("\n")


def find_xmas_pattern(grid):
    """
    Find all occurrences of the XMAS pattern in all possible directions.
    """
    rows, cols = len(grid), len(grid[0])
    xmas_count = 0

    # All possible search directions: horizontal, vertical, diagonal
    directions = [
        (0, 1),  # right
        (1, 0),  # down
        (1, 1),  # diagonal down-right
        (1, -1),  # diagonal down-left
        (0, -1),  # left
        (-1, 0),  # up
        (-1, -1),  # diagonal up-left
        (-1, 1),  # diagonal up-right
    ]

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def check_xmas(r, c, dr, dc):
        """
        Check if XMAS can be formed starting from (r,c) in direction (dr,dc)
        """
        xmas_letters = "XMAS"
        for i, letter in enumerate(xmas_letters):
            nr, nc = r + i * dr, c + i * dc
            if not is_valid(nr, nc) or grid[nr][nc] != letter:
                return False
        return True

    # Iterate through all possible starting positions
    for r in range(rows):
        for c in range(cols):
            for dr, dc in directions:
                if check_xmas(r, c, dr, dc):
                    xmas_count += 1

    return xmas_count


def find_x_mas_pattern(grid):
    """
    Find all occurrences of the X-MAS pattern.
    """
    rows, cols = len(grid), len(grid[0])
    x_mas_count = 0

    # Check only the specific X-MAS structure
    for r in range(rows - 2):
        for c in range(cols - 2):
            # Check if we have an X-MAS pattern
            pattern_check = (
                (grid[r][c] == "M")
                and (grid[r][c + 2] == "S")
                and (grid[r + 1][c + 1] == "A")
                and (grid[r + 2][c] == "M")
                and (grid[r + 2][c + 2] == "S")
            )

            # Check the reverse pattern as well
            reverse_pattern_check = (
                (grid[r][c] == "S")
                and (grid[r][c + 2] == "M")
                and (grid[r + 1][c + 1] == "A")
                and (grid[r + 2][c] == "S")
                and (grid[r + 2][c + 2] == "M")
            )

            if pattern_check or reverse_pattern_check:
                x_mas_count += 1

    return x_mas_count


def part1(data: list[str]) -> int:
    """
    Solution for part 1: Find all XMAS patterns
    """
    return find_xmas_pattern(data)


def part2(data: list[str]) -> int:
    """
    Solution for part 2: Find X-MAS patterns
    """
    return find_x_mas_pattern(data)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
