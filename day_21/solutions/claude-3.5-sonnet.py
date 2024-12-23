from collections import deque
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple
import re


@dataclass
class Position:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))


class Keypad:
    def __init__(self, layout: List[List[str]], start_pos: Position):
        self.layout = layout
        self.height = len(layout)
        self.width = len(layout[0])
        self.start_pos = start_pos

    def is_valid_position(self, pos: Position) -> bool:
        return (
            0 <= pos.x < self.width
            and 0 <= pos.y < self.height
            and self.layout[pos.y][pos.x] != " "
        )

    def get_button(self, pos: Position) -> str:
        return self.layout[pos.y][pos.x]


def create_numeric_keypad() -> Keypad:
    layout = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], [" ", "0", "A"]]
    return Keypad(layout, Position(1, 3))  # Start at position of 'A'


def create_directional_keypad() -> Keypad:
    layout = [[" ", "^", "A"], ["<", "v", ">"]]
    return Keypad(layout, Position(2, 0))  # Start at position of 'A'


def find_shortest_path(target_code: str) -> Tuple[str, int]:
    numeric_keypad = create_numeric_keypad()
    directions = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}

    # State consists of (current_position, remaining_code)
    initial_state = (numeric_keypad.start_pos, target_code)
    queue = deque([(initial_state, "")])
    visited = set()

    while queue:
        current_state, path = queue.popleft()
        current_pos, remaining_code = current_state

        if not remaining_code:  # Found complete path
            return path, len(path)

        state_hash = (current_pos.x, current_pos.y, remaining_code)
        if state_hash in visited:
            continue
        visited.add(state_hash)

        # Try each direction
        for dir_key, (dx, dy) in directions.items():
            new_pos = Position(current_pos.x + dx, current_pos.y + dy)

            if not numeric_keypad.is_valid_position(new_pos):
                continue

            current_button = numeric_keypad.get_button(new_pos)
            new_path = path + dir_key

            # If we're at the correct button for the next code digit
            if remaining_code and current_button == remaining_code[0]:
                new_state = (new_pos, remaining_code[1:])
                queue.append((new_state, new_path + "A"))
            else:
                new_state = (new_pos, remaining_code)
                queue.append((new_state, new_path))

    return "", 0  # No path found


def calculate_complexity(code: str, sequence_length: int) -> int:
    # Extract numeric part of the code and convert to integer
    numeric_part = int("".join(filter(str.isdigit, code)))
    return sequence_length * numeric_part


def read_input():
    with open("../input.txt") as f:
        return f.read().strip().split("\n")


def part1(data: str) -> int:
    """
    Solution for part 1
    """
    codes = data.split()
    total_complexity = 0

    for code in codes:
        sequence, length = find_shortest_path(code)
        complexity = calculate_complexity(code, length)
        total_complexity += complexity

    return total_complexity


def part2(data: str) -> int:
    """
    Solution for part 2
    """
    pass


def main():
    data = read_input()

    result1 = part1("\n".join(data))
    print(f"Part 1: {result1}")


if __name__ == "__main__":
    main()
