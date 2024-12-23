from collections import deque

# Define keypad layouts as graphs with possible moves
numeric_keypad = {
    "7": {"D": "4", "R": "8"},
    "8": {"D": "5", "L": "7", "R": "9"},
    "9": {"D": "6", "L": "8"},
    "4": {"U": "7", "D": "1", "R": "5"},
    "5": {"U": "8", "D": "2", "L": "4", "R": "6"},
    "6": {"U": "9", "D": "3", "L": "5"},
    "1": {"U": "4", "R": "2"},
    "2": {"U": "5", "L": "1", "R": "3"},
    "3": {"U": "6", "L": "2"},
    "0": {"U": "2", "R": "A"},
    "A": {"L": "0"},
}

directional_keypad = {
    "^": {"D": "v", "R": "A"},
    "A": {"D": "v", "L": "v"},
    "<": {"U": "^", "D": "v", "R": "v"},
    "v": {"U": "^", "L": "<", "R": ">"},
    ">": {"U": "A", "L": "v"},
}


# Function to find the shortest sequence on a keypad to achieve a target sequence
def find_shortest_sequence(current_keypad, start_button, target_sequence):
    queue = deque()
    queue.append((start_button, "", 0))
    visited = set()
    visited.add((start_button, 0))

    while queue:
        current_pos, current_seq, seq_idx = queue.popleft()

        if seq_idx == len(target_sequence):
            return current_seq

        for move in ["^", "<", "v", ">"]:
            next_pos = current_keypad.get(current_pos, {}).get(move, None)
            if next_pos:
                if (next_pos, seq_idx) not in visited:
                    visited.add((next_pos, seq_idx))
                    queue.append((next_pos, current_seq + move, seq_idx))

        if "A" in current_keypad.get(current_pos, {}):
            next_pos = current_keypad[current_pos]["A"]
            expected_button = target_sequence[seq_idx]
            if next_pos == expected_button:
                if (next_pos, seq_idx + 1) not in visited:
                    visited.add((next_pos, seq_idx + 1))
                    queue.append((next_pos, current_seq + "A", seq_idx + 1))
    return None  # If no sequence found


# Read input codes
def read_input():
    with open("../input.txt") as f:
        return [line.strip() for line in f.readlines()]


# Main function to calculate the sum of complexities
def main():
    codes = read_input()
    total_complexity = 0

    for code in codes:
        numeric_sequence = code[:-1]  # Exclude the 'A' at the end
        numeric_target = list(numeric_sequence)

        # Find sequence for first robot's directional keypad
        seq_first_robot = find_shortest_sequence(
            directional_keypad, "A", numeric_target
        )
        if seq_first_robot is None:
            continue  # Skip if no sequence found

        # Find sequence for second robot's directional keypad
        seq_second_robot = find_shortest_sequence(
            directional_keypad, "A", list(seq_first_robot)
        )
        if seq_second_robot is None:
            continue  # Skip if no sequence found

        # Find sequence for my directional keypad
        seq_my_keypad = find_shortest_sequence(
            directional_keypad, "A", list(seq_second_robot)
        )
        if seq_my_keypad is None:
            continue  # Skip if no sequence found

        # Calculate complexity
        numeric_value = int(numeric_sequence)
        complexity = len(seq_my_keypad) * numeric_value
        total_complexity += complexity

    print(f"Total Complexity: {total_complexity}")


if __name__ == "__main__":
    main()
