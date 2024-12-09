import matplotlib.pyplot as plt
import numpy as np
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


def part1(grid: List[str]) -> int:
    """
    Placeholder for Part 1 solution.

    Args:
        grid: Word search grid.

    Returns:
        Example value (to be replaced with actual Part 1 logic).
    """
    # Implement Part 1 logic here if needed
    return 0


def part2(grid: List[str]) -> Tuple[int, List[List[Tuple[int, int]]]]:
    """
    Count the number of X-MAS patterns in the word search grid and store their coordinates.

    An X-MAS consists of two "MAS" sequences arranged in an "X" shape.
    Each "MAS" can be forwards or backwards.

    Args:
        grid: Word search grid.

    Returns:
        A tuple containing:
            - Number of X-MAS patterns found.
            - List of X-MAS patterns, each represented as a list of (row, col) tuples.
    """
    if not grid:
        return 0, []

    rows = len(grid)
    cols = len(grid[0])
    xmas_count = 0
    xmas_patterns = []

    # Iterate through each cell, excluding the borders where an X-MAS can't fit
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            center_char = grid[i][j]
            # Primary diagonal characters
            tl = grid[i - 1][j - 1]  # Top-Left
            br = grid[i + 1][j + 1]  # Bottom-Right
            # Secondary diagonal characters
            tr = grid[i - 1][j + 1]  # Top-Right
            bl = grid[i + 1][j - 1]  # Bottom-Left

            # Define the two diagonals
            primary_diagonal = tl + center_char + br
            secondary_diagonal = tr + center_char + bl

            # Define valid "MAS" and "SAM" sequences
            valid_sequences = {"MAS", "SAM"}

            # Check if both diagonals form a valid "MAS" or "SAM"
            if (primary_diagonal in valid_sequences) and (
                secondary_diagonal in valid_sequences
            ):
                xmas_count += 1
                # Store the coordinates of the X-MAS pattern
                pattern_coords = [
                    (i - 1, j - 1),  # Top-Left
                    (i, j),  # Center
                    (i + 1, j + 1),  # Bottom-Right
                    (i - 1, j + 1),  # Top-Right
                    (i + 1, j - 1),  # Bottom-Left
                ]
                xmas_patterns.append(pattern_coords)

    return xmas_count, xmas_patterns


def visualize_xmas(grid: List[str], xmas_patterns: List[List[Tuple[int, int]]]):
    """
    Visualize the word search grid and highlight X-MAS patterns.
    Creates a clearer view with more space between letters.

    Args:
        grid: Word search grid.
        xmas_patterns: List of X-MAS patterns with their coordinates.
    """
    if not grid:
        print("No grid to visualize.")
        return

    rows = len(grid)
    cols = len(grid[0])

    # Increase figure size and spacing
    fig, ax = plt.subplots(figsize=(cols * 1.2, rows * 1.2))
    ax.set_xlim(-0.5, cols + 0.5)
    ax.set_ylim(-0.5, rows + 0.5)

    # Remove ticks but keep grid
    ax.set_xticks(range(cols + 1))
    ax.set_yticks(range(rows + 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(True, linestyle=":")

    # Invert y-axis to match grid indexing
    ax.invert_yaxis()

    # Plot each letter in the grid with larger font
    for i in range(rows):
        for j in range(cols):
            char = grid[i][j]
            if char != ".":
                ax.text(
                    j + 0.5,
                    i + 0.5,
                    char,
                    ha="center",
                    va="center",
                    fontsize=14,  # Increased font size
                    fontweight="bold",
                )

    # Define colors for different X-MAS patterns
    colors = plt.cm.rainbow(np.linspace(0, 1, len(xmas_patterns)))

    # Highlight each X-MAS pattern
    for pattern, color in zip(xmas_patterns, colors):
        x_coords = [col + 0.5 for _, col in pattern]
        y_coords = [row + 0.5 for row, _ in pattern]
        ax.plot(
            x_coords,
            y_coords,
            marker="o",
            markersize=10,  # Increased marker size
            markeredgecolor="black",
            markerfacecolor=color,
            linestyle="-",
            linewidth=2,
            alpha=0.6,  # Added some transparency
        )

    plt.title("X-MAS Patterns in Grid", pad=20)
    plt.tight_layout()

    # Save the plot
    plt.savefig("xmas_patterns.png", dpi=300, bbox_inches="tight")
    plt.close()


def main():
    """
    Main function to run the Advent of Code solution with visualization.
    """
    word_search_grid = read_input()

    part1_result = part1(word_search_grid)
    part2_result, xmas_patterns = part2(word_search_grid)

    print("Part 1:", part1_result)
    print("Part 2:", part2_result)

    if part2_result > 0:
        visualize_xmas(word_search_grid, xmas_patterns)
    else:
        print("No X-MAS patterns found to visualize.")


if __name__ == "__main__":
    main()
