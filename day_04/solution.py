from typing import List, Tuple


def read_input() -> List[str]:
    """
    Read the input file and return the word search grid.

    Returns:
        List of strings representing the word search grid.
    """
    try:
        with open("input.txt", "r") as input_file:
            return input_file.read().strip().split("\n")
    except FileNotFoundError:
        print("Error: Input file not found.")
        return []


def get_search_directions() -> List[Tuple[int, int]]:
    """
    Define all possible search directions for finding words.

    Returns:
        List of direction tuples (row_delta, column_delta).
    """
    return [
        (0, 1),  # right
        (1, 1),  # down-right diagonal
        (1, 0),  # down
        (1, -1),  # down-left diagonal
        (0, -1),  # left
        (-1, -1),  # up-left diagonal
        (-1, 0),  # up
        (-1, 1),  # up-right diagonal
    ]


def is_valid_grid_position(grid: List[str], row: int, col: int) -> bool:
    """
    Check if the given grid position is within the grid boundaries.

    Args:
        grid: 2D grid of characters
        row: Row index to check
        col: Column index to check

    Returns:
        Boolean indicating if the position is valid
    """
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])


def find_xmas_occurrences(grid: List[str]) -> int:
    """
    Count all unique occurrences of 'XMAS' in the word search grid.

    Args:
        grid: 2D grid of characters to search

    Returns:
        Total number of unique 'XMAS' occurrences
    """
    target_word = "XMAS"
    xmas_count = 0
    unique_locations = set()

    # Iterate through each starting position in the grid
    for start_row in range(len(grid)):
        for start_col in range(len(grid[0])):
            # Check all possible search directions
            for row_delta, col_delta in get_search_directions():
                if is_xmas_at_location(
                    grid, start_row, start_col, row_delta, col_delta
                ):
                    # Track unique occurrences to handle overlaps
                    location = (start_row, start_col, row_delta, col_delta)
                    if location not in unique_locations:
                        unique_locations.add(location)
                        xmas_count += 1

    return xmas_count


def is_xmas_at_location(
    grid: List[str], start_row: int, start_col: int, row_delta: int, col_delta: int
) -> bool:
    """
    Check if 'XMAS' can be formed starting from a specific location and direction.

    Args:
        grid: 2D grid of characters
        start_row: Starting row for the search
        start_col: Starting column for the search
        row_delta: Row direction delta
        col_delta: Column direction delta

    Returns:
        Boolean indicating if 'XMAS' is found at the specified location
    """
    target_word = "XMAS"

    # Check each letter of 'XMAS'
    for i, letter in enumerate(target_word):
        current_row = start_row + i * row_delta
        current_col = start_col + i * col_delta

        # Validate grid position and letter match
        if (
            not is_valid_grid_position(grid, current_row, current_col)
            or grid[current_row][current_col] != letter
        ):
            return False

    return True


def part1(grid: List[str]) -> int:
    """
    Solve part 1 of the puzzle by counting XMAS occurrences.

    Args:
        grid: Word search grid

    Returns:
        Total number of unique XMAS occurrences
    """
    return find_xmas_occurrences(grid)


def part2(grid: List[str]) -> int:
    """
    Count the number of X-MAS patterns in the word search grid.

    An X-MAS pattern consists of two "MAS" sequences arranged in an X shape:
        M.S
         A
        M.S
    Each "MAS" can be read forwards or backwards ("SAM").

    Args:
        grid: Word search grid.

    Returns:
        Number of X-MAS patterns found.
    """
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    xmas_count = 0
    valid_sequences = {"MAS", "SAM"}

    # Iterate through potential center positions (excluding edges)
    for center_row in range(1, rows - 1):
        for center_col in range(1, cols - 1):
            # Get the five characters that form the X pattern
            x_pattern = {
                "center": grid[center_row][center_col],
                # Primary diagonal (top-left to bottom-right)
                "top_left": grid[center_row - 1][center_col - 1],
                "bottom_right": grid[center_row + 1][center_col + 1],
                # Secondary diagonal (top-right to bottom-left)
                "top_right": grid[center_row - 1][center_col + 1],
                "bottom_left": grid[center_row + 1][center_col - 1],
            }

            # Form the two diagonal sequences including the center character
            primary_diagonal = (
                x_pattern["top_left"] + x_pattern["center"] + x_pattern["bottom_right"]
            )
            secondary_diagonal = (
                x_pattern["top_right"] + x_pattern["center"] + x_pattern["bottom_left"]
            )

            # Check if both diagonals form valid MAS/SAM sequences
            if (
                primary_diagonal in valid_sequences
                and secondary_diagonal in valid_sequences
            ):
                xmas_count += 1

    return xmas_count


if __name__ == "__main__":
    grid = read_input()
    print("Part 1:", part1(grid))
    print("Part 2:", part2(grid))
