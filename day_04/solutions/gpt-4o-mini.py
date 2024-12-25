def read_input():
    with open("../input.txt") as f:
        return f.read().strip().splitlines()


# Check for "XMAS" in various directions
def count_xmas(grid, word="XMAS"):
    n_rows = len(grid)
    n_cols = len(grid[0])
    count = 0

    def check_word_in_direction(start_r, start_c, dr, dc):
        nonlocal count
        # Check if the word "XMAS" can be formed starting at (start_r, start_c)
        # moving in direction (dr, dc)
        for i in range(len(word)):
            r = start_r + i * dr
            c = start_c + i * dc
            if not (0 <= r < n_rows and 0 <= c < n_cols):
                return False
            if grid[r][c] != word[i]:
                return False
        return True

    # Horizontal and Vertical
    for r in range(n_rows):
        for c in range(n_cols):
            # Horizontal right
            if check_word_in_direction(r, c, 0, 1):
                count += 1
            # Horizontal left
            if check_word_in_direction(r, c, 0, -1):
                count += 1
            # Vertical down
            if check_word_in_direction(r, c, 1, 0):
                count += 1
            # Vertical up
            if check_word_in_direction(r, c, -1, 0):
                count += 1
            # Diagonals
            if check_word_in_direction(r, c, 1, 1):
                count += 1
            if check_word_in_direction(r, c, -1, -1):
                count += 1
            if check_word_in_direction(r, c, 1, -1):
                count += 1
            if check_word_in_direction(r, c, -1, 1):
                count += 1

    return count


# Check for the "X-MAS" shape
def count_xmas_shape(grid):
    n_rows = len(grid)
    n_cols = len(grid[0])
    count = 0

    def check_xmas_shape(r, c):
        # Check if there is an "X-MAS" shape with center at (r, c)
        if not (0 <= r < n_rows and 0 <= c < n_cols):
            return False
        if grid[r][c] != "A":
            return False
        # Positions for "M" and "S"
        directions = [
            (-1, -1, "M"),
            (1, 1, "S"),  # Top-left and Bottom-right
            (1, -1, "M"),
            (-1, 1, "S"),  # Bottom-left and Top-right
        ]
        for dr, dc, letter in directions:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < n_rows and 0 <= nc < n_cols):
                return False
            if grid[nr][nc] != letter:
                return False
        return True

    for r in range(1, n_rows - 1):  # We need at least 1 row above and below
        for c in range(
            1, n_cols - 1
        ):  # We need at least 1 column to the left and right
            if check_xmas_shape(r, c):
                count += 1

    return count


def part1(data):
    return count_xmas(data)


def part2(data):
    return count_xmas_shape(data)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
