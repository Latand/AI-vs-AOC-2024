def read_input():
    """
    Reads the puzzle input (word search) from ../input.txt and
    returns a list of strings, each string representing one row
    of the puzzle.
    """
    with open("../input.txt") as f:
        return [line.strip() for line in f.readlines()]


def part1(grid) -> int:
    """
    Part 1:
    Count how many times the word 'XMAS' appears in the grid,
    in all 8 possible directions.
    """
    word = "XMAS"
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Directions: (dx, dy)
    # 8 directions: up, down, left, right, and the 4 diagonals
    directions = [
        (-1, 0),  # up
        (1, 0),  # down
        (0, -1),  # left
        (0, 1),  # right
        (-1, -1),  # up-left
        (-1, 1),  # up-right
        (1, -1),  # down-left
        (1, 1),  # down-right
    ]

    def in_bounds(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def count_occurrences_of_word_at(r, c):
        """Count how many times 'word' starts at (r, c) in any of the 8 directions."""
        count_here = 0
        for dx, dy in directions:
            # Check if we can fit the word in this direction
            # last position will be r + (len(word)-1)*dx, c + (len(word)-1)*dy
            rr = r + (len(word) - 1) * dx
            cc = c + (len(word) - 1) * dy
            if not in_bounds(rr, cc):
                continue  # can't fit the word in this direction

            # Check each character
            match = True
            for i in range(len(word)):
                nr = r + i * dx
                nc = c + i * dy
                if grid[nr][nc] != word[i]:
                    match = False
                    break
            if match:
                count_here += 1
        return count_here

    total_count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == word[0]:  # quick check to skip obviously impossible starts
                total_count += count_occurrences_of_word_at(r, c)
    return total_count


def part2(grid) -> int:
    """
    Part 2:
    Count how many "X-MAS" patterns appear.

    A "X-MAS" is defined as a 3x3 'X' shape with 'A' in the center.
    Each diagonal (top-left -> center -> bottom-right) and
    (top-right -> center -> bottom-left) must spell 'MAS' or 'SAM'.

    The center must be 'A'.
    The corners must be M and S in one of the 4 permutations:
        1) (0,0)->'M', (2,2)->'S'  AND  (0,2)->'M', (2,0)->'S'
        2) (0,0)->'M', (2,2)->'S'  AND  (0,2)->'S', (2,0)->'M'
        3) (0,0)->'S', (2,2)->'M'  AND  (0,2)->'M', (2,0)->'S'
        4) (0,0)->'S', (2,2)->'M'  AND  (0,2)->'S', (2,0)->'M'
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # We only check 3x3 sub-grids, so row must go up to rows-2,
    # col must go up to cols-2.

    # All valid corner permutations for the diagonals
    valid_patterns = [
        ("M", "S", "M", "S"),  # top-left=M, bottom-right=S, top-right=M, bottom-left=S
        ("M", "S", "S", "M"),  # top-left=M, bottom-right=S, top-right=S, bottom-left=M
        ("S", "M", "M", "S"),  # top-left=S, bottom-right=M, top-right=M, bottom-left=S
        ("S", "M", "S", "M"),  # top-left=S, bottom-right=M, top-right=S, bottom-left=M
    ]

    count_x_mas = 0

    for r in range(rows - 2):
        for c in range(cols - 2):
            # Center must be 'A'
            if grid[r + 1][c + 1] != "A":
                continue

            # top-left (r, c), bottom-right (r+2, c+2)
            # top-right (r, c+2), bottom-left (r+2, c)
            tl = grid[r][c]  # top-left
            br = grid[r + 2][c + 2]  # bottom-right
            tr = grid[r][c + 2]  # top-right
            bl = grid[r + 2][c]  # bottom-left

            # Check if (tl, br, tr, bl) is in valid_patterns
            if (tl, br, tr, bl) in valid_patterns:
                count_x_mas += 1

    return count_x_mas


def main():
    grid = read_input()

    result1 = part1(grid)
    print(f"Part 1: {result1}")

    result2 = part2(grid)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
