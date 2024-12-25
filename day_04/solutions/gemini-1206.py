import re


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def count_xmas(grid):
    count = 0
    rows = len(grid)
    cols = len(grid[0])

    # Check horizontal
    for row in grid:
        count += "".join(row).count("XMAS")
        count += "".join(row)[::-1].count("XMAS")

    # Check vertical
    for j in range(cols):
        col_str = "".join(grid[i][j] for i in range(rows))
        count += col_str.count("XMAS")
        count += col_str[::-1].count("XMAS")

    # Check diagonals
    for i in range(rows):
        for j in range(cols):
            # Top-left to bottom-right
            diag_str = ""
            row, col = i, j
            while row < rows and col < cols:
                diag_str += grid[row][col]
                row += 1
                col += 1
            count += diag_str.count("XMAS")
            count += diag_str[::-1].count("XMAS")

            # Top-right to bottom-left
            diag_str = ""
            row, col = i, j
            while row < rows and col >= 0:
                diag_str += grid[row][col]
                row += 1
                col -= 1
            count += diag_str.count("XMAS")
            count += diag_str[::-1].count("XMAS")

    return count


def count_x_mas(grid):
    count = 0
    rows = len(grid)
    cols = len(grid[0])

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if grid[i][j] == "A":
                # Check for X-MAS pattern
                if (
                    grid[i - 1][j - 1] == "M"
                    and grid[i - 1][j + 1] == "M"
                    and grid[i + 1][j - 1] == "M"
                    and grid[i + 1][j + 1] == "M"
                ):
                    if (
                        grid[i - 1][j - 1] == "M"
                        and grid[i][j - 1] == "A"
                        and grid[i + 1][j - 1] == "S"
                    ) or (
                        grid[i - 1][j - 1] == "S"
                        and grid[i][j - 1] == "A"
                        and grid[i + 1][j - 1] == "M"
                    ):
                        if (
                            grid[i - 1][j + 1] == "M"
                            and grid[i][j + 1] == "A"
                            and grid[i + 1][j + 1] == "S"
                        ) or (
                            grid[i - 1][j + 1] == "S"
                            and grid[i][j + 1] == "A"
                            and grid[i + 1][j + 1] == "M"
                        ):
                            count += 1
                    elif (
                        grid[i - 1][j - 1] == "M"
                        and grid[i - 1][j] == "A"
                        and grid[i - 1][j + 1] == "S"
                    ) or (
                        grid[i - 1][j - 1] == "S"
                        and grid[i - 1][j] == "A"
                        and grid[i - 1][j + 1] == "M"
                    ):
                        if (
                            grid[i + 1][j - 1] == "M"
                            and grid[i + 1][j] == "A"
                            and grid[i + 1][j + 1] == "S"
                        ) or (
                            grid[i + 1][j - 1] == "S"
                            and grid[i + 1][j] == "A"
                            and grid[i + 1][j + 1] == "M"
                        ):
                            count += 1

    return count


def part1(data: str) -> int:
    """
    Solution for part 1
    """
    grid = [list(line) for line in data.split("\n")]
    return count_xmas(grid)


def part2(data: str) -> int:
    """
    Solution for part 2
    """
    grid = [list(line) for line in data.split("\n")]
    return count_x_mas(grid)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
