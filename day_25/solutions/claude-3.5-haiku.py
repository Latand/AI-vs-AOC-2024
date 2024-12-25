def parse_pattern(pattern: str) -> list[int]:
    """
    Convert a pattern into a list of column heights,
    skipping the first and last rows.
    """
    # Split the pattern into rows, skip first and last rows
    rows = pattern.split("\n")[1:-1]

    # Determine number of columns from the first row
    columns = len(rows[0])

    # Calculate height for each column
    heights = []
    for col in range(columns):
        # Count from bottom to top, stop when reaching a '.'
        height = 0
        for row in reversed(rows):
            if row[col] == "#":
                height += 1
            else:
                break
        heights.append(height)

    return heights


def can_fit(lock: list[int], key: list[int]) -> bool:
    """
    Check if a lock and key can fit together without overlapping
    """
    # Ensure lock and key have same length
    if len(lock) != len(key):
        return False

    # Check each column's compatibility
    for lock_height, key_height in zip(lock, key):
        # Total height of lock and key in a column must not exceed 5
        if lock_height + key_height > 5:
            return False

    return True


def solve_puzzle(data: str) -> int:
    """
    Find number of unique lock/key pairs that can fit together
    """
    # Split input into individual patterns
    patterns = data.split("\n\n")

    # Separate into locks and keys
    locks = []
    keys = []

    # Classify each pattern as lock or key based on top row
    for pattern in patterns:
        top_row = pattern.split("\n")[0]
        if all(c == "#" for c in top_row):
            locks.append(parse_pattern(pattern))
        else:
            keys.append(parse_pattern(pattern))

    # Count unique fitting pairs
    fitting_pairs = 0

    for lock in locks:
        for key in keys:
            if can_fit(lock, key):
                fitting_pairs += 1

    return fitting_pairs


def read_input():
    """Read input from the file"""
    with open("../input.txt", "r") as f:
        return f.read().strip()


def main():
    data = read_input()
    result = solve_puzzle(data)
    print(f"Number of unique lock/key pairs that fit: {result}")


if __name__ == "__main__":
    main()
