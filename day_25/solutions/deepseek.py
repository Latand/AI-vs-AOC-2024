def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def is_lock(pattern):
    first_row = pattern[0]
    last_row = pattern[-1]
    return all(c == "#" for c in first_row) and all(c == "." for c in last_row)


def is_key(pattern):
    first_row = pattern[0]
    last_row = pattern[-1]
    return all(c == "." for c in first_row) and all(c == "#" for c in last_row)


def calculate_lock_heights(pattern, num_middle_rows, num_columns):
    heights = [0] * num_columns
    for col in range(num_columns):
        count = 0
        for row in range(1, len(pattern) - 1):  # Skip first and last rows
            if pattern[row][col] == "#":
                count += 1
            else:
                break
        heights[col] = count
    return heights


def calculate_key_heights(pattern, num_middle_rows, num_columns):
    heights = [0] * num_columns
    for col in range(num_columns):
        count = 0
        for row in reversed(range(1, len(pattern) - 1)):  # Skip first and last rows
            if pattern[row][col] == "#":
                count += 1
            else:
                break
        heights[col] = count
    return heights


def main():
    data = read_input().split("\n\n")
    patterns = [pattern.split("\n") for pattern in data]

    locks = []
    keys = []
    for pattern in patterns:
        if is_lock(pattern):
            num_middle_rows = len(pattern) - 2
            num_columns = len(pattern[1])  # Skip first and last rows
            heights = calculate_lock_heights(pattern, num_middle_rows, num_columns)
            locks.append(heights)
        elif is_key(pattern):
            num_middle_rows = len(pattern) - 2
            num_columns = len(pattern[1])  # Skip first and last rows
            heights = calculate_key_heights(pattern, num_middle_rows, num_columns)
            keys.append(heights)

    total_available_space = (
        num_middle_rows  # This should be consistent across all patterns
    )

    valid_pairs = 0
    for lock in locks:
        for key in keys:
            if all(
                lock[i] + key[i] <= total_available_space for i in range(num_columns)
            ):
                valid_pairs += 1

    print(f"Number of valid lock/key pairs: {valid_pairs}")


if __name__ == "__main__":
    main()
